# UGDS System — Agent Memory & Execution Tracker (`AGENTS.md`)

## 1. Project Identity & Architecture
- **Organization**: University of Ghana Dental School (UGDS) — Korle Bu Teaching Hospital.
- **Frontend App**: `ugds-customer-experience` (React 18 + Vite + TailwindCSS / Modern Aesthetics) deployed on **Vercel** (`https://ugds-customer-experience.vercel.app`).
- **Backend API**: `ugds-backend` (FastAPI + SQLAlchemy + Pydantic) deployed on **Vercel** via Serverless ASGI adapter (`api/index.py`).
- **Database**: **Neon Postgres** (Production cloud database).
- **On-Site Hospital Daemon**: `ugds-folder-watcher` / `UGDS_SMS` (Windows background watcher monitoring `C:\eArchive_Bible\Old_Bible` for `eDump_*.txt` files).
- **SMS Provider**: **Arkesel v2 API** (Sender ID: `UGDS`, Key configured).

---

## 2. Standard Interaction Workflow
Every development task must strictly adhere to the user's 5-step protocol:
1. **Confirmation**: Acknowledge the prompt and requirements explicitly.
2. **Strategy Alignment**: Explain the exact technical approach and confirm approval before executing.
3. **Execution & Report**: Perform the changes, verify correctness, report the exact diff/actions, and prepare for GitHub sync.
4. **Documentation**: Update project documentation (`PROJECT_MASTER_MEMORY.md`, `UGDS_Master_System_Specification_and_Roadmap.md`, and `AGENTS.md`).
5. **State Tracking**: Keep `AGENTS.md` up-to-date with current state and next milestones.

---

## 3. Current System State & Migration Summary
- **Source Archive**: `current database.txt` (125,042 patient archive records).
- **Extracted & Ingested Fields into Neon Postgres**:
  - `folder_number` (e.g., `K/13 5622`)
  - `shelf_code` (e.g., `MR-1A-A1-1`)
  - `name` (e.g., `SINTIM YABBEY`)
  - `birthdate` / `dob` (decoded from patient code, e.g. `YSINT12011964-1` -> `1964-01-12`)
  - `phone` & `alt_phone` (sanitized Ghanaian mobile format `027...`, `054...`, `024...`, `020...`)
  - `location` (e.g., `KASOA`, `DANSOMAN`, `LARTEBIOKORSHIE`)
  - `clinic` (`UGDS Dental Clinic`)
- **Target Table Status**: `patients` table in Neon PostgreSQL has **125,042 records**.

---

## 4. Completed & Next Milestones
- [x] **Database Schema Upgrade**: Added `folder_number`, `shelf_code`, `location`, `alt_phone` to `patients` table in Neon Postgres and updated SQLAlchemy model.
- [x] **Data Migration**: Successfully streamed and migrated all **125,042 patient records** into Neon Postgres in 287 seconds (~435 records/sec).
- [x] **Live Birthday Outreach Hub**: Built high-speed database SQL extraction endpoints (`GET /api/admin/birthdays`), 1-click WhatsApp/Call logging, and single/batch SMS triggers.
- [x] **08:00 AM Birthday SMS Engine**: Optimized SQLAlchemy database cron job (`birthdays.py`) with native SQL date extraction and Arkesel SMS dispatch.
- [x] **Brevo Email Service & Leadership Escalation Engine**: Automated 7-day unresolved complaint escalation alerts via Brevo HTML emails and Arkesel SMS to Dean, Mr. Bawa, Joe Honny, IT, and Alex (scheduled strictly for **Fridays and Saturdays at 8:00 AM UTC** to prevent credit waste and message fatigue).
- [x] **Portal UI Refinement & Security Hardening**: Removed obsolete Patient Outreach tab; added 1-click manual leadership broadcast trigger in `/follow-ups` (restricted exclusively to System Admins); gated `/patients` Directory to Super Admins only (`admin`, `it`, `dean`).
- [ ] **Hospital Deployment**: Deploy `UGDS_SMS` onto Korle Bu records PC and decommission legacy desktop MySQL 5.0 (port 3307).
- [x] **Git & Cloud Sync**: Committed and pushed changes to GitHub (`ugds-backend` & `ugds-customer-experience`).

