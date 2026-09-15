"""
eArchiver Direct MySQL Live Poller & SMS Dispatcher.
Connects directly to MySQL over TCP (port 3307), listens for live scan events,
fetches patient phone numbers in real-time, and dispatches SMS via Arkesel.
"""

import os
import sys
import time
import logging
import pymysql
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple

from dotenv import load_dotenv
from database import init_db, log_message, is_recently_sent
from sms_sender import ArkeselSMSService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("watcher.log", encoding="utf-8")
    ]
)
logger = logging.getLogger("UGDS_MySQL_Watcher")

if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

env_path = os.path.join(BASE_DIR, ".env")
if os.path.exists(env_path):
    load_dotenv(env_path)


def clean_ghana_phone(raw_phone: str) -> Optional[str]:
    """Extracts a valid Ghanaian mobile number from raw string."""
    if not raw_phone:
        return None
    import re
    cleaned = re.sub(r"[^\d]", "", str(raw_phone))
    # Handle numbers starting with 0
    if len(cleaned) == 10 and cleaned.startswith("0"):
        cleaned = "233" + cleaned[1:]
    elif len(cleaned) == 9 and not cleaned.startswith("0"):
        cleaned = "233" + cleaned
    elif len(cleaned) == 12 and cleaned.startswith("233"):
        pass
    else:
        return None

    # Verify mobile prefix (024, 054, 055, 059, 027, 057, 026, 020, 050)
    prefix = cleaned[3:5]
    if prefix in {"24", "54", "55", "59", "27", "57", "26", "20", "50", "28"}:
        return cleaned
    return None


