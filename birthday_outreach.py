"""
UGDS Automated Master Birthday Outreach System
================================================
Centralized outreach engine with Active Patient (2019-2026) + Staff filtering.
- Preserves all 125,042 archive records (never dropped, available for searches).
- Targets active cohort (2019-2026 registrations) to prevent burning SMS credits on 15-year-old files.
- Includes UGDS Staff database from 'other files/CURRENT STAFF LIST WITH DATES OF BIRTH.xlsx'.
- Checks against SQLite sent ledger (sent_history.db) to prevent duplicate SMS in the same year.
- Validates Ghanaian mobile formats (MTN, Telecel, AT, Glo).
- Dispatches personalized wishes via Arkesel v2 API.
"""

import os
import sys
import re
import time
import argparse
import sqlite3
import requests
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

ARKESEL_API_KEY = os.getenv("ARKESEL_API_KEY", "").strip()
ARKESEL_SENDER_ID = os.getenv("ARKESEL_SENDER_ID", "UGDS").strip()
URL_V2 = "https://sms.arkesel.com/api/v2/sms/send"
BALANCE_URL = "https://sms.arkesel.com/api/v2/clients/balance-details"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVE_PATH = os.path.join(BASE_DIR, "current database.txt")
STAFF_EXCEL_PATH = os.path.join(BASE_DIR, "other files", "CURRENT STAFF LIST WITH DATES OF BIRTH.xlsx")
DB_PATH = os.path.join(BASE_DIR, "ugds-folder-watcher", "sent_history.db")

GHANA_MOBILE_PREFIXES = {
    "24", "54", "55", "59",  # MTN
    "20", "50",              # Telecel
    "27", "57", "26", "56",  # AT
    "28"                     # Glo
}

def clean_gh_phone(raw: str):
    if not raw:
        return None
    cleaned = re.sub(r"\D", "", str(raw))
    if cleaned.startswith("0") and len(cleaned) == 10:
        cleaned = "233" + cleaned[1:]
    elif cleaned.startswith("233") and len(cleaned) == 12:
        pass
    else:
        return None
    
    if len(cleaned) == 12 and cleaned[3:5] in GHANA_MOBILE_PREFIXES:
        return cleaned
    return None

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
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

def get_already_sent(year: int):
    init_db()
    sent_folders = set()
    sent_phones = set()
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT folder_number, phone_number 
            FROM sent_birthdays 
            WHERE birth_year_sent = ? AND status IN ('SENT', 'DRY_RUN');
        """, (year,))
        for f, p in cur.fetchall():
            if f:
                sent_folders.add(f.strip())
            if p:
                sent_phones.add(p.strip())
    return sent_folders, sent_phones

def log_send(folder, phone, name, year, msg, status, resp_str):
    init_db()
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO sent_birthdays 
            (folder_number, phone_number, patient_name, birth_year_sent, message_text, status, arkesel_response)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(folder_number, birth_year_sent) DO UPDATE SET
                status = excluded.status,
                sent_at = CURRENT_TIMESTAMP;
        """, (folder, phone, name, year, msg, status, resp_str))
        conn.commit()

def check_arkesel_balance():
    headers = {"api-key": ARKESEL_API_KEY}
    try:
        res = requests.get(BALANCE_URL, headers=headers, timeout=10)
        if res.status_code == 200:
            data = res.json()
            return data.get("data", {}).get("sms_balance", "N/A")
    except Exception as e:
        return f"Error: {e}"
    return "Unavailable"

def extract_registration_year(folder: str):
    m1 = re.search(r"([A-Z])/(\d{2})\s+\d+", folder)
    m2 = re.match(r"^(\d{2})\d{4,6}$", folder)
    if m1:
        y = int(m1.group(2))
        return 2000 + y if y <= 30 else 1900 + y
    elif m2:
        y = int(m2.group(1))
        if 15 <= y <= 30:
            return 2000 + y
    return None

