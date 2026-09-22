# UGDS Customer Care, Hospital Archive & Experience Platform
## Comprehensive Master System Specification & Strategic Phased Roadmap
**University of Ghana Dental School (UGDS) — Korle Bu Teaching Hospital**

---

## 1. Executive Summary & Vision

The **UGDS Customer Care & Experience Platform** is an enterprise-grade digital ecosystem designed specifically for the University of Ghana Dental School at Korle Bu. 

It unifies **clinical feedback analytics**, **real-time hospital folder tracking (`UGDS_SMS`)**, **priority patient follow-ups**, **automated quality flag email alerts**, and **automated patient & staff relationship management (CRM)** into a modern, cloud-connected architecture.

```
+-----------------------------------------------------------------------------------+
|                        UGDS ENTERPRISE HEALTHCARE PLATFORM                        |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|   [ 1. FRONTEND EXPERIENCE (React 18 + Vite) ]                                    |
|   - Executive Overview & Role-based Unit Dashboards                               |
|   - Full Birthday Celebration Hub on Main Dashboard (Tomorrow, Today, Week, Month)|
|   - Patients Directory & Movement Tracker (`/patients`) (125k Archive Records)    |
|   - Unit Quality Flags & Automated Leadership Email Alerting (`/flags`)           |
|   - Unit Leaderboard & Satisfaction Rankings (13 Clinical Departments)            |
|   - Priority Follow-Ups & Complaints Kanban Resolution Desk                       |
|   - Public Mobile-Optimized Survey Experience (`/survey`)                         |
|                                                                                   |
|                                       ^                                           |
|                                       | REST API (JWT & PIN Auth)                 |
|                                       v                                           |
|                                                                                   |
|   [ 2. CLOUD CORE ENGINE (FastAPI + Neon Postgres) ]                              |
|   - RESTful API with Role-Based Access Control (Dean, IT Admin, Unit Heads)       |
|   - Automated Email Service: Dispatches Quality Flag & Underperformance Alerts   |
|   - Real-time Analytics Aggregations & Sentiment Scoring                          |
|   - Automatic Birthday Decoding Engine (Translates legacy eArchive codes to DOB)  |
|   - Automated Scheduler (Daily Morning SMS via Vercel Cron @ 08:00 AM)           |
|                                                                                   |
|           ^                                               ^                       |
|           | Secure DB Sync                                | SMS API Webhooks      |
|           v                                               v                       |
|                                                                                   |
|   [ 3. ON-SITE HOSPITAL PC INTEGRATION ]          [ 4. TELECOM & EMAIL GATEWAYS ] |
|   - Background Folder Watcher (`UGDS_SMS`)        - Arkesel v2 SMS Provider       |
|   - Live Scanner & Hourly eDump Diff Engine       - Automated SMTP / Resend Email |
|   - Anti-Spam 7-Day Frequency Guard               - Ghanaian Telco Mobile Parser  |
|                                                   - Dedicated Sender ID (`UGDS`)  |
+-----------------------------------------------------------------------------------+
```

---

## 2. Inventory of System Modules & Features

### Module 1: Executive Overview Dashboard
* **Real-Time Headline KPIs**:
  * **Patients Visited This Week**: Direct metric counter connected to the on-site folder watcher scanning live patient registrations (e.g. 142 visits).
  * **Overall Satisfaction Rate**: Composite calculation across all evaluated clinical interactions (94%).
  * **Total Responses**: Real-time count of patient feedback submissions.
  * **Recommendation Rate**: Proportion of patients who recommend UGDS.
  * **Active Follow-Up Requests**: Immediate visual alert for pending clinical complaints requiring attention.
* **Full Birthday Celebrations & Personal Call Hub**:
  * Embedded directly on the Overview Dashboard.
  * Shows badge: *"Automated SMS Active (8:00 AM)"* clarifying that text greetings are delivered automatically.
  * Enables administrators to **personally call celebrants** via a 1-click telephone button, with a checkmark logger to track completed calls.
  * Filter tabs across **Tomorrow**, **Today**, **This Week**, and **This Whole Month**.

### Module 2: Patients Directory & Movement Tracker (`/patients`)
* Complete digital directory indexing **125,042 patient archive records** from Korle Bu's legacy archives.
* **Live Movement Breakdown**:
  * **Total Patients in System**: 125,042.
  * **Visited Within This Month**: 312 patients (synced from live folder watcher scans).
  * **Yet to Visit This Month**: 124,730 patients (eligible for recall and follow-up care).
* **Instant Search & Filters**: Search by Name, Hospital Folder Number (`K/13 ...`), Shelf Rack Location (`MR-1A-...`), or Mobile Number.
* **Direct Action**: Quick-call button for patient coordination and recall.

### Module 3: Unit Quality Flags & Automated Leadership Email Alerting (`/flags`)
* **Underperformance Detection**: Automatically evaluates all 13 clinics against hospital clinical benchmarks (default: 40% satisfaction threshold).
* **Automated Email Notification System**:
  * When a clinic drops below the quality threshold or receives repeated negative feedback (e.g., pain management or cashier delays), the system automatically triggers an **Executive Email Alert** with quality flags.
  * Sent directly to:
    * The **Dean & Medical Directorate**
    * The specific **Unit Head** in charge of the flagged department
    * The **Quality Assurance Committee**
  * Email contents include: Flagged department name, satisfaction score, critical patient quotes, and recommended corrective action.