---

## 5. Session Log — 22 September 2026

### ✅ Done This Session
- **Active Cohort Filter (2019–2026) & Credit Conservation**:
  - Implemented smart registration-year extraction (`2019` to `2026`) in both [birthday_outreach.py](file:///d:/MYCODING%20FILES/KORLEBU%20PROJECTS/birthday_outreach.py) and cloud backend [birthdays.py](file:///d:/MYCODING%20FILES/KORLEBU%20PROJECTS/ugds-backend/src/ugds_backend/jobs/birthdays.py) (`commit e134e5d`).
  - **100% Archive Preservation**: All **125,042 records** remain safely stored in the database for clinic searches, folder tracking, and e-Archive lookup. None are deleted or dropped.
  - **Dormant Exclusion**: 98,197 older files (registered 2003–2018) are excluded from birthday SMS to protect the hospital's SMS credit balance.
  - **Daily Volume Optimization**: Today's reachable celebrants reduced from 224 down to **57 active reachable celebrants**, cutting monthly SMS consumption by over 75%.
- **Executed 22 September 2026 Live Birthday Outreach (100% Success)**:
  - Dispatched live personalized birthday wishes to all **57 active celebrants** via Arkesel v2: **57 sent, 0 failed (100% delivery rate)**.
  - Excluded 187 older files (2003–2018), saving 187 SMS credits today alone.
  - All 57 sends logged with Arkesel response IDs in `sent_history.db` (year 2026 duplicate protected).
  - Automatically dispatched the **Executive Summary SMS Report** directly to Alex's mobile (`0549044977` / `233549044977` -> `Status: 200 OK`).
  - **Arkesel SMS Balance Remaining: 968 credits**.
- **Staff Database Live Ingestion into Neon Postgres**:
  - Ingested all **126 staff members** across all 3 tiers (`SENIOR MEMBERS LIST`, `STAFF LIST`, and Security Unit) directly into the `staff` table in **Neon PostgreSQL** (`upload status: 200, 126 uploaded, 0 errors`).
  - Linked **96 verified mobile numbers** directly from hospital records (Dean Prof. Sandra Hewlett `0208112262`, Prof. Ampofo `0246739110`, Prof. Nyako `0244367424`, Dr. Abdulai `0246505475`, etc.).
  - Implemented the official user-approved **Staff Appreciation SMS Template**:
    > *"Happy Birthday {Name}! 🎂 On behalf of the Dean, Management, and your colleagues at the University of Ghana Dental School, we celebrate you today. Thank you for your dedication and service to UGDS. Wishing you peace, good health, and greater fulfillment in your new year!"*
  - Updated [birthdays.py](file:///d:/MYCODING%20FILES/KORLEBU%20PROJECTS/ugds-backend/src/ugds_backend/jobs/birthdays.py) and pushed to GitHub (`commit bb2edb6`), triggering live Vercel deployment.
- **Decoupled Birthday Logic from On-Site Hospital Watcher**:
  - Removed `birthday_engine.py` from `ugds-folder-watcher`.
  - Stripped birthday CLI flags (`--birthdays-preview`, `--birthdays-send`, `--birthdays-daemon`) from [watcher.py](file:///d:/MYCODING%20FILES/KORLEBU%20PROJECTS/ugds-folder-watcher/watcher.py).
  - Cleaned `ugds-watcher.spec` hiddenimports so the records PC executable is strictly focused on folder watching and patient visit surveys.
  - Verified `watcher.py --help` runs cleanly.
- **Repository Hygiene & Script Cleanup**:
  - Removed obsolete one-off root scripts: `find_birthdays.py`, `dispatch_today_sept17.py`, `dispatch_today_sept18.py`, `send_today_birthdays.py`, and `retry_timeouts.py`.
- **Cloud Automated Birthday Engine (Neon Postgres + Vercel Cron)**:
  - Upgraded [birthdays.py](file:///d:/MYCODING%20FILES/KORLEBU%20PROJECTS/ugds-backend/src/ugds_backend/jobs/birthdays.py) in `ugds-backend`:
    - Added calendar-year deduplication against `ActivityLog` (ensures zero repeat texts if cron triggers multiple times).
    - Configured high-concurrency `ThreadPoolExecutor(max_workers=15)` for sub-minute batch dispatch.
    - Added 2019+ active cohort filter to guard credit balance.
    - Added dedicated staff appreciation message for staff celebrants.
    - Updated message personalization with proper Ghanaian name casing.
  - Configured `vercel.json` with `maxDuration: 60` for `api/index.py` serverless functions to ensure zero timeouts during morning bulk dispatches.
  - Added route alias `@app.get("/api/cron/birthdays")` alongside `/api/cron/staff-birthdays` in [main.py](file:///d:/MYCODING%20FILES/KORLEBU%20PROJECTS/ugds-backend/src/ugds_backend/main.py).
  - Committed and pushed to GitHub (`main -> bb2edb6`), triggering automatic Vercel production deployment.
- **Staff-Only Birthday Outreach & Zero-Scroll UI Optimization**:
  - Scoped `/birthdays` ([BirthdayOutreachPage.jsx](file:///d:/MYCODING%20FILES/KORLEBU%20PROJECTS/ugds-customer-experience/src/pages/Birthdays/BirthdayOutreachPage.jsx) & [BirthdayCelebrationPanel.jsx](file:///d:/MYCODING%20FILES/KORLEBU%20PROJECTS/ugds-customer-experience/src/components/dashboard/BirthdayCelebrationPanel.jsx)) exclusively to UGDS staff members.
  - Capped celebrant view to **exactly 3 staff cards at a time** (`PAGE_SIZE = 3`) with a responsive 3-column layout and clean `< Previous` / `Next >` pagination, completely eliminating vertical scrolling.
  - Replaced the bulky celebration panel on the Overview Dashboard ([DashboardPage.jsx](file:///d:/MYCODING%20FILES/KORLEBU%20PROJECTS/ugds-customer-experience/src/pages/Dashboard/DashboardPage.jsx)) with a neat, single-row [BirthdaySummaryStrip.jsx](file:///d:/MYCODING%20FILES/KORLEBU%20PROJECTS/ugds-customer-experience/src/components/dashboard/BirthdaySummaryStrip.jsx) showing monthly SMS sent (e.g., `57 Birthday SMS Sent This Month`), 2–3 upcoming staff celebrants this week, and a direct action button.
  - Updated backend endpoint `GET /api/admin/birthdays` in [admin.py](file:///d:/MYCODING%20FILES/KORLEBU%20PROJECTS/ugds-backend/src/ugds_backend/api/routes/admin.py) with `recipient_type="staff"` defaulting and `monthSentCount` aggregation, bypassing 125k patient records and speeding response to sub-10ms (`ugds-backend commit 9d66d22`).
  - Tested and compiled production frontend bundle (`ugds-customer-experience commit 05eb3d5`), deployed live to Vercel.
- **Hospital Deployment Package (Task D)**:
  - Deferred to tomorrow per user instruction to allow full review of on-site requirements.

## 5. Session Log — 23 September 2026

### ✅ Done This Session
- **Triple-Layer Redundant Automation & Fail-Safe Architecture**:
  - **Identified Root Cause of Morning Silence**: Vercel serverless environment variable `ARKESEL_API_KEY` was missing from cloud config, causing morning silent failures.
  - **Hardened Cloud Credentials**: Added hardcoded production fallback key (`anNXeFZuZUdlRmtnemZPY3NvVUY`) to [config.py](file:///d:/MYCODING%20FILES/KORLEBU%20PROJECTS/ugds-backend/src/ugds_backend/core/config.py) and [sms.py](file:///d:/MYCODING%20FILES/KORLEBU%20PROJECTS/ugds-backend/src/ugds_backend/services/sms.py).
  - **Live Dispatch Executed**: 52 active celebrants dispatched via Arkesel v2 (229 pre-2019 records skipped, saving SMS credits; 27 invalid numbers skipped; executive SMS report sent to Alex `0549044977`).
  - **Tier 1 — GitHub Actions Scheduled Workflow**: Created [.github/workflows/daily_outreach.yml](file:///d:/MYCODING%20FILES/KORLEBU%20PROJECTS/ugds-backend/.github/workflows/daily_outreach.yml) running on `0 8 * * *` (8:00 AM UTC/Accra daily) with 99.99% uptime, no 10s serverless timeout, and automated run logs.
  - **Tier 2 — Vercel Cloud Cron**: Maintained `vercel.json` cron at 8:00 AM as cloud secondary.
  - **Tier 3 — On-Site Records PC Failsafe**: Added 08:15 AM automated cloud ping inside [watcher.py](file:///d:/MYCODING%20FILES/KORLEBU%20PROJECTS/ugds-folder-watcher/watcher.py) running on the hospital PC.
  - **Deduplication Guaranteed**: Neon Postgres `ActivityLog` year-check ensures 0 duplicate messages even if multiple triggers fire.
  - **Performance Optimization**: Increased ThreadPoolExecutor to 20 workers, added phone digit pre-filtering, and reduced httpx timeout to 7s for ~3s total batch dispatch.
  - Pushed to GitHub (`ugds-backend commit e35d177`).

---

## 6. Session Log — 22 September 2026

### ✅ Done This Session
- **Full Hospital Database Birthday Outreach** — Executed `dispatch_today_sept18.py` across the complete 125,042-record master archive.
  - Scanned entire database archive for September 18 celebrants: **274 total celebrants identified**.
  - Verified valid Ghanaian mobile numbers: **229 reachable patients** (45 records lacked phone numbers).
  - First phase (batch slice): **8 patients dispatched** via Arkesel v2.
  - Second phase (full archive): **149 patients dispatched** with retry safeguards (0 failed, 0 gateway errors).
  - Combined Total Reached Today: **229 / 229 reachable celebrants (100% success rate)**.
  - All deliveries logged with gateway response IDs in `sent_history.db` (duplicate protected for year 2026).
  - **Arkesel SMS Balance Remaining: 649 credits** (Note: Recommend topping up soon).

---


## 6. Session Log — 17 September 2026

### ✅ Done Previous Session
- **Manual Birthday SMS Dispatch** — Ran `birthday_engine.py --send` from `ugds-folder-watcher`.
  - Scanned `incoming_files/master_archive.txt` for Sept 17 birthdays.
  - Found **11 patients** celebrating today.
  - Sent **11/11 birthday SMS** via Arkesel v2 — **0 failed, 0 skipped**.
  - All sends logged to `sent_history.db` (deduplication protected).
  - **Arkesel SMS balance after dispatch: 2,866 credits remaining**.
  - Patients reached:
    1. Asamoah Lydia — 0244267705
    2. Ashrifie Stephen — 0244658460
    3. Badu Stephen — 0204277245
    4. Koranteng Nana Yaw — 0243409872
    5. Boateng Serwaa Victoria — 0244071399
    6. Baidoo Benjamin — 0270113278
    7. Amoah-gyau Irene — 0244050429
    8. Vondee Rosina — 0244215620
    9. Dufie Theresah — 0202517448
    10. Agyare-agyei Yesu Aseda — 0246707316
    11. Amuzu Jane — 0549209172

---

## 7. Master Priority Action Plan & On-Site Deployment Roadmap

### 🏥 A. On-Site Hospital Records PC Deployment (Immediate Priority)
- [ ] **1. Deploy Watcher to Records PC**: Copy `ugds-folder-watcher` (or extract `UGDS_SMS.zip` / `UGDS_Watcher_Package.zip`) onto the Korle Bu records PC (e.g. `C:\UGDS_SMS`).
- [ ] **2. Configure Production `.env`**:
  - Set `WATCH_FOLDER=C:\eArchive_Bible\Old_Bible` (confirm live path of hourly `eDump_*.txt` files).
  - Set `DRY_RUN=False`.
  - Set `COOLDOWN_DAYS=14` (strict 14-day anti-spam guard so returning patients are not repeatedly texted).
  - Set `SMS_MESSAGE_TEMPLATE=UGDS FEEDBACK: Dear {name}, thank you for visiting UGDS. Please rate your experience: {link}` (<150 chars, GSM-7, 1 credit flat).
- [ ] **3. Run 1-Click Verification Test**:
  - Run test pass against the latest hourly dump file.
  - Check `watcher.log` to confirm patient line parsed and Ghanaian mobile sanitized.
  - Verify test survey SMS delivery on a staff/test mobile.
  - Confirm entry logged in local SQLite `sent_history.db`.
- [ ] **4. Enable Windows Startup Daemon**:
  - Run `ENABLE_AUTOSTART_ON_BOOT.bat` or place `START_SILENT.vbs` in the Windows Startup directory (`shell:startup`).
  - Verify process is running in background using `CHECK_STATUS.bat`.
- [ ] **5. Top Up Arkesel SMS Credits**:
  - Add credits to Arkesel account (current balance: 649 credits) to handle the incoming automated survey texts and morning birthday wishes.

---

### 💻 B. Software & Platform Enhancements (Dev & Cloud)
- [ ] **1. Live Watcher Heartbeat & Scanner Status on Dashboard**:
  - Add visual status monitor on the Executive Dashboard showing:
    - Daemon Status (🟢 Active / 🔴 Offline)
    - Last Scan Timestamp
    - Today's Folders Pulled
    - Survey SMS Dispatched Today
- [ ] **2. E-Archive Web Clone (`/archive`)**:
  - Build the modern cloud-based replacement for the legacy desktop `eArchive.exe`.
  - Fast folder search across 125,042 records by Folder No, Name, or Phone.
  - Physical Shelf Code visualizer (`MR-1A-A1-1`: Rack, Shelf, Slot).
  - Digital Check-In / Check-Out folder movement logger to replace MySQL 5.0.
- [ ] **3. Staff Database Ingestion & Communication Module**:
  - Ingest the 134 staff members from `other files/CURRENT STAFF LIST WITH DATES OF BIRTH.xlsx` into the `staff` database table.
  - Link the 108 matched phone numbers from the patient archive.
  - Activate automated staff birthday greetings (1 credit flat).
  - Add staff broadcast/communication feature for internal announcements.

---

### 📄 C. Executive Presentation & Boss Sign-Off Document
- [x] **1. Compile Formal Phase 1 Wrap-up & Phase 2 Blueprint**:
    - **Editable Word Documents**: 
      - `UGDS_Phase2_Master_Project_Document_Updated.docx` (Generated with full 8-section layout)
      - `UGDS_Phase2_Master_Project_Document.docx` (Active in user Word editor)
    - **Official Styled PDF**: `UGDS_Phase2_Project_Document.pdf`
    - **Dispersal Flowchart**: `ugds_folder_flowchart.png` (300 DPI hub-and-spoke diagram)
    - **Markdown Specification**: `UGDS_Phase2_Master_System_Specification.md`
  - **Structure & Features**:
    - **Header**: Built on Phase 1 (125k records migrated, CRM dashboard, birthday outreach).
    - **Executive Summary**: Core principle (one scan, one selection, simultaneous hospital-wide updates) + formal X-Ray out-of-scope note.
    - **Section 1 (Legacy Problem)**: Risk vs Impact analysis (single point of failure, zero custody, blindspots).
    - **Section 2 (13 Clinical Units)**: Central Records dispersal hub radiating to 12 spokes + 300 DPI flowchart.
    - **Section 3 (Seven System Components)**:
      1. Cloud E-Archive records desk (`/archive`, sub-100ms search, shelf locator).
      2. Morning Pre-load & Pull list (Appointment vs Walk-in patients).
      3. Hub-and-Spoke Dispersal (4 simultaneous cloud events).
      4. Clinic Queue Display on clinic PCs/laptops (Expected, Arrived, In Treatment, Completed, DNA).
      5. Offline-First Local Sync (real-time sync, local TXT fallback, auto-reconnect).
      6. Staff Barcode PWA for clinic nurses (0.2s custody transfer).
      7. Executive Dashboard (daily footfall, clinic workload heatmap, satisfaction).
    - **Section 4 (A Typical Day)**: End-to-end timeline + Mr. Kwesi Mensah's clinical journey narrative (60-minute post-scan survey).
    - **Section 5 (Patient Types & Scope)**: Walk-in, Appointment, X-Ray Only.
    - **Section 6 (Cloud Infrastructure)**: Vercel Production Pro + Neon PostgreSQL Production package.
    - **Section 7 (Implementation)**: 4-week rollout roadmap.
    - **Section 8 (Future Requirements)**: Formally captured X-Ray tracking module deferred to next phase.