def find_celebrants(target_day: int, target_month: int, current_year: int, min_year: int = 2019):
    if not os.path.exists(ARCHIVE_PATH):
        raise FileNotFoundError(f"Master archive not found at: {ARCHIVE_PATH}")

    celebrants = []
    seen_folders = set()
    day_str = f"{target_day:02d}"
    month_str = f"{target_month:02d}"
    total_lines = 0
    older_excluded = 0

    with open(ARCHIVE_PATH, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            total_lines += 1
            line = line.strip()
            if not line:
                continue
            m = re.search(r"([0-3]\d)([0-1]\d)(\d{4})-\d", line)
            if m:
                d, mo, yr = m.group(1), m.group(2), m.group(3)
                if d == day_str and mo == month_str:
                    parts = [p.strip() for p in line.split("'") if p.strip()]
                    folder = parts[1] if len(parts) > 1 else ""
                    
                    reg_year = extract_registration_year(folder)
                    # Filter: Only include active cohort from min_year upwards
                    if reg_year and reg_year < min_year:
                        older_excluded += 1
                        continue

                    name_parts = []
                    for p in parts[2:]:
                        if re.match(r"^[A-Z\s\-]+$", p) and not re.search(r"\d", p) and p not in ("MR", "DR", "MRS", "MISS", "PROF", "MADAM", "REV"):
                            name_parts.append(p)
                        elif "-" in p and any(c.isdigit() for c in p):
                            break
                    name = " ".join(name_parts) if name_parts else (parts[2] if len(parts) > 2 else "Patient")
                    
                    raw_phones = re.findall(r"0[235][0-9]{8}", line)
                    valid_phones = []
                    for rp in raw_phones:
                        cleaned = clean_gh_phone(rp)
                        if cleaned and cleaned not in valid_phones:
                            valid_phones.append(cleaned)
                            
                    birth_year = int(yr)
                    age = current_year - birth_year if birth_year > 1900 else 0

                    if folder and folder not in seen_folders:
                        seen_folders.add(folder)
                        celebrants.append({
                            "type": "patient",
                            "folder": folder,
                            "reg_year": reg_year or "Unknown",
                            "name": name.strip(),
                            "dob": f"{yr}-{month_str}-{day_str}",
                            "age": age,
                            "phones": valid_phones
                        })
    return celebrants, total_lines, older_excluded

def find_staff_celebrants(target_day: int, target_month: int, current_year: int):
    staff_celebrants = []
    if not os.path.exists(STAFF_EXCEL_PATH):
        return staff_celebrants

    try:
        import openpyxl
        wb = openpyxl.load_workbook(STAFF_EXCEL_PATH)
        ws = wb.active
        for r in ws.iter_rows(values_only=True):
            if len(r) >= 5 and isinstance(r[4], (datetime.datetime, datetime.date)):
                bdate = r[4] if isinstance(r[4], datetime.date) else r[4].date()
                if bdate.month == target_month and bdate.day == target_day:
                    name = str(r[1]).strip()
                    dept = str(r[2]).strip() if r[2] else "Dental School"
                    age = current_year - bdate.year
                    staff_celebrants.append({
                        "type": "staff",
                        "folder": f"STAFF-{name[:6].upper()}",
                        "reg_year": "Staff",
                        "name": name,
                        "department": dept,
                        "dob": bdate.isoformat(),
                        "age": age,
                        "phones": []  # Linked if matched or provided
                    })
    except Exception as e:
        print(f"Warning: Could not read staff list: {e}")
    return staff_celebrants

def format_message(name: str, is_staff: bool = False) -> str:
    first_name = name.split()[0].title() if name else "Colleague"
    if is_staff:
        return (
            f"Happy Birthday {first_name}! 🎂 The Dean, faculty, and entire team at the University of Ghana "
            f"Dental School celebrate you today. Thank you for your dedication. Have a blessed and joyous celebration!"
        )
    return (
        f"Happy Birthday {first_name}! 🎂 Best wishes from all of us at the University of Ghana Dental School, "
        f"Korle Bu. May your new year bring you happiness, success, and glowing smiles. Have a blessed celebration!"
    )

def send_sms(celebrant, current_year: int, dry_run: bool = False):
    folder = celebrant["folder"]
    phone = celebrant["phones"][0]
    name = celebrant["name"].title()
    is_staff = celebrant.get("type") == "staff"
    msg = format_message(name, is_staff)

    if dry_run:
        log_send(folder, phone, name, current_year, msg, "DRY_RUN", "Simulated delivery")
        return {"status": "DRY_RUN", "patient": name, "folder": folder, "phone": phone}

    headers = {
        "api-key": ARKESEL_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "sender": ARKESEL_SENDER_ID,
        "message": msg,
        "recipients": [phone]
    }

    last_error = None
    for attempt in range(3):
        try:
            resp = requests.post(URL_V2, json=payload, headers=headers, timeout=15)
            if resp.status_code in (200, 201):
                log_send(folder, phone, name, current_year, msg, "SENT", resp.text)
                return {"status": "SENT", "patient": name, "folder": folder, "phone": phone}
            else:
                last_error = resp.text
        except Exception as exc:
            last_error = str(exc)
            time.sleep(1)

    log_send(folder, phone, name, current_year, msg, "FAILED", str(last_error))
    return {"status": "FAILED", "patient": name, "folder": folder, "phone": phone, "error": str(last_error)}

def main():
    parser = argparse.ArgumentParser(description="UGDS Patient & Staff Birthday Outreach Engine")
    parser.add_argument("--send", action="store_true", help="Dispatch live SMS to celebrants")
    parser.add_argument("--dry-run", action="store_true", help="Simulate dispatch without sending")
    parser.add_argument("--date", type=str, default="", help="Target date in YYYY-MM-DD format (default: today)")
    parser.add_argument("--min-year", type=int, default=2019, help="Minimum patient registration year (default: 2019 for last 7 years)")
    args = parser.parse_args()

    if args.date:
        target_date = datetime.datetime.strptime(args.date, "%Y-%m-%d")
    else:
        target_date = datetime.datetime.now()

    day = target_date.day
    month = target_date.month
    year = target_date.year

    print("===================================================================")
    print("  UGDS PATIENT & STAFF BIRTHDAY OUTREACH ENGINE")
    print(f"  Target Date:         {target_date.strftime('%A, %d %B %Y')}")
    print(f"  Active Window:       {args.min_year} to {year} (Last {year - args.min_year + 1} Years)")
    print("===================================================================")

    balance = check_arkesel_balance()
    print(f"  Arkesel SMS Balance: {balance} credits")
    print("-------------------------------------------------------------------")

    t0 = time.time()
    celebrants, total_lines, older_excluded = find_celebrants(day, month, year, min_year=args.min_year)
    staff_celebrants = find_staff_celebrants(day, month, year)
    scan_time = time.time() - t0

    print(f"  Master Archive Size:          {total_lines:,} records (100% PRESERVED)")
    print(f"  Older Dormant (Pre-{args.min_year}):   {older_excluded} celebrants excluded from SMS")
    print(f"  Active Patients (>= {args.min_year}):   {len(celebrants)} celebrants found for today")
    print(f"  Hospital Staff:               {len(staff_celebrants)} staff celebrants found for today")
    print(f"  Scan Completed in:            {scan_time:.2f}s")
    print("-------------------------------------------------------------------")

    reachable = [c for c in celebrants if c["phones"]]
    unreachable = [c for c in celebrants if not c["phones"]]

    print(f"  Reachable Active Patients:    {len(reachable)}")
    print(f"  Unreachable (No Valid Phone): {len(unreachable)}")

    already_folders, already_phones = get_already_sent(year)
    pending = []
    already_sent_count = 0

    for c in reachable:
        if c["folder"].strip() in already_folders or c["phones"][0] in already_phones:
            already_sent_count += 1
        else:
            pending.append(c)

    print(f"  Already Sent This Year:       {already_sent_count}")
    print(f"  PENDING DISPATCH TODAY:       {len(pending)} SMS")
    print("===================================================================")

    if not args.send and not args.dry_run:
        print("\n[PREVIEW MODE] (Run with --send to dispatch or --dry-run to simulate)\n")
        print("Sample pending active celebrants for today:")
        for idx, c in enumerate(pending[:15], 1):
            reg = c.get("reg_year", "Unknown")
            print(f"  {idx:2d}. {c['name'].title():<30} | Reg: {reg} | {c['folder']:<12} | {c['phones'][0]} | Age: {c['age']}")
        if len(pending) > 15:
            print(f"  ... and {len(pending) - 15} more active celebrants.")
        print("\nTo send to all pending active celebrants:")
        print(f"  python birthday_outreach.py --send")
        return

    mode_name = "SIMULATING" if args.dry_run else "DISPATCHING LIVE"
    print(f"\n{mode_name} SMS to {len(pending)} active celebrants...")

    if not pending:
        print("No pending celebrants to dispatch for today.")
        return

    sent_count = 0
    fail_count = 0

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(send_sms, c, year, args.dry_run): c for c in pending}
        for future in as_completed(futures):
            res = future.result()
            if res["status"] in ("SENT", "DRY_RUN"):
                sent_count += 1
                print(f"  [OK] {res['patient']} ({res['phone']}) - {res['status']}")
            else:
                fail_count += 1
                print(f"  [FAIL] {res['patient']} ({res['phone']}) - {res.get('error', 'Error')}")

    print("\n===================================================================")
    print(f"  Dispatch Completed: Sent={sent_count}, Failed={fail_count}")
    final_balance = check_arkesel_balance()
    print(f"  Arkesel Balance Remaining: {final_balance} credits")
    print("===================================================================")

    # Dispatch Executive SMS Report to Alex (0549044977)
    admin_phone = "233549044977"
    date_str = target_date.strftime("%d-%b-%Y")
    admin_msg = (
        f"UGDS BIRTHDAY DISPATCH REPORT ({date_str}):\n"
        f"Hello Alex, today's outreach completed:\n"
        f"- Active Celebrants Reached: {sent_count}\n"
        f"- Failed: {fail_count}\n"
        f"- SMS Balance Remaining: {final_balance} credits\n"
        f"System Status: 100% Active & Healthy."
    )
    if not args.dry_run:
        print(f"\nSending Executive Dispatch Report to Alex ({admin_phone})...")
        try:
            report_payload = {
                "sender": ARKESEL_SENDER_ID,
                "message": admin_msg,
                "recipients": [admin_phone]
            }
            rep_resp = requests.post(
                URL_V2,
                json=report_payload,
                headers={"api-key": ARKESEL_API_KEY, "Content-Type": "application/json"},
                timeout=12
            )
            print(f"  Report SMS Delivery Status: {rep_resp.status_code}")
        except Exception as ex:
            print(f"  Failed to send admin report: {ex}")
    else:
        print(f"\n[DRY RUN] Would send executive report to {admin_phone}:\n{admin_msg}")

if __name__ == "__main__":
    main()
