"""
eArchiver MySQL Database Discovery & Auto-Configuration Tool.
Connects to localhost:3307 (or specified host), discovers tables,
and identifies the patient and movement tables.
"""

import os
import sys
import json
import pymysql
from typing import List, Dict, Any, Optional

COMMON_PASSWORDS = ["", "root", "admin", "123456", "1234", "mysql", "earchiver", "earchive"]

def find_working_connection(host="127.0.0.1", port=3307, user="root") -> Optional[pymysql.Connection]:
    print("=" * 65)
    print("  eArchiver MySQL Auto-Discovery Tool")
    print(f"  Target: {host}:{port} | User: {user}")
    print("=" * 65)
    
    for pwd in COMMON_PASSWORDS:
        pwd_display = "(empty)" if pwd == "" else f"'{pwd}'"
        try:
            conn = pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=pwd,
                connect_timeout=3
            )
            print(f"[SUCCESS] Connected to MySQL with password: {pwd_display}!")
            return conn
        except pymysql.MySQLError as e:
            # 1045: Access denied
            if e.args[0] == 1045:
                continue
            else:
                print(f"[NOTICE] Connection note with {pwd_display}: {e.args[1] if len(e.args) > 1 else e}")
    
    # If standard passwords failed, prompt
    print("\n[!] Standard passwords did not match.")
    custom_pwd = input("Please enter the MySQL root password (press Enter for none): ").strip()
    try:
        conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=custom_pwd,
            connect_timeout=5
        )
        print("[SUCCESS] Connected successfully with entered password!")
        return conn
    except Exception as e:
        print(f"[ERROR] Could not connect: {e}")
        return None


def inspect_databases(conn: pymysql.Connection):
    with conn.cursor() as cursor:
        cursor.execute("SHOW DATABASES;")
        dbs = [row[0] for row in cursor.fetchall()]
    
    system_dbs = {"information_schema", "mysql", "performance_schema", "sys"}
    user_dbs = [d for d in dbs if d.lower() not in system_dbs]
    
    print("\n--- Available Databases ---")
    for d in user_dbs:
        print(f"  * {d}")
    
    if not user_dbs:
        print("No user databases found. (Only system databases exist).")
        return None
    
    # Pick the most likely candidate (earchive, earchiver, hospital, etc.)
    target_db = user_dbs[0]
    for d in user_dbs:
        if any(k in d.lower() for k in ["earch", "archive", "patient", "dental", "ugds", "record"]):
            target_db = d
            break
            
    print(f"\nTarget Database identified: [{target_db}]")
    conn.select_db(target_db)
    
    with conn.cursor() as cursor:
        cursor.execute("SHOW TABLES;")
        tables = [row[0] for row in cursor.fetchall()]
        
    print(f"\n--- Tables in '{target_db}' ({len(tables)} tables) ---")
    for t in tables:
        # Get row count
        try:
            cursor.execute(f"SELECT COUNT(*) FROM `{t}`;")
            count = cursor.fetchone()[0]
            print(f"  * {t:<30} ({count:,} rows)")
        except Exception:
            print(f"  * {t:<30}")
            
    # Inspect columns in each table
    print("\n--- Scanning Schema for Patient & Scan Fields ---")
    candidate_patient_table = None
    candidate_movement_table = None
    
    for t in tables:
        try:
            cursor.execute(f"DESCRIBE `{t}`;")
            columns = [row[0] for row in cursor.fetchall()]
            cols_lower = [c.lower() for c in columns]
            
            # Check for patient indicators
            has_phone = any(any(k in c for k in ["phone", "tel", "mobile", "contact"]) for c in cols_lower)
            has_folder = any(any(k in c for k in ["folder", "fld", "card", "rec"]) for c in cols_lower)
            has_name = any(any(k in c for k in ["name", "fname", "sname"]) for c in cols_lower)
            
            # Check for movement/scan indicators
            has_time = any(any(k in c for k in ["time", "date", "created", "scanned", "out"]) for c in cols_lower)
            has_status = any(any(k in c for k in ["status", "state", "movement", "action"]) for c in cols_lower)
            
            if has_folder and has_phone and has_name:
                print(f"  [+] Patient Directory Candidate: `{t}` -> Columns: {columns[:6]}")
                if not candidate_patient_table:
                    candidate_patient_table = t
            elif has_folder and (has_time or has_status):
                print(f"  [+] Live Scans / Movements Candidate: `{t}` -> Columns: {columns[:6]}")
                if not candidate_movement_table:
                    candidate_movement_table = t
        except Exception as e:
            pass
            
    return {
        "database": target_db,
        "patient_table": candidate_patient_table,
        "movement_table": candidate_movement_table
    }


def save_to_env(results: Dict[str, Any], host: str, port: int, user: str, password: str):
    env_file = os.path.join(os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else os.path.dirname(os.path.abspath(__file__)), ".env")
    
    # Read existing lines if any
    existing_lines = []
    if os.path.exists(env_file):
        with open(env_file, "r", encoding="utf-8") as f:
            existing_lines = f.readlines()
            
    # Filter out existing MYSQL_ keys
    filtered = [l for l in existing_lines if not l.strip().startswith("MYSQL_")]
    
    # Append fresh MySQL settings
    mysql_block = [
        "\n# --- Live MySQL Database Configuration ---\n",
        f"MYSQL_HOST={host}\n",
        f"MYSQL_PORT={port}\n",
        f"MYSQL_USER={user}\n",
        f"MYSQL_PASSWORD={password}\n",
        f"MYSQL_DATABASE={results.get('database', '')}\n",
        f"MYSQL_PATIENT_TABLE={results.get('patient_table', '')}\n",
        f"MYSQL_MOVEMENT_TABLE={results.get('movement_table', '')}\n",
    ]
    
    with open(env_file, "w", encoding="utf-8") as f:
        f.writelines(filtered + mysql_block)
        
    print(f"\n[AUTO-SAVED] MySQL settings successfully written to: {env_file}")


def main():
    host = os.getenv("MYSQL_HOST", "127.0.0.1")
    port = int(os.getenv("MYSQL_PORT", "3307"))
    user = os.getenv("MYSQL_USER", "root")
    
    conn = find_working_connection(host=host, port=port, user=user)
    if not conn:
        print("\nDiscovery aborted: Could not connect to MySQL.")
        input("Press Enter to exit...")
        sys.exit(1)
        
    try:
        results = inspect_databases(conn)
        print("\n" + "=" * 65)
        print("  DISCOVERY SUMMARY")
        print("=" * 65)
        print(f"  Database:        {results.get('database')}")
        print(f"  Patient Table:   {results.get('patient_table')}")
        print(f"  Movement Table:  {results.get('movement_table')}")
        print("=" * 65)
        
        # Auto-save
        save_to_env(results, host=host, port=port, user=user, password=conn.password if hasattr(conn, 'password') else "")
    finally:
        conn.close()
        
    print("\nSetup complete! You can now double-click 'START_MYSQL_WATCHER' to begin live monitoring.")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()

