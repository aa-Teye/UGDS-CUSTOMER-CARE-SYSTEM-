import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def generate_pdf():
    pdf_filename = r"d:\MYCODING FILES\KORLEBU PROJECTS\UGDS_Phase2_Project_Document.pdf"
    img_flowchart = r"d:\MYCODING FILES\KORLEBU PROJECTS\ugds_folder_flowchart.png"

    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Brand Colors
    primary_color = colors.HexColor("#003866")     # UGDS Navy Blue
    secondary_color = colors.HexColor("#0284C7")   # Medical Blue
    dark_neutral = colors.HexColor("#1E293B")      # Charcoal Text
    light_blue = colors.HexColor("#EFF6FF")        # Soft Blue Accent
    border_blue = colors.HexColor("#BFDBFE")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=primary_color,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=secondary_color,
        spaceAfter=10
    )

    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#64748B"),
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=primary_color,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=secondary_color,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=dark_neutral,
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=12,
        bulletIndent=4,
        spaceAfter=3
    )

    table_header = ParagraphStyle(
        'TH',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white
    )

    table_cell = ParagraphStyle(
        'TC',
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=dark_neutral
    )

    table_cell_bold = ParagraphStyle(
        'TCB',
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=primary_color
    )

    elements = []

    # ==================== PAGE 1: TITLE & EXECUTIVE SUMMARY ====================
    elements.append(Paragraph("UNIVERSITY OF GHANA DENTAL SCHOOL — KORLE BU", subtitle_style))
    elements.append(Paragraph("Phase 2 Master System Specification & Strategic Blueprint", title_style))
    elements.append(Paragraph("Cloud E-Archive, Intelligent Folder Chain of Custody, Staff Barcode PWA & Enterprise Cloud Hosting", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceBefore=4, spaceAfter=12))


    exec_box = (
        "<b>Strategic Executive Mandate:</b> Following the successful completion of <b>Phase 1</b> (125,042 patient records migrated to the cloud, "
        "live customer experience dashboard deployed, and automated birthday CRM active), <b>Phase 2</b> modernizes clinical records "
        "operations across the entire hospital. It permanently replaces the legacy desktop eArchive software (MySQL 5.0 on port 3307) "
        "with an accessible <b>Cloud E-Archive</b>, equips nurses and records officers with a <b>Staff Barcode Progressive Web App (PWA)</b> "
        "to track folder chain-of-custody in real time across all 13 clinical departments, feeds live daily patient footfall intelligence "
        "directly into executive management, and formalizes the dedicated annual cloud production hosting on Vercel and Neon PostgreSQL."
    )
    exec_table = Table([[Paragraph(exec_box, body_style)]], colWidths=[540])
    exec_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), light_blue),
        ('BOX', (0,0), (-1,-1), 1, border_blue),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    elements.append(exec_table)
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("1. Legacy System Audit & Decommissioning Rationale", h1_style))
    elements.append(Paragraph("The hospital records room currently operates on an unmaintained desktop setup installed over 15 years ago:", body_style))
    elements.append(Paragraph("• <b>Single Point of Failure:</b> 125,042 patient folder histories sit on a single physical workstation in the records room. Hard disk failure or malware would paralyze clinical retrieval school-wide.", bullet_style))
    elements.append(Paragraph("• <b>Zero Clinical Unit Visibility:</b> When folders leave the records room, records officers have no real-time knowledge of where they are, leading to missing folders and delayed consultations.", bullet_style))
    elements.append(Paragraph("• <b>No Patient Journey History:</b> The legacy desktop program does not track clinical routes—when the patient arrived, which units they passed through, or which clinician treated them.", bullet_style))
    elements.append(Paragraph("• <b>Administrative Blindspot:</b> Management has no automated count of daily, weekly, or monthly attendance figures.", bullet_style))

    elements.append(Spacer(1, 6))
    elements.append(Paragraph("2. The 13 UGDS Clinical Units & Service Points", h1_style))
    elements.append(Paragraph("Phase 2 integrates directly with the 13 authentic clinical and operational units of the Dental School:", body_style))

    unit_data = [
        [Paragraph("No.", table_header), Paragraph("Unit / Service Point", table_header), Paragraph("Departmental Function", table_header), Paragraph("Phase 2 Folder Tracking Role", table_header)],
        [Paragraph("1", table_cell), Paragraph("<b>Records Unit</b>", table_cell_bold), Paragraph("Central Archival Custody", table_cell), Paragraph("Pulls folder from Shelf (MR-1A-A1-1); scans barcode out; audits returns.", table_cell)],
        [Paragraph("2", table_cell), Paragraph("<b>Account (Cashier)</b>", table_cell_bold), Paragraph("Billing & Financial Clearance", table_cell), Paragraph("Verifies active consultation and fee/NHIS receipt.", table_cell)],
        [Paragraph("3", table_cell), Paragraph("<b>Oral Diagnosis</b>", table_cell_bold), Paragraph("Intake & Primary Triage", table_cell), Paragraph("Scans folder arrival; diagnoses and routes patient to specialty clinics.", table_cell)],
        [Paragraph("4", table_cell), Paragraph("<b>Cons. Clinic</b>", table_cell_bold), Paragraph("Conservative & Restorative Dentistry", table_cell), Paragraph("Logs folder receipt; manages operative procedures and cavity restorations.", table_cell)],
        [Paragraph("5", table_cell), Paragraph("<b>Student's Clinic</b>", table_cell_bold), Paragraph("Undergraduate Training Facility", table_cell), Paragraph("Monitors folders assigned to dental students under faculty supervision.", table_cell)],
        [Paragraph("6", table_cell), Paragraph("<b>Advance Cons. Clinic</b>", table_cell_bold), Paragraph("Endodontics & Prosthodontics", table_cell), Paragraph("Tracks complex multi-visit root canals, crowns, and bridges.", table_cell)],
        [Paragraph("7", table_cell), Paragraph("<b>Resident's Clinic</b>", table_cell_bold), Paragraph("Postgraduate Specialized Care", table_cell), Paragraph("Manages advanced referral cases and resident clinical logs.", table_cell)],
        [Paragraph("8", table_cell), Paragraph("<b>Periodontic Clinic</b>", table_cell_bold), Paragraph("Gum Health & Periodontology", table_cell), Paragraph("Tracks surgical and non-surgical periodontal therapy sessions.", table_cell)],
        [Paragraph("9", table_cell), Paragraph("<b>Paedodontic Clinic</b>", table_cell_bold), Paragraph("Child & Adolescent Dentistry", table_cell), Paragraph("Specialized child dental procedures and preventive sealants.", table_cell)],
        [Paragraph("10", table_cell), Paragraph("<b>Orthodontic Clinic</b>", table_cell_bold), Paragraph("Malocclusion & Dental Alignment", table_cell), Paragraph("Monthly brace adjustments and craniofacial follow-ups.", table_cell)],
        [Paragraph("11", table_cell), Paragraph("<b>Consultant Surgery 1</b>", table_cell_bold), Paragraph("Oral & Maxillofacial Surgery 1", table_cell), Paragraph("Surgical extractions, impactions, and soft-tissue biopsies.", table_cell)],
        [Paragraph("12", table_cell), Paragraph("<b>Consultant Surgery 2</b>", table_cell_bold), Paragraph("Oral & Maxillofacial Surgery 2", table_cell), Paragraph("Facial trauma review, complex maxillofacial surgeries.", table_cell)],
        [Paragraph("13", table_cell), Paragraph("<b>X-Ray (Radiology)</b>", table_cell_bold), Paragraph("Dental Imaging & Radiography", table_cell), Paragraph("Periapical, bitewing, and panoramic (OPG) imaging scans.", table_cell)],
    ]
    unit_table = Table(unit_data, colWidths=[24, 116, 170, 230])
    unit_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(unit_table)

    # ==================== PAGE 2: FLOWCHART ====================
    elements.append(PageBreak())
    elements.append(Paragraph("3. Central Records Dispersal & Custody Flowchart", h1_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceBefore=2, spaceAfter=8))
    elements.append(Paragraph(
        "The diagram below illustrates the direct Hub-and-Spoke Dispersal architecture: the patient arrives at the Records Desk, "
        "the folder is pulled and barcode-scanned (arming the automated 60-minute feedback survey), and Records disperses it directly "
        "to whichever clinic or service point the patient is visiting. Once treatment is completed, the folder returns directly to Records:",
        body_style
    ))
    elements.append(Spacer(1, 4))

    if os.path.exists(img_flowchart):
        elements.append(Image(img_flowchart, width=7.2*inch, height=8.2*inch))

    # ==================== PAGE 3: WHAT USERS SEE & HOW IT WORKS ====================
    elements.append(PageBreak())
    elements.append(Paragraph("4. Operational Walkthrough: What Each User Sees & How It Operates", h1_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceBefore=2, spaceAfter=8))

    elements.append(Paragraph("A. For the Records Officer (At the Central Records Desk)", h2_style))
    elements.append(Paragraph(
        "<b>Screen Interface:</b> Cloud E-Archive Desk (<code>/archive</code>)<br/>"
        "• <b>What Appears:</b> High-speed search bar with live filtering across 125,042 records. Typing folder number (<code>K/13 5622</code>) "
        "renders a prominent shelf coordinate badge: <b>[ RACK: 1A | BAY: 1 | SHELF: A1 | SLOT: 1 ]</b>.<br/>"
        "• <b>Action:</b> Officer taps 'Check-Out', picks destination clinic (e.g. Cons. Clinic, Surgery, Ortho, or Cashier), scans folder barcode. "
        "Status changes instantly to <i>'CHECKED OUT / IN TRANSIT'</i>. The automated 60-minute patient survey timer is armed in the cloud.",
        body_style
    ))

    elements.append(Paragraph("B. For the Clinic Nurse & Dental Assistant (In Any Destination Clinic)", h2_style))
    elements.append(Paragraph(
        "<b>Screen Interface:</b> Staff Mobile Progressive Web App (PWA)<br/>"
        "• <b>Authentication:</b> Nurse signs in with staff PIN and active clinic profile (e.g., 'Nurse Grace — Cons. Clinic').<br/>"
        "• <b>What Appears:</b> Camera scanner viewfinder. Nurse points phone camera at the folder barcode upon arrival.<br/>"
        "• <b>Confirmation:</b> Screen flashes green: <i>'Folder K/13 5622 Confirmed: In Custody at Cons. Clinic at 08:15 AM'</i>. "
        "Custody updates in 0.2 seconds hospital-wide without cashier bottlenecks.",
        body_style
    ))

    elements.append(Paragraph("C. For the Dean & Executive Leadership (On the Master Dashboard)", h2_style))
    elements.append(Paragraph(
        "<b>Screen Interface:</b> Executive Overview Dashboard<br/>"
        "• <b>Live Daily Footfall:</b> Verified count of patients who visited the dental school today, this week, and this month.<br/>"
        "• <b>Departmental Heatmap:</b> Live bar chart showing active folder distribution across all 13 clinics.<br/>"
        "• <b>Patient Route Timeline:</b> Complete audit trail showing when the patient arrived, which units they visited, and when discharged.",
        body_style
    ))

    elements.append(Paragraph("A Typical Day in the Hospital (End-to-End Workflow):", h2_style))
    elements.append(Paragraph("• <b>07:30 AM — Morning Pulls & Dispersal:</b> Records officers query scheduled patients on /archive, pull folders from shelf coordinates, scan them out, and disperse them to assigned clinics. The checkout scan arms the 60-minute survey countdown.", bullet_style))
    elements.append(Paragraph("• <b>08:30 AM to 02:00 PM — Direct Clinic Arrival & Care:</b> Orderlies deliver folders directly. Nurses scan on arrival via the Staff PWA. Custody is tracked in real time across the hospital.", bullet_style))
    elements.append(Paragraph("• <b>60 Minutes Post-Checkout Scan — Automated Follow-up Survey:</b> Exactly one hour after the folder was scanned at Records, the patient receives the SMS: <i>'UGDS FEEDBACK: Dear {name}, thank you for visiting UGDS. Please rate your experience: {link}'</i>.", bullet_style))
    elements.append(Paragraph("• <b>02:30 PM to 04:30 PM — Archival Check-In & Re-Shelving:</b> Folders return to records. Officer scans each back in, confirming safe return, and restores it to its physical shelf slot.", bullet_style))
    elements.append(Paragraph("• <b>04:35 PM — Executive Attendance & Quality Reconciliation:</b> Leadership reviews verified daily footfall, clinic turnaround times, and incoming patient ratings on the dashboard.", bullet_style))

    # ==================== PAGE 4: THE PATIENT JOURNEY STORY ====================
    elements.append(PageBreak())
    elements.append(Paragraph("5. The Patient Journey: A Day with Mr. Kwesi Mensah at UGDS Dental School", h1_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceBefore=2, spaceAfter=8))
    elements.append(Paragraph(
        "To illustrate how Phase 2 elevates patient care and operational efficiency, we follow the complete clinical journey "
        "of Mr. Kwesi Mensah visiting the dental school for a scheduled crown review:",
        body_style
    ))

    story_pdf = [
        ("1. 08:00 AM — Patient Arrival & Reception", "Mr. Kwesi Mensah arrives at UGDS and gives his name and folder number (K/13 5622) at the central records reception desk."),
        ("2. 08:01 AM — Sub-Second Cloud Shelf Coordinate", "The records officer enters 'K/13 5622' into /archive. In under 100ms, the screen highlights: <b>[ RACK: 1A | BAY: 2 | SHELF: B1 | SLOT: 8 ]</b>. Zero time is wasted searching through disorganized papers."),
        ("3. 08:03 AM — Direct Dispersal & Survey Countdown Armed", "The officer pulls the physical folder, scans the barcode out, and marks 'Disperse to: Cons. Clinic'. Status updates to 'IN TRANSIT'. An automated 60-minute cloud survey countdown is initiated for Mr. Mensah's phone."),
        ("4. 08:15 AM — Arrival at Clinic & 0.2-Second Custody Scan", "The folder is delivered directly to Conservative Clinic. Nurse Grace scans the barcode using the Staff Barcode PWA on her phone. The screen chimes green: custody is confirmed instantly."),
        ("5. 08:30 AM — Consultation & Treatment", "Dr. Boateng attends to Mr. Mensah, reviews his complete physical records, and completes the crown review and polishing."),
        ("6. 09:03 AM — The 1-Hour Automated Feedback Prompt", "Exactly 60 minutes after the records checkout scan, Mr. Mensah's phone buzzes with the friendly SMS: <i>'UGDS FEEDBACK: Dear Kwesi, thank you for visiting UGDS. Please rate your experience: {link}'</i>. He taps the link and rates his visit 5 stars in 20 seconds."),
        ("7. 09:15 AM — Non-Blocking Service Clearance", "Mr. Mensah completes fee payment at the Cashier desk in under 90 seconds and departs the facility thoroughly satisfied."),
        ("8. 02:30 PM — Archival Return & Physical Re-Shelving", "Completed folders return to Central Records. The officer scans Mr. Mensah's folder back in: status switches to 'RETURNED TO ARCHIVE', and it is re-shelved at [ RACK: 1A | BAY: 2 | SHELF: B1 | SLOT: 8 ]."),
        ("9. 04:00 PM — Executive Leadership Oversight", "The Dean reviews the live Executive Dashboard: 192 patients attended today, zero folders misplaced, and Mr. Mensah's 5-star rating is integrated into the school's real-time satisfaction score.")
    ]

    for st_title, st_desc in story_pdf:
        elements.append(Paragraph(f"• <b>{st_title}:</b> {st_desc}", bullet_style))

    # ==================== PAGE 5: ANNUAL ENTERPRISE CLOUD PACKAGE & ROADMAP ====================
    elements.append(PageBreak())
    elements.append(Paragraph("6. Annual Enterprise Cloud Infrastructure Package (Vercel + Neon PostgreSQL)", h1_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceBefore=2, spaceAfter=8))

    elements.append(Paragraph(
        "To guarantee 100% uptime, high-speed responsiveness, and enterprise security across all 13 clinics, Phase 2 formalizes "
        "a dedicated annual cloud production package on <b>Vercel</b> and <b>Neon PostgreSQL</b>:",
        body_style
    ))
    elements.append(Spacer(1, 4))

    infra_data = [
        [Paragraph("Cloud Component", table_header), Paragraph("Provider & Tier", table_header), Paragraph("Hospital Purpose", table_header), Paragraph("Enterprise Safeguards", table_header)],
        [Paragraph("<b>Frontend & API</b>", table_cell_bold), Paragraph("Vercel Production Pro", table_cell), Paragraph("Hosts Customer Experience Hub, E-Archive Desk, and Serverless API.", table_cell), Paragraph("99.99% SLA uptime, high-speed regional CDN, custom UGDS domain with automated SSL.", table_cell)],
        [Paragraph("<b>Central Database</b>", table_cell_bold), Paragraph("Neon PostgreSQL Production", table_cell), Paragraph("Stores 125,042 patient records, real-time folder movement logs, and staff data.", table_cell), Paragraph("Dedicated compute, automated point-in-time recovery (daily backups), connection pooling for all 13 clinics.", table_cell)],
        [Paragraph("<b>Staff Barcode PWA</b>", table_cell_bold), Paragraph("Vercel PWA / Edge Cache", table_cell), Paragraph("Delivers mobile barcode camera scanner to staff phones and tablets.", table_cell), Paragraph("Instant mobile loading, offline caching support, zero app store installation friction.", table_cell)],
    ]
    infra_table = Table(infra_data, colWidths=[110, 110, 170, 150])
    infra_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    elements.append(infra_table)
    elements.append(Spacer(1, 8))

    elements.append(Paragraph("Strategic Value of the Annual Cloud Package:", h2_style))
    elements.append(Paragraph("• <b>Zero On-Premise Server Risk:</b> Eliminates costly physical server rooms, UPS backups, and on-site hardware maintenance at Korle Bu.", bullet_style))
    elements.append(Paragraph("• <b>Continuous Automated Backups:</b> Neon PostgreSQL provides point-in-time recovery, protecting patient records against data loss.", bullet_style))
    elements.append(Paragraph("• <b>High Concurrency for 13 Clinics:</b> Built-in connection pooling ensures all 13 clinics and records staff search and scan simultaneously without latency.", bullet_style))

    elements.append(Spacer(1, 8))
    elements.append(Paragraph("7. Implementation Phasing & 4-Week Technical Rollout", h1_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceBefore=2, spaceAfter=8))

    roadmap_data = [
        [Paragraph("Sprint / Phase", table_header), Paragraph("Focus & Milestones", table_header), Paragraph("Key Deliverables", table_header), Paragraph("Target Window", table_header)],
        [Paragraph("<b>Sprint 1 (Week 1)</b>", table_cell_bold), Paragraph("On-Site Daemon & Annual Cloud", table_cell), Paragraph("Configure on-site daemon at Records PC; activate Vercel Pro & Neon production packages; ingest 134 staff.", table_cell), Paragraph("Sprint 1", table_cell)],
        [Paragraph("<b>Sprint 2 (Week 2)</b>", table_cell_bold), Paragraph("Cloud E-Archive Desk", table_cell), Paragraph("Deploy /archive web module; sub-100ms 125k search; physical shelf locator; decommission MySQL 5.0.", table_cell), Paragraph("Sprint 2", table_cell)],
        [Paragraph("<b>Sprint 3 (Week 3)</b>", table_cell_bold), Paragraph("Staff Barcode PWA", table_cell), Paragraph("Launch camera barcode PWA; roll out 1-tap check-in/out across Oral Diagnosis, Cons. Clinic, and Surgery.", table_cell), Paragraph("Sprint 3", table_cell)],
        [Paragraph("<b>Sprint 4 (Week 4)</b>", table_cell_bold), Paragraph("Executive Analytics & Handover", table_cell), Paragraph("Connect live visit footfall counters to Phase 1 Dashboard; staff clinical training; leadership review.", table_cell), Paragraph("Sprint 4", table_cell)],
    ]
    roadmap_table = Table(roadmap_data, colWidths=[90, 130, 230, 90])
    roadmap_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    elements.append(roadmap_table)

    doc.build(elements)
    print(f"Updated Phase 2 PDF generated successfully at: {pdf_filename}")

if __name__ == "__main__":
    generate_pdf()
