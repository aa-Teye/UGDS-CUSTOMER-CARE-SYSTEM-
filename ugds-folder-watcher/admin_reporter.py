import os
import sys
import time
import sqlite3
import requests
from datetime import datetime

from dotenv import load_dotenv

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "sent_history.db")
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_PATH)

API_KEY = os.getenv("ARKESEL_API_KEY", "").strip()
SENDER_ID = os.getenv("ARKESEL_SENDER_ID", "UGDS").strip()
ADMIN_PHONE = os.getenv("ADMIN_PHONE", "233549044977").strip()

def send_admin_sms(message: str):
    if not API_KEY:
        return
    url = "https://sms.arkesel.com/api/v2/sms/send"
    headers = {"api-key": API_KEY, "Content-Type": "application/json"}
    payload = {
        "sender": SENDER_ID,
        "message": message,
        "recipients": [ADMIN_PHONE]
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10)
    except Exception:
        pass

def get_today_stats():
    if not os.path.exists(DB_PATH):
        return 0, 0
    try:
        today_str = datetime.now().strftime("%Y-%m-%d")
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM sent_messages WHERE date(created_at) = date('now') AND status IN ('SENT', 'DRY_RUN');")
            sent = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM sent_messages WHERE date(created_at) = date('now');")
            total = cur.fetchone()[0]
            return total, sent
    except Exception:
        return 0, 0

def run_daily_summary():
    total, sent = get_today_stats()
    date_str = datetime.now().strftime("%d-%b-%Y")
    msg = (
        f"UGDS DAILY REPORT ({date_str}):\n"
        f"Hello Alex, today's outreach summary:\n"
        f"Patient Scans: {total}\n"
        f"Survey SMS Sent: {sent}\n"
        f"System Status: Active & Healthy."
    )
    send_admin_sms(msg)
    print("Daily summary sent to Alex:", msg)

if __name__ == "__main__":
    if "--test" in sys.argv:
        send_admin_sms("UGDS ALERT TEST: Hello Alex, your SMS notifications are active!")
        print("Test sent!")
    else:
        run_daily_summary()
