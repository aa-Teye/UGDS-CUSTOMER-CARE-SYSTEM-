# UNIVERSITY OF GHANA DENTAL SCHOOL
## Phase 2 — Master System Specification & Strategic Blueprint
**Cloud E-Archive  |  Hub-and-Spoke Dispersal  |  Barcode PWA  |  Executive Dashboard**  
*Built on Phase 1: 125,042 patient records migrated  |  Live CRM dashboard  |  Automated birthday messaging*

---

## EXECUTIVE SUMMARY

Phase 2 transforms clinical records operations at the University of Ghana Dental School. Building on Phase 1 — which migrated 125,042 patient records to the cloud and deployed a live CRM dashboard — Phase 2 permanently replaces the 15-year-old legacy desktop eArchive software with a cloud-native system that gives every stakeholder in the hospital real-time visibility of every patient folder, from the moment it is pulled from the shelf to the moment it is returned.

The system is built around a single core principle: **one scan, one destination selection, and everything updates everywhere simultaneously — the clinic queue, the records room, and the executive dashboard.**

> **Out of Scope Notice:**  
> *X-Ray patients (who do not have folders) are captured as a future user requirement and are out of scope for Phase 2. They will be addressed in a subsequent phase.*

---

## 1. WHY PHASE 2: THE LEGACY SYSTEM PROBLEM

For over fifteen years, all 125,042 patient folder histories have lived on a single desktop PC running Visual Basic eArchive software connected to a local MySQL 5.0 database on port 3307. This creates four critical operational risks:

| Risk | Impact |
| :--- | :--- |
| **Single Point of Failure** | One hard drive crash or malware attack instantly paralyses records retrieval across all 13 departments. |
| **Zero Clinical Custody** | Once a folder leaves the records room, no one knows where it is. Staff waste hours searching clinic by clinic. |
| **No Patient Journey History** | The legacy system stores registration numbers only. It cannot record when a patient arrived, which clinic treated them, or how long they waited. |
| **Management Blindspot** | The Dean and leadership have no real-time counters of daily patient visits, forcing staffing decisions based on guesswork. |

---

## 2. THE 13 UGDS CLINICAL UNITS

The Records Unit acts as the Central Archival and Dispersal Hub. All 12 clinical and service departments are spokes that receive folders directly from Records and return them directly to Records after treatment.

| No. | Unit | Function | Role in Dispersal Model |
| :---: | :--- | :--- | :--- |
| **1** | **Records Unit (Hub)** | Central Archival & Dispersal | Pulls folders; scans out; selects destination; audits all returns. |
| **2** | **Account (Cashier)** | Billing & Financial Clearance | Independent service point; does not block clinical flow. |
| **3** | **Oral Diagnosis Clinic** | Primary Intake & Triage | Receives and routes new patients to specialist care. |
| **4** | **Cons. Clinic** | Conservative & Operative Dentistry | Receives folders for restorations and routine care. |
| **5** | **Students Clinic** | Undergraduate Training | Receives folders for supervised student clinical work. |
| **6** | **Advance Cons. Clinic** | Endodontics & Prosthodontics | Receives folders for root canals, crowns, and bridges. |
| **7** | **Residents Clinic** | Postgraduate Specialized Care | Receives folders for advanced referral cases. |
| **8** | **Periodontic Clinic** | Gum Health & Periodontology | Receives folders for scaling, surgery, and bone-loss care. |
| **9** | **Paedodontic Clinic** | Child & Adolescent Dentistry | Receives folders for child dentistry and preventive care. |
| **10** | **Orthodontic Clinic** | Malocclusion & Alignment | Receives folders for brace adjustments and follow-ups. |
| **11** | **Consultant Surgery 1** | Oral & Maxillofacial Surgery | Receives folders for surgical extractions and biopsies. |
| **12** | **Consultant Surgery 2** | Oral & Maxillofacial Surgery | Receives folders for facial trauma and surgical consultations. |
| **13** | **X-Ray (Radiology)** | Dental Imaging | Receives folders for periapical, bitewing, and OPG imaging. |

