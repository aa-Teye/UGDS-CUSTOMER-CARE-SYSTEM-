import sqlite3
import os

dbs = [
    'ugds-folder-watcher/sent_history.db',
    'ugds-backend/ugds_dev.db',
    'ugds-backend/test.db'
]

for db in dbs:
    if os.path.exists(db):
        print(f"=== {db} ===")
        conn = sqlite3.connect(db)
        tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        for t in tables:
            tname = t[0]
            cnt = conn.execute(f"SELECT count(*) FROM [{tname}]").fetchone()[0]
            print(f"  Table '{tname}': {cnt} rows")
            if 'sent' in tname.lower() or 'visit' in tname.lower() or 'patient' in tname.lower() or 'log' in tname.lower():
                sample = conn.execute(f"SELECT * FROM [{tname}] LIMIT 3").fetchall()
                print(f"    Sample: {sample}")
        conn.close()
