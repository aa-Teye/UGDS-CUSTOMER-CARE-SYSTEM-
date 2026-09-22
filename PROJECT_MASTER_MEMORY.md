# UGDS Customer Care & Hospital Management System — Master Project Memory

> **IMPORTANT ARCHITECTURE DIRECTIVE**:
> Both frontend and backend are hosted on **VERCEL**. Render is completely deprecated/removed.
> Database: **Neon Postgres**.
> Hospital PC Integration: **`UGDS_SMS`** (Legacy eArchive watcher monitoring `C:\eArchive_Bible\Old_Bible`).

---

## 1. Cloud Infrastructure & Hosting
- **Frontend Repo / App**: `ugds-customer-experience` (React + Vite) ➔ Hosted on **Vercel** (`https://ugds-customer-experience.vercel.app`)
- **Backend Repo / API**: `ugds-backend` (FastAPI via ASGI serverless adapter in `api/index.py`) ➔ Hosted on **Vercel** (`vercel.json` with cron jobs)
- **Database**: **Neon Postgres** (Direct connection pooling)
- **SMS Gateway**: **Arkesel v2 API** (Sender ID: `UGDS`, Key: `anNXeFZuZUdlRmtnemZPY3NvVUY`)

---

## 2. On-Site Hospital PC Integration (`UGDS_SMS`)
- **Folder Location**: `C:\Users\<username>\Documents\UGDS_SMS`
- **Watch Target**: `C:\eArchive_Bible\Old_Bible`
- **Detection Mechanism**: Hourly `eDump_YYYY_MM_DD__HH_08_26.txt` differential parser.
  - Automatically compares the latest dump against the previous dump.
  - Extracts both brand-new registrations and returning patients whose folders were pulled/scanned in that hour.
  - Cleans Ghanaian mobile numbers (MTN `024/054/055/059`, Telecel `020/050`, AT `027/057/026`, Glo `028`).
  - Dispatches survey link: `https://ugds-customer-experience.vercel.app/survey`.
  - Duplicate prevention: SQLite ledger (`sent_history.db`) ensures max 1 SMS per 7 days per patient.
- **Autostart**: Configured in Windows Startup folder via `START_SILENT.vbs` and `ENABLE_AUTOSTART_ON_BOOT.bat`.
- **Status Checker**: `CHECK_STATUS.bat`.

---

## 3. Hospital 10-Day Migration Blueprint
- **Goal**: Full migration from legacy desktop eArchive (MySQL 5.0 on port 3307 / `eArchive_Bible_Server.exe`) to our modern cloud Hospital Management System within 10 days.
- **Source Data Captured**:
  - `C:\eArchive_Bible` (125,042 patient archive records in `eDump_*.txt`, historical logs, `eArchive_Bible.xlsm`)
  - `C:\TCL` (`eArchive.exe`, `Reporter.exe`)
  - MySQL 5.0 raw data files (`C:\Program Files (x86)\MySQL\MySQL Server 5.0\data`)
- **Core Entities to Map**:
  - `patients`: Folder number, Full name, Primary mobile, Area/Location, Date of birth (decoded from patient code, e.g., `YSINT12011964-1`), Next of kin.
  - `shelves`: Rack/Bay, Shelf/Level, Slot position (e.g. `MR-1B-A6-266`).
  - `folder_movements`: Check-out timestamp, staff handler, return status.
- **Automated Cloud Features**:
  - Automated patient birthday wishes via Vercel Cron (`0 8 * * *`).
  - Weekly executive SMS summary report to admin/Dean via Arkesel.