### Central Records Dispersal & Custody Flowchart
```
                                  ┌───► [3. Oral Diagnosis Clinic] ───► [13. X-Ray Radiology]
                                  │
                                  ├───► [2. Account (Cashier)]     ───► (Non-blocking Clearance)
                                  │
[1. Records Unit] ────────────────┼───► [4. Cons. Clinic]          ───► [6. Advance Cons. Clinic]
(Central Dispersal Hub)            │
                                  ├───► [5. Student's Clinic]      ───► [7. Resident's Clinic]
                                  │
                                  ├───► [8. Periodontic Clinic]    ───► [9. Paedodontic Clinic]
                                  │
                                  ├───► [10. Orthodontic Clinic]
                                  │
                                  └───► [11. Consultant Surgery 1] ───► [12. Consultant Surgery 2]
```

---

## 3. THE SEVEN SYSTEM COMPONENTS

### 3.1 Cloud E-Archive — Records Desk Interface
The records officer's primary interface. Replaces the legacy desktop software entirely.

| Feature | Detail |
| :--- | :--- |
| **Patient Search** | Sub-100ms search across all 125,042 records by folder number or patient name. |
| **Shelf Coordinate Locator** | Instantly displays the exact physical location: `RACK | BAY | SHELF | SLOT` so the officer walks directly to the right shelf. |
| **Scan & Dispatch** | Officer scans the folder barcode, selects the destination clinic from a dropdown. One action triggers everything. |
| **Status Tracking** | Folder status updates hospital-wide: `PULLED` / `IN TRANSIT` / `IN CUSTODY` / `RETURNED TO ARCHIVE`. |

### 3.2 Morning Pre-Load & Pull List — Appointment Scheduling
Every patient at UGDS falls into one of two categories:

| Patient Type | How They Are Handled |
| :--- | :--- |
| **Appointment Patient** | Has a pre-booked session with a specific doctor. Their folder is pre-loaded into the system the night before or early morning so Records can prepare the morning pull list in advance. |
| **Walk-in Patient** | Arrives without an appointment. Folder is pulled and dispatched on arrival using the same scan-and-select flow. |

> **Operational Rule:**  
> *Even appointment patients must go through the scan-and-select step at Records before their folder moves. The pre-load simply means Records knows in advance which folders to prepare.*

### 3.3 Hub-and-Spoke Dispersal — The Core Workflow
This is the central operational change Phase 2 delivers. The Records officer scans the folder barcode and selects the destination clinic from a dropdown. That single action triggers four simultaneous events:

| What Happens | Where It Occurs |
| :--- | :--- |
| **Folder status changes to IN TRANSIT** | Records desk and all system views |
| **Patient is added to that clinic's daily queue** | Clinic PC / laptop display |
| **Executive dashboard updates workload count** | Dean's dashboard in real time |
| **60-minute SMS survey countdown begins** | Cloud engine (background dispatch) |

### 3.4 Clinic Queue Display — On Each Clinic PC / Laptop
Each of the 13 clinics has its own display on their PC or laptop showing their patient queue for the day. This screen updates live as the Records desk dispatches folders throughout the morning.

| Queue Status | What the Clinic Sees |
| :--- | :--- |
| **Expected** | Patients dispatched from Records, folder in transit to this clinic. |
| **Arrived** | Folder scanned in by clinic nurse via the PWA. Patient confirmed in custody. |
| **In Treatment** | Patient currently being attended to by the doctor. |
| **Completed** | Treatment done. Folder awaiting return to Records. |
| **Did Not Attend** | Patient was expected but folder was never scanned in at the clinic. |

The clinic can see at a glance: how many patients are expected today, how many have arrived, how many have been seen, and how many are still outstanding.

### 3.5 Offline-First Local Sync — Clinic Data Resilience
The clinic queue and all scan activity at each clinic operates offline-first. This means:

| Scenario | What Happens |
| :--- | :--- |
| **Internet is available** | All scans and queue updates sync to the central Neon PostgreSQL database in real time. |
| **Internet drops** | All activity continues normally. Scans and updates are saved immediately to a local TXT file on the clinic laptop. No data is lost. |
| **Internet is restored** | The system automatically detects the connection and syncs all locally saved records to the central database. No manual action required. |

### 3.6 Staff Barcode PWA — Clinic Nurse & Assistant Interface
A mobile-first Progressive Web App that runs on any clinic smartphone, tablet, or PC browser. No app store installation required.

| Feature | Detail |
| :--- | :--- |
| **Authentication** | Nurse or assistant signs in with their staff PIN and selects their active clinic unit. |
| **Folder Arrival Scan** | Live camera viewfinder with a single *Scan Arriving Folder* button. When the folder arrives, the nurse scans the barcode. |
| **Custody Confirmation** | Screen flashes green: `Folder K/13 5622 Confirmed — In Custody at Cons. Clinic at 09:42 AM`. |
| **Instant Sync** | Custody transfers in 0.2 seconds. Records room and executive dashboard update immediately. |

### 3.7 Executive Dashboard — Dean & Management View
Real-time operational intelligence for the Dean and hospital leadership. No manual compilation required.

| Metric | What It Shows |
| :--- | :--- |
| **Live Daily Footfall** | Verified total patients who visited today, this week, and this month across all 13 departments. |
| **Departmental Workload** | Live count of how many folders are currently held in each of the 13 clinical units. |
| **Patient Journey Timeline** | Full day timeline for any individual patient: `08:15 Arrival at Records > Dispatched to Surgery 1 > 08:40 Custody Confirmed > 10:15 Returned to Archive`. |
| **Patient Satisfaction** | Live satisfaction scores from automated SMS surveys, integrated in real time. |

---

## 4. A TYPICAL DAY: END-TO-END WORKFLOW

| Time | Who | Action |
| :--- | :--- | :--- |
| **07:30 AM** | Records Officers | Open `/archive`. Pre-loaded appointment list is ready. Officers pull folders for scheduled patients and begin scanning and dispatching to clinics. |
| **08:00 AM onwards** | Walk-in Patients | Arrive at reception. Records officer searches folder, pulls from shelf coordinate, scans out, selects clinic. Patient added to that clinic's queue instantly. |
| **08:15 AM** | Clinic Nurse | Opens Staff PWA. Sees incoming folders on clinic queue. Scans each folder barcode as it arrives. Custody confirmed in 0.2 seconds. |
| **08:30 AM – 02:00 PM** | Doctors & Staff | Attend to patients. Clinic queue tracks who has been seen and who is still waiting in real time. |
| **60 Min Post-Scan** | Cloud Engine | Automated SMS dispatched to patient: personalized feedback survey link: *"UGDS FEEDBACK: Dear {name}, thank you for visiting UGDS. Please rate your experience: {link}"*. |
| **02:30 PM – 04:30 PM** | Records Officers | Treated folders returned from clinics. Officer scans each one back in. Status returns to `ARCHIVED`. Folder returned to exact shelf slot. |
| **04:35 PM** | Dean / Leadership | Reviews executive dashboard: total patients seen, clinic workload distribution, folder accountability, live satisfaction scores. |

