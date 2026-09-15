"""
SQLite Database manager to track SMS sends and prevent duplicate messages.
"""

import sqlite3
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import sys


if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, "sent_history.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes SQLite tables if they do not exist."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sent_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                folder_number TEXT,
                phone_number TEXT NOT NULL,
                patient_name TEXT,
                message_text TEXT,
                status TEXT NOT NULL,  -- 'SENT', 'FAILED', 'DRY_RUN', 'SKIPPED'
                arkesel_response TEXT,
                source_file TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_folder_phone 
            ON sent_messages (folder_number, phone_number, created_at);
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS processed_files (
                file_path TEXT PRIMARY KEY,
                last_modified REAL,
                last_line_read INTEGER DEFAULT 0,
                processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()

def is_recently_sent(
    folder_number: str,
    phone_number: str,
    max_per_week: int = 1
) -> bool:
    """
    Checks if this patient has received an SMS in the last 7 days.
    Allows at most 'max_per_week' (default: 1) SMS per patient per week.
    """

    seven_days_ago = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM sent_messages
            WHERE (folder_number = ? OR phone_number = ?)
              AND status IN ('SENT', 'DRY_RUN')
              AND created_at >= ?;
        """, (folder_number, phone_number, seven_days_ago))
        count = cursor.fetchone()[0]
        return count >= max_per_week



def log_message(
    folder_number: str,
    phone_number: str,
    patient_name: str,
    message_text: str,
    status: str,
    arkesel_response: str = "",
    source_file: str = ""
):
    """Logs a sent/attempted SMS into the ledger."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO sent_messages 
            (folder_number, phone_number, patient_name, message_text, status, arkesel_response, source_file)
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """, (folder_number, phone_number, patient_name, message_text, status, arkesel_response, source_file))
        conn.commit()

def get_file_checkpoint(file_path: str) -> Dict[str, Any]:
    """Retrieves file processing progress (for streaming/tailing appended files)."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT last_modified, last_line_read FROM processed_files WHERE file_path = ?", (file_path,))
        row = cursor.fetchone()
        if row:
            return {"last_modified": row["last_modified"], "last_line_read": row["last_line_read"]}
        return {"last_modified": 0.0, "last_line_read": 0}

def update_file_checkpoint(file_path: str, last_modified: float, last_line_read: int):
    """Updates progress on a processed tracker file."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO processed_files (file_path, last_modified, last_line_read, processed_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(file_path) DO UPDATE SET
                last_modified = excluded.last_modified,
                last_line_read = excluded.last_line_read,
                processed_at = CURRENT_TIMESTAMP;
        """, (file_path, last_modified, last_line_read))
        conn.commit()

# Run init on import
init_db()
