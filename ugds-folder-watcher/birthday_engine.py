"""
UGDS Automated Patient Birthday Engine.
Extracts birthdays from patient codes, checks who is celebrating today,
and automatically dispatches personalized birthday wishes via Arkesel.
"""

import os
import sys
import re
import time
import sqlite3
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

from dotenv import load_dotenv
from sms_sender import ArkeselSMSService
from parser import parse_tracker_line

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("birthday.log", encoding="utf-8")
    ]
)
logger = logging.getLogger("UGDS_Birthday_Engine")

if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

env_path = os.path.join(BASE_DIR, ".env")
if os.path.exists(env_path):
    load_dotenv(env_path)

DB_PATH = os.path.join(BASE_DIR, "sent_history.db")

def init_birthday_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sent_birthdays (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                folder_number TEXT,
                phone_number TEXT NOT NULL,
                patient_name TEXT,
                birth_year_sent INTEGER NOT NULL,
                message_text TEXT,
                status TEXT NOT NULL,
                arkesel_response TEXT,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(folder_number, birth_year_sent)
            );
        """)
        conn.commit()

init_birthday_db()

def has_received_birthday_this_year(folder_number: str, phone_number: str, year: int) -> bool:
    """Checks if patient already received their birthday message this calendar year."""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT id FROM sent_birthdays
            WHERE (folder_number = ? OR phone_number = ?)
              AND birth_year_sent = ?
              AND status IN ('SENT', 'DRY_RUN');
        """, (folder_number, phone_number, year))
        return cur.fetchone() is not None