### The Patient Experience: A Day with Mr. Kwesi Mensah
To see these seven components working in harmony, consider **Mr. Kwesi Mensah (Folder `K/13 5622`)** arriving at 08:00 AM:
1. **At Records:** The officer queries his name in <100ms, walks straight to Shelf `[ RACK: 1A | BAY: 2 | SHELF: B1 | SLOT: 8 ]`, scans the barcode, and selects *Cons. Clinic*. Instantly, Mr. Mensah appears on the Conservative Clinic PC queue as *Expected*.
2. **At 08:15 AM:** The orderly delivers the folder. Nurse Grace scans the barcode on her PWA camera, moving him to *Arrived*.
3. **At 08:30 AM:** Dr. Boateng attends to him (*In Treatment*).
4. **At 09:03 AM (Exactly 60 minutes after checkout scan):** Mr. Mensah's phone buzzes with the feedback survey link. He submits a 5-star rating while rinsing.
5. **At 02:30 PM:** His folder is scanned back into Records and safely restored to Shelf `1A-2-B1-8`. In his office, the Dean sees today's attendance hit 192, with 100% of folders accounted for.

---

## 5. PATIENT TYPES & SYSTEM SCOPE

| Patient Type | Folder? | Pre-Load? | Scan Flow? | Phase |
| :--- | :---: | :---: | :--- | :--- |
| **Walk-in** | Yes | No — pulled on arrival | Full scan-and-select | **Phase 2 (Active)** |
| **Appointment** | Yes | Yes — pre-loaded night before or morning | Full scan-and-select (mandatory) | **Phase 2 (Active)** |
| **X-Ray Only** | No | N/A | Future requirement — out of scope | Deferred to Future Phase |

---

## 6. CLOUD INFRASTRUCTURE

Phase 2 moves from the single-PC legacy environment to a dedicated annual enterprise cloud package on Vercel and Neon PostgreSQL:

| Component | Provider & Tier | Purpose | Key Safeguards |
| :--- | :--- | :--- | :--- |
| **Frontend & API** | **Vercel Production Pro** | Hosts E-Archive desk, clinic queues, and serverless API. | 99.99% SLA uptime, regional CDN, automated SSL, custom UGDS domain. |
| **Central Database** | **Neon PostgreSQL Production** | Stores all 125,042 patient records, folder movement logs, and staff data. | Automated point-in-time recovery, daily backups, connection pooling for all 13 clinics simultaneously. |
| **Staff PWA** | **Vercel PWA / Edge Cache** | Delivers the mobile barcode scanner to all clinic devices. | Instant mobile loading, offline caching, no app store installation required. |

---

## 7. IMPLEMENTATION: 4-WEEK ROLLOUT

| Sprint | Focus | Key Deliverables |
| :--- | :--- | :--- |
| **Week 1** | **Foundation & Cloud Setup** | Configure on-site daemon at Records PC. Activate Vercel Pro and Neon production packages. Ingest 134 staff profiles. Set up appointment pre-load system. |
| **Week 2** | **Cloud E-Archive Deployment** | Deploy `/archive` module with sub-100ms search and shelf coordinate locator. Decommission legacy MySQL 5.0 desktop software. |
| **Week 3** | **Clinic Queue & PWA Launch** | Launch clinic queue displays on all 13 clinic PCs. Deploy Staff Barcode PWA. Activate offline-first local TXT sync. Roll out across Oral Diagnosis, Cons. Clinic, and Surgery. |
| **Week 4** | **Executive Dashboard & Handover** | Connect live footfall counters to Phase 1 dashboard. Conduct nursing staff training. Executive leadership review and sign-off. |

---

## 8. FUTURE REQUIREMENTS (OUT OF SCOPE — PHASE 2)

> **Formally Captured Requirement:**  
> *The following requirement has been formally captured and deferred to a future development phase. It does not affect Phase 2 delivery.*

| Requirement | Description | Reason Deferred |
| :--- | :--- | :--- |
| **X-Ray Patient Tracking** | X-Ray patients do not have physical folders. A lightweight check-in system is needed to log their visits for daily footfall counts without triggering the standard folder scan-and-dispatch flow. | Different workflow from folder-based patients. Requires separate design and will be scoped as a standalone feature in the next phase. |

---

**University of Ghana Dental School**  
Phase 2 Master System Specification  |  2026  
*Cloud E-Archive  |  Hub-and-Spoke Dispersal  |  Barcode PWA  |  Executive Dashboard*