class MySQLWatcher:
    def __init__(self):
        init_db()
        self.host = os.getenv("MYSQL_HOST", "127.0.0.1").strip()
        self.port = int(os.getenv("MYSQL_PORT", "3307"))
        self.user = os.getenv("MYSQL_USER", "root").strip()
        self.password = os.getenv("MYSQL_PASSWORD", "").strip()
        self.database = os.getenv("MYSQL_DATABASE", "").strip()

        self.movement_table = os.getenv("MYSQL_MOVEMENT_TABLE", "").strip()
        self.patient_table = os.getenv("MYSQL_PATIENT_TABLE", "").strip()

        self.api_key = os.getenv("ARKESEL_API_KEY", "").strip()
        self.sender_id = os.getenv("ARKESEL_SENDER_ID", "UGDS").strip()
        self.dry_run = os.getenv("DRY_RUN", "False").strip().lower() in ("true", "1", "yes")

        self.survey_url = os.getenv("SURVEY_BASE_URL", "https://ugds-customer-experience.vercel.app/survey").strip()
        self.sms_template = os.getenv(
            "SMS_MESSAGE_TEMPLATE",
            "UGDS PATIENT FEEDBACK: Dear {name}, thank you for visiting UGDS. Please rate your experience: {link}"
        ).strip()
        self.max_sms_per_week = int(os.getenv("MAX_SMS_PER_WEEK", "1"))

        self.sms_service = ArkeselSMSService(
            api_key=self.api_key,
            sender_id=self.sender_id,
            dry_run=self.dry_run
        )

        self.last_seen_id = None
        self.conn = None

    def get_connection(self):
        if self.conn:
            try:
                self.conn.ping(reconnect=True)
                return self.conn
            except Exception:
                pass
        self.conn = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=5
        )
        return self.conn

    def print_banner(self):
        mode_str = "DRY-RUN (SIMULATION ONLY)" if self.dry_run else "LIVE (REAL SMS SENT)"
        logger.info("=" * 60)
        logger.info("  UGDS PATIENT OUTREACH — REAL-TIME MYSQL WATCHER")
        logger.info(f"  Mode:            {mode_str}")
        logger.info(f"  Database Target: {self.host}:{self.port} / {self.database}")
        logger.info(f"  Movement Table:  {self.movement_table}")
        logger.info(f"  Patient Table:   {self.patient_table}")
        logger.info(f"  Weekly Limit:    Max {self.max_sms_per_week} SMS / patient / week")
        logger.info("=" * 60)

    def initialize_checkpoint(self):
        """Sets checkpoint to the current latest ID so old scans are ignored."""
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:
                # Find primary key or auto-increment column
                cursor.execute(f"SELECT MAX(id) AS max_id FROM `{self.movement_table}`;")
                row = cursor.fetchone()
                self.last_seen_id = row["max_id"] or 0
                logger.info(f"Initialized live stream checkpoint at movement ID {self.last_seen_id}.")
                logger.info("Listening for incoming patient scans...")
        except Exception as e:
            logger.warning(f"Could not initialize ID checkpoint: {e}. Will watch from current time.")
            self.last_seen_id = 0

    def check_for_new_scans(self):
        """Queries for newly scanned records since last_seen_id."""
        conn = self.get_connection()
        with conn.cursor() as cursor:
            # Query new movement rows joined with patient table if separate
            if self.patient_table and self.patient_table != self.movement_table:
                query = f"""
                    SELECT m.id, m.folder_number, p.name, p.phone, p.location
                    FROM `{self.movement_table}` m
                    LEFT JOIN `{self.patient_table}` p ON m.folder_number = p.folder_number
                    WHERE m.id > %s
                    ORDER BY m.id ASC
                    LIMIT 25;
                """
            else:
                query = f"""
                    SELECT id, folder_number, name, phone
                    FROM `{self.movement_table}`
                    WHERE id > %s
                    ORDER BY id ASC
                    LIMIT 25;
                """
            cursor.execute(query, (self.last_seen_id,))
            rows = cursor.fetchall()
            return rows

    def process_scan_row(self, row: Dict[str, Any]):
        row_id = row.get("id")
        folder_no = str(row.get("folder_number") or "").strip()
        raw_name = str(row.get("name") or "Patient").strip()
        raw_phone = str(row.get("phone") or "").strip()

        mobile = clean_ghana_phone(raw_phone)
        if not mobile:
            logger.info(f"Scan #{row_id}: Skipped {raw_name} (Folder: {folder_no}) - No valid Ghanaian mobile in '{raw_phone}'")
            return

        # Check weekly frequency limit
        if is_recently_sent(folder_no, mobile, max_per_week=self.max_sms_per_week):
            logger.info(f"Scan #{row_id}: Skipped {raw_name} (Folder: {folder_no}) - Reached weekly limit of {self.max_sms_per_week} SMS.")
            return

        first_name = raw_name.split()[0] if raw_name else "Patient"
        sms_text = self.sms_template.format(
            name=first_name,
            folder=folder_no,
            link=self.survey_url
        )

        # Dispatch via Arkesel
        result = self.sms_service.send_sms(mobile, sms_text)
        status = result.get("status", "FAILED")

        # Log into SQLite history
        log_message(
            folder_number=folder_no,
            phone_number=mobile,
            patient_name=raw_name,
            message_text=sms_text,
            status=status,
            arkesel_response=str(result),
            source_file=f"mysql:{self.movement_table}"
        )

    def start_polling(self, poll_interval: int = 2):
        self.print_banner()
        self.initialize_checkpoint()
        try:
            while True:
                try:
                    new_scans = self.check_for_new_scans()
                    for scan in new_scans:
                        self.process_scan_row(scan)
                        self.last_seen_id = max(self.last_seen_id, scan.get("id", self.last_seen_id))
                except pymysql.MySQLError as e:
                    logger.error(f"MySQL query error: {e}. Retrying in 5s...")
                    time.sleep(5)
                except Exception as e:
                    logger.error(f"Unexpected error: {e}")

                time.sleep(poll_interval)
        except KeyboardInterrupt:
            logger.info("Watcher stopped by user.")


def main():
    watcher = MySQLWatcher()
    watcher.start_polling()

if __name__ == "__main__":
    main()