def log_birthday_send(folder_number: str, phone_number: str, name: str, year: int, msg: str, status: str, resp: str):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO sent_birthdays 
            (folder_number, phone_number, patient_name, birth_year_sent, message_text, status, arkesel_response)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(folder_number, birth_year_sent) DO UPDATE SET
                status = excluded.status,
                sent_at = CURRENT_TIMESTAMP;
        """, (folder_number, phone_number, name, year, msg, status, resp))
        conn.commit()

def extract_dob(patient_code: str) -> Optional[Dict[str, int]]:
    """Extracts day and month from patient code like YSINT12011964-1."""
    if not patient_code:
        return None
    m = re.search(r'(\d{2})(\d{2})(\d{4})', patient_code)
    if m:
        day, month, year = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if 1 <= day <= 31 and 1 <= month <= 12 and 1900 <= year <= 2026:
            return {"day": day, "month": month, "year": year, "dob": f"{day:02d}/{month:02d}/{year}"}
    return None


class BirthdayEngine:
    def __init__(self):
        self.api_key = os.getenv("ARKESEL_API_KEY", "").strip()
        self.sender_id = os.getenv("ARKESEL_SENDER_ID", "UGDS").strip()
        self.dry_run = os.getenv("DRY_RUN", "False").strip().lower() in ("true", "1", "yes")
        
        self.template = os.getenv(
            "BIRTHDAY_MESSAGE_TEMPLATE",
            "Happy Birthday {name}! 🎂 Best wishes from all of us at the University of Ghana Dental School, Korle Bu. May your new year bring you happiness, success, and glowing smiles. Have a blessed and memorable celebration!"
        ).strip()
        
        self.watch_folder = os.getenv("WATCH_FOLDER", "C:\\eArchive_Bible\\Old_Bible").strip()
        self.sms_service = ArkeselSMSService(
            api_key=self.api_key,
            sender_id=self.sender_id,
            dry_run=self.dry_run
        )

    def find_master_file(self) -> Optional[str]:
        """Finds the most recent or largest tracker/dump text file."""
        if not os.path.exists(self.watch_folder):
            return None
            
        candidates = []
        for root, _, files in os.walk(self.watch_folder):
            for fname in files:
                if fname.lower().endswith(".txt"):
                    fpath = os.path.join(root, fname)
                    if os.path.isfile(fpath):
                        candidates.append((fpath, os.path.getmtime(fpath), os.path.getsize(fpath)))
                        
        if not candidates:
            return None
            
        # Sort by file size descending (to pick the master archive with 125,000 records)
        candidates.sort(key=lambda x: (x[2], x[1]), reverse=True)
        return candidates[0][0]

    def load_todays_birthday_patients(self, target_day: int = None, target_month: int = None) -> List[Dict[str, Any]]:
        now = datetime.now()
        day = target_day or now.day
        month = target_month or now.month
        
        master_file = self.find_master_file()
        if not master_file:
            logger.warning(f"No master file found in: {self.watch_folder}")
            return []
            
        logger.info(f"Scanning archive: {master_file} for birthdays on {day:02d}/{month:02d}...")
        
        try:
            with open(master_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            with open(master_file, "r", encoding="latin-1") as f:
                lines = f.readlines()
                
        birthday_patients = []
        seen_phones = set()
        
        for line in lines:
            record = parse_tracker_line(line)
            if not record:
                continue
                
            code = record.get("patient_code", "")
            dob = extract_dob(code)
            if not dob:
                continue
                
            if dob["day"] == day and dob["month"] == month:
                mobile = record.get("primary_mobile")
                if mobile and mobile not in seen_phones:
                    seen_phones.add(mobile)
                    record["dob"] = dob["dob"]
                    birthday_patients.append(record)
                    
        return birthday_patients

    def preview_today(self):
        now = datetime.now()
        patients = self.load_todays_birthday_patients()
        print("=" * 70)
        print(f"  UGDS PATIENT BIRTHDAYS FOR TODAY ({now.strftime('%d %B %Y')})")
        print(f"  Total Celebrating Today: {len(patients)}")
        print("=" * 70)
        
        if not patients:
            print("  No patient birthdays found for today in the master archive.")
            return
            
        for i, p in enumerate(patients, 1):
            already_sent = has_received_birthday_this_year(p['folder_number'], p['primary_mobile'], now.year)
            status_tag = "[ALREADY SENT THIS YEAR]" if already_sent else "[READY TO DISPATCH]"
            print(f"  {i:<3}. {p['full_name']:<24} | Folder: {p['folder_number']:<10} | Mobile: {p['primary_mobile']} | DOB: {p['dob']} {status_tag}")
        print("=" * 70)

    def dispatch_todays_birthdays(self) -> Dict[str, int]:
        now = datetime.now()
        patients = self.load_todays_birthday_patients()
        stats = {"total": len(patients), "sent": 0, "skipped_already_sent": 0, "failed": 0}
        
        logger.info(f"Dispatching birthday wishes for {len(patients)} patients on {now.strftime('%d %B %Y')}...")
        
        for p in patients:
            folder = p["folder_number"]
            mobile = p["primary_mobile"]
            name = p["full_name"]
            first_name = p["first_name"]
            
            if has_received_birthday_this_year(folder, mobile, now.year):
                logger.info(f"Skipped {name} ({mobile}) - Birthday message already sent for {now.year}.")
                stats["skipped_already_sent"] += 1
                continue
                
            sms_text = self.template.format(name=first_name, folder=folder)
            res = self.sms_service.send_sms(mobile, sms_text)
            status = res.get("status", "FAILED")
            
            if status in ("SENT", "DRY_RUN"):
                stats["sent"] += 1
                logger.info(f"[DISPATCHED] Birthday SMS sent to {name} ({mobile})")
            else:
                stats["failed"] += 1
                logger.error(f"[FAILED] Could not send birthday SMS to {name} ({mobile}): {res}")
                
            log_birthday_send(
                folder_number=folder,
                phone_number=mobile,
                name=name,
                year=now.year,
                msg=sms_text,
                status=status,
                resp=str(res)
            )
            time.sleep(0.5) # Gentle rate-limit
            
        logger.info(f"Birthday Dispatch Summary: Sent={stats['sent']}, AlreadySent={stats['skipped_already_sent']}, Failed={stats['failed']}")
        return stats

    def run_daily_daemon(self, target_hour: int = 8, target_minute: int = 0):
        """Runs continuously, triggering once every morning at 8:00 AM."""
        logger.info(f"UGDS Birthday Daemon active. Will dispatch daily at {target_hour:02d}:{target_minute:02d} AM.")
        last_dispatched_day = None
        
        try:
            while True:
                now = datetime.now()
                # Check if it's the target morning time and hasn't run today
                if now.hour == target_hour and now.minute >= target_minute and last_dispatched_day != now.date():
                    logger.info("Morning birthday trigger activated!")
                    self.dispatch_todays_birthdays()
                    last_dispatched_day = now.date()
                    
                time.sleep(30)
        except KeyboardInterrupt:
            logger.info("Birthday daemon stopped by user.")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="UGDS Automated Patient Birthday Engine")
    parser.add_argument("--preview", action="store_true", help="Preview patients celebrating birthdays today")
    parser.add_argument("--send", action="store_true", help="Dispatch birthday messages for today immediately")
    parser.add_argument("--daemon", action="store_true", help="Run background daemon (sends daily at 8:00 AM)")
    
    args = parser.parse_args()
    engine = BirthdayEngine()
    
    if args.send:
        engine.dispatch_todays_birthdays()
    elif args.daemon:
        engine.run_daily_daemon()
    else:
        engine.preview_today()

if __name__ == "__main__":
    main()
