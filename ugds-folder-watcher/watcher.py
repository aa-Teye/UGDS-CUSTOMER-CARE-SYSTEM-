"""
Main UGDS Folder Tracker Watcher service.
Monitors folder tracker .txt files, parses patient records, and dispatches SMS via Arkesel.
"""

import os
import sys
import time
import argparse
import logging
from typing import Optional
from dotenv import load_dotenv

from parser import parse_tracker_line
from database import (
    is_recently_sent,
    log_message,
    get_file_checkpoint,
    update_file_checkpoint
)
from sms_sender import ArkeselSMSService

# Determine base directory (works for both standard python and PyInstaller .exe)
if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load configuration from .env file
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Set up logging
LOG_FILE = os.path.join(BASE_DIR, "watcher.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOG_FILE, encoding="utf-8")
    ]
)

logger = logging.getLogger("ugds-watcher")

def get_env_bool(key: str, default: bool = True) -> bool:
    val = os.getenv(key, str(default)).strip().lower()
    return val in ("true", "1", "yes", "t")

def get_env_int(key: str, default: int = 7) -> int:
    try:
        return int(os.getenv(key, str(default)))
    except ValueError:
        return default

class TrackerWatcher:
    def __init__(self):
        self.api_key = os.getenv("ARKESEL_API_KEY", "").strip()
        self.sender_id = os.getenv("ARKESEL_SENDER_ID", "UGDS").strip()
        self.dry_run = get_env_bool("DRY_RUN", False)
        raw_watch = os.getenv("WATCH_FOLDER", "./incoming_files").strip()
        self.watch_folder = raw_watch if os.path.isabs(raw_watch) else os.path.normpath(os.path.join(BASE_DIR, raw_watch))


        raw_spec = os.getenv("SPECIFIC_TRACKER_FILE", "").strip()
        self.specific_file = (
            raw_spec if (not raw_spec or os.path.isabs(raw_spec)) else os.path.normpath(os.path.join(BASE_DIR, raw_spec))
        )

        self.survey_url = os.getenv("SURVEY_BASE_URL", "https://ugds-customer-experience.vercel.app/feedback").strip()
        self.sms_template = os.getenv(
            "SMS_MESSAGE_TEMPLATE",
            "Dear {name}, thank you for visiting UGDS. Please rate your experience: {link}"
        ).strip()
        self.max_sms_per_week = get_env_int("MAX_SMS_PER_WEEK", 1)
        self.watch_new_only = os.getenv("WATCH_NEW_ONLY", "true").strip().lower() in ("true", "1", "yes")


        self.sms_service = ArkeselSMSService(
            api_key=self.api_key,
            sender_id=self.sender_id,
            dry_run=self.dry_run
        )

        # Ensure watch folder exists
        os.makedirs(self.watch_folder, exist_ok=True)

    def print_banner(self):
        mode_str = "DRY-RUN (SIMULATION ONLY - NO CREDITS USED)" if self.dry_run else "LIVE (REAL SMS WILL BE SENT)"
        logger.info("=" * 60)
        logger.info("  UGDS PATIENT OUTREACH TRACKER WATCHER")
        logger.info(f"  Mode:            {mode_str}")
        logger.info(f"  Sender ID:       {self.sender_id}")
        logger.info(f"  Watch Folder:    {os.path.abspath(self.watch_folder)}")
        if self.specific_file:
            logger.info(f"  Specific File:   {os.path.abspath(self.specific_file)}")
        logger.info(f"  Weekly Limit:    Max {self.max_sms_per_week} SMS per patient / week")
        logger.info("=" * 60)

    def process_file(self, file_path: str, force_full: bool = False):
        """Processes a single tracker text file, sending messages for new records."""
        if not os.path.exists(file_path):
            logger.warning(f"File not found: {file_path}")
            return

        mtime = os.path.getmtime(file_path)
        checkpoint = get_file_checkpoint(file_path)
        last_line_read = 0 if force_full else checkpoint["last_line_read"]

        # If file hasn't changed, skip
        if not force_full and checkpoint["last_modified"] == mtime:
            return

        # Try utf-8 first, fallback to latin-1 for Windows legacy files
        content_lines = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content_lines = f.readlines()
        except UnicodeDecodeError:
            with open(file_path, "r", encoding="latin-1") as f:
                content_lines = f.readlines()

        total_lines = len(content_lines)

        # Safety: on first encounter of an existing large file, bookmark at end if watch_new_only is active
        is_first_encounter = (checkpoint["last_modified"] == 0.0 and checkpoint["last_line_read"] == 0)
        if is_first_encounter and self.watch_new_only and not force_full and total_lines > 10:
            logger.info(f"First scan of existing file ({total_lines} lines). Bookmarked at end so old records are not re-sent. Listening for new scans...")
            update_file_checkpoint(file_path, mtime, total_lines)
            return

        if last_line_read >= total_lines and not force_full:
            # Nothing new added
            update_file_checkpoint(file_path, mtime, total_lines)
            return

        logger.info(f"Processing tracker file: {file_path} (from line {last_line_read + 1} to {total_lines})")
        lines_to_process = content_lines[last_line_read:]

        stats = {
            "total_processed": 0,
            "dispatched": 0,
            "skipped_no_phone": 0,
            "skipped_duplicate": 0,
            "failed": 0
        }

        current_line_idx = last_line_read
        for line in lines_to_process:
            current_line_idx += 1
            record = parse_tracker_line(line)
            if not record:
                update_file_checkpoint(file_path, mtime, current_line_idx)
                continue

            stats["total_processed"] += 1
            folder_no = record["folder_number"]
            patient_name = record["full_name"]
            mobile = record["primary_mobile"]

            if not mobile:
                logger.info(f"Line {current_line_idx}: Skipped {patient_name} (Folder: {folder_no}) - No valid Ghanaian mobile in '{record['raw_phone']}'")
                stats["skipped_no_phone"] += 1
                update_file_checkpoint(file_path, mtime, current_line_idx)
                continue

            # Duplicate / Weekly limit check (max 3 times in 7 days)
            if is_recently_sent(folder_no, mobile, self.max_sms_per_week):
                logger.info(f"Line {current_line_idx}: Skipped {patient_name} (Folder: {folder_no}) - Reached weekly limit of {self.max_sms_per_week} SMS.")
                stats["skipped_duplicate"] += 1
                update_file_checkpoint(file_path, mtime, current_line_idx)
                continue

            # Generate survey link
            survey_link = f"{self.survey_url}"

            # Format SMS message
            sms_text = self.sms_template.format(

                name=record["first_name"],
                folder=folder_no,
                link=survey_link
            )

            # Dispatch via Arkesel
            result = self.sms_service.send_sms(mobile, sms_text)
            status = result.get("status", "FAILED")

            if status in ("SENT", "DRY_RUN"):
                stats["dispatched"] += 1
            else:
                stats["failed"] += 1

            # Log to SQLite
            log_message(
                folder_number=folder_no,
                phone_number=mobile,
                patient_name=patient_name,
                message_text=sms_text,
                status=status,
                arkesel_response=str(result),
                source_file=os.path.basename(file_path)
            )
            update_file_checkpoint(file_path, mtime, current_line_idx)

        # Final checkpoint update
        update_file_checkpoint(file_path, mtime, total_lines)


        logger.info(
            f"Done {os.path.basename(file_path)}: "
            f"Processed={stats['total_processed']}, "
            f"Dispatched={stats['dispatched']}, "
            f"Duplicates={stats['skipped_duplicate']}, "
            f"NoMobile={stats['skipped_no_phone']}, "
            f"Failed={stats['failed']}"
        )

    def process_edump_diff(self, old_file: str, new_file: str):
        """Extracts newly added or modified lines between two consecutive hourly dumps."""
        logger.info(f"Comparing hourly dumps to detect both new and returning patients:")
        logger.info(f"  Previous: {os.path.basename(old_file)}")
        logger.info(f"  Latest:   {os.path.basename(new_file)}")

        try:
            with open(old_file, "r", encoding="utf-8", errors="replace") as f:
                old_lines = set(line.strip() for line in f if line.strip())
        except Exception as e:
            logger.warning(f"Could not read previous dump {old_file}: {e}")
            old_lines = set()

        try:
            with open(new_file, "r", encoding="utf-8", errors="replace") as f:
                new_lines = [line.strip() for line in f if line.strip()]
        except Exception as e:
            logger.error(f"Could not read latest dump {new_file}: {e}")
            return

        diff_lines = [l for l in new_lines if l not in old_lines]
        logger.info(f"Found {len(diff_lines)} updated/new patient record(s) in latest dump.")

        mtime = os.path.getmtime(new_file)
        stats = {"total_processed": 0, "dispatched": 0, "skipped_no_phone": 0, "skipped_duplicate": 0, "failed": 0}

        for line in diff_lines:
            record = parse_tracker_line(line)
            if not record:
                continue

            stats["total_processed"] += 1
            folder_no = record["folder_number"]
            patient_name = record["full_name"]
            mobile = record["primary_mobile"]

            if not mobile:
                stats["skipped_no_phone"] += 1
                continue

            if is_recently_sent(folder_no, mobile, self.max_sms_per_week):
                logger.info(f"Skipped {patient_name} (Folder: {folder_no}) - Reached weekly limit of {self.max_sms_per_week} SMS.")
                stats["skipped_duplicate"] += 1
                continue

            survey_link = f"{self.survey_url}"
            sms_text = self.sms_template.format(
                name=record["first_name"],
                folder=folder_no,
                link=survey_link
            )

            result = self.sms_service.send_sms(mobile, sms_text)
            status = result.get("status", "FAILED")

            if status in ("SENT", "DRY_RUN"):
                stats["dispatched"] += 1
            else:
                stats["failed"] += 1

            log_message(
                folder_number=folder_no,
                phone_number=mobile,
                patient_name=patient_name,
                message_text=sms_text,
                status=status,
                arkesel_response=str(result),
                source_file=os.path.basename(new_file)
            )

        update_file_checkpoint(new_file, mtime, len(new_lines))
        logger.info(
            f"Dump Diff Completed: Processed={stats['total_processed']}, "
            f"Dispatched={stats['dispatched']}, Duplicates={stats['skipped_duplicate']}, "
            f"NoMobile={stats['skipped_no_phone']}, Failed={stats['failed']}"
        )

    def scan_directory(self):
        """Scans the watch folder and all subfolders for active tracker .txt files."""
        if self.specific_file and os.path.exists(self.specific_file):
            self.process_file(self.specific_file)
            return

        if not os.path.exists(self.watch_folder):
            return

        # Find all .txt files recursively
        txt_files = []
        for root, _, files in os.walk(self.watch_folder):
            for fname in files:
                if fname.lower().endswith(".txt"):
                    fpath = os.path.join(root, fname)
                    if os.path.isfile(fpath):
                        txt_files.append(fpath)

        # Sort by modification time descending (newest first)
        txt_files.sort(key=lambda p: os.path.getmtime(p) if os.path.exists(p) else 0, reverse=True)

        # Detect hourly eDump series (e.g. eDump_2026_*.txt)
        edump_files = [f for f in txt_files if "edump_" in os.path.basename(f).lower()]
        if len(edump_files) >= 2:
            latest_dump = edump_files[0]
            checkpoint = get_file_checkpoint(latest_dump)
            mtime = os.path.getmtime(latest_dump)
            if checkpoint["last_modified"] != mtime:
                # Compare latest with immediately preceding dump
                prev_dump = edump_files[1]
                self.process_edump_diff(prev_dump, latest_dump)
                return

        for fpath in txt_files:
            self.process_file(fpath)


    def start_polling_loop(self, poll_interval: int = 5):
        """Continuous polling loop to detect changes or new files."""
        self.print_banner()
        logger.info(f"Watching for tracker files every {poll_interval}s. Press Ctrl+C to stop.")
        try:
            while True:
                self.scan_directory()
                time.sleep(poll_interval)
        except KeyboardInterrupt:
            logger.info("Watcher stopped by user.")