### Module 4: Unit Leaderboard (`/units`)
* Dedicated clinical department ranking across all 13 dental school units.
* Comparative satisfaction charts benchmarking each department against the hospital-wide average.

### Module 5: Priority Follow-Ups & Complaints Kanban Desk (`/follow-ups`)
* Real-time routing of dissatisfied responses (ratings ≤ 2 stars, pain management issues, cashier delays).
* Pipeline: **Pending Review ➔ Under Investigation ➔ Resolved**.

### Module 6: On-Site Folder Watcher Daemon (`ugds-folder-watcher`)
* Background Windows service monitoring folder movements and hourly dumps (`C:\eArchive_Bible\Old_Bible`).
* Automatically formats Ghanaian numbers and queues SMS survey links via Arkesel.

---

## 3. Comprehensive Phased Implementation Roadmap

```
  PHASE 1 (Immediate / In-Flight)       PHASE 2 (Post-Friday Launch)          PHASE 3 (Full HMS Expansion)
+---------------------------------+   +---------------------------------+   +---------------------------------+
| Complete eArchive Cloud Sync    |   | Zero-Touch Automation & Alerts  |   | Enterprise Hospital Management  |
| - 125,042 archive migration     |   | - Automated 8:00 AM Birthday SMS|   | - Electronic Medical Records    |
| - Watcher visit sync to cloud   |   | - Automated Quality Email Flags |   | - Digital Dental Charting       |
| - Decommission desktop MySQL 5.0|   | - Weekly Dean's SMS Digest      |   | - Electronic Appointment System |
| - Full local testing validation |   | - Unit Head Alert Triggers      |   | - Billing & Insurance NHIS Sync |
+---------------------------------+   +---------------------------------+   +---------------------------------+
```

### Phase 1: Core Foundation & eArchive Cloud Sync (Current Active Phase)
* **Status**: In-Flight (Local testing verified; preparing for post-Friday production deployment).
* **Deliverables**:
  1. Complete extraction and cloud migration of the **125,042 patient archive records** (`eDump_*.txt` & Excel bible).
  2. Full DOB decoding from patient codes (e.g., `YSINT12011964-1` ➔ `12-01-1964`).
  3. Real-time folder movement synchronization connecting the on-site PC watcher to the cloud database.
  4. Local testing sign-off by hospital team.
  5. Retirement of the legacy desktop MySQL 5.0 server on port 3307.

### Phase 2: Zero-Touch Automation & Automated Email Flagging (Post-Friday)
* **Status**: Scheduled immediately after Phase 1 sign-off.
* **Deliverables**:
  1. **Automated Birthday Cron Engine**: Daily scheduled Vercel Cron execution at `08:00 AM UTC` dispatching personalized SMS greetings from the Dean.
  2. **Automated Clinic Quality Email Alerts**:
     * Real-time email dispatch to the Dean and Unit Heads when a clinic falls below quality benchmarks.
     * Weekly quality digests highlighting recurring complaint areas.
  3. **Weekly Dean's Executive SMS**: Automated Friday 5:00 PM summary SMS sent to the Dean with departmental rankings and patient visit totals.

### Phase 3: Full Hospital Management System (HMS) & Patient Care Portal
* **Status**: Strategic Vision (Building directly upon the Patients Directory).
* **Deliverables**:
  1. **Electronic Medical Records (EMR)**: Transitioning patient profiles from read-only directory to full electronic clinical records with treatment history.
  2. **Interactive Dental Charting**: Visual odontogram for dental surgeons across Conservative, Periodontic, and Orthodontic clinics.
  3. **Electronic Appointment Scheduling & 24h Recall SMS**: Automated reminder texts sent 24 hours in advance to reduce missed clinic appointments.
  4. **WhatsApp Interactive Patient Bot**: Two-way patient communication for post-operative instructions and appointment confirmations.
  5. **Cashier & NHIS Billing Reconciliation**: Digital receipts and revenue tracking integrated directly into the account unit.

---

## 4. Responsibility & Operational Matrix

| Stakeholder | Role in System | Key Actions |
| :--- | :--- | :--- |
| **Dean & Directorate** | Executive Oversight | Receives automated weekly SMS & quality alert emails; reviews hospital-wide satisfaction. |
| **Unit Heads** | Departmental Leadership | Receives quality flag emails when unit rating drops; investigates clinical and cashier bottlenecks. |
| **Customer Care Officers** | Patient Care & Outreach | Uses Dashboard Birthday Hub to make personal calls to celebrants; resolves complaints in Follow-ups desk. |
| **Records / Reception** | Folder Tracking | Monitors folder movements via on-site watcher; checks monthly patient visit numbers in Patients Directory. |
| **IT Administration** | Infrastructure & Security | Maintains database backups, manages user PINs, and monitors SMS/Email gateway health. |