def main():
    parser = argparse.ArgumentParser(description="UGDS Patient Outreach Watcher & Real-Time Poller")
    parser.add_argument("--process-file", type=str, help="Process a specific tracker .txt file once and exit")
    parser.add_argument("--once", action="store_true", help="Scan watch folder once and exit")
    parser.add_argument("--poll-interval", type=int, default=5, help="Seconds between scan checks (default: 5)")
    parser.add_argument("--force-full", action="store_true", help="Force full reprocessing from line 1 (ignoring checkpoints)")
    parser.add_argument("--discover-mysql", action="store_true", help="Run the interactive MySQL database auto-discovery tool")
    parser.add_argument("--mysql", action="store_true", help="Run the direct MySQL real-time live watcher")
    parser.add_argument("--birthdays-preview", action="store_true", help="Preview patients celebrating birthdays today")
    parser.add_argument("--birthdays-send", action="store_true", help="Dispatch automated birthday wishes for today")
    parser.add_argument("--birthdays-daemon", action="store_true", help="Run birthday background daemon (sends daily at 8:00 AM)")

    args = parser.parse_args()

    if getattr(args, "discover_mysql", False):
        import discover_mysql
        discover_mysql.main()
        return

    if getattr(args, "birthdays_preview", False):
        import birthday_engine
        birthday_engine.BirthdayEngine().preview_today()
        return

    if getattr(args, "birthdays_send", False):
        import birthday_engine
        birthday_engine.BirthdayEngine().dispatch_todays_birthdays()
        return

    if getattr(args, "birthdays_daemon", False):
        import birthday_engine
        birthday_engine.BirthdayEngine().run_daily_daemon()
        return

    if args.mysql or os.getenv("WATCHER_MODE", "").strip().lower() == "mysql":
        import mysql_watcher
        mysql_watcher.main()
        return


    watcher = TrackerWatcher()

    if args.process_file:
        watcher.print_banner()
        watcher.process_file(args.process_file, force_full=args.force_full)
    elif args.once:
        watcher.print_banner()
        watcher.scan_directory()
    else:
        watcher.start_polling_loop(poll_interval=args.poll_interval)

if __name__ == "__main__":
    main()

