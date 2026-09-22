import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def create_flowchart_image(output_path):
    fig, ax = plt.subplots(figsize=(14, 11), dpi=300)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 11)
    ax.axis('off')

    # Color Palette
    c_blue = "#003866"       # UGDS Navy Blue
    c_sky = "#0284C7"        # Medical Sky Blue
    c_teal = "#0D9488"       # Teal
    c_amber = "#D97706"      # Amber
    c_purple = "#7C3AED"     # Purple
    c_green = "#059669"      # Emerald Green
    c_card_bg = "#F8FAFC"    # Slate Light

    # Title
    ax.text(7, 10.5, "UGDS CLINICAL FOLDER DISPERSAL & CUSTODY FLOWCHART", 
            ha='center', va='center', fontsize=15, fontweight='bold', color=c_blue)
    ax.text(7, 10.15, "Hub & Spoke Model: Central Records Disperses Directly to Any Clinical / Service Unit ➔ Re-Shelving", 
            ha='center', va='center', fontsize=9, style='italic', color='#64748B')

    def draw_box(x, y, w, h, title, subtitle, details, color):
        rect_shadow = patches.FancyBboxPatch((x-w/2+0.05, y-h/2-0.05), w, h,
                                            boxstyle="round,pad=0.12,rounding_size=0.15",
                                            facecolor="#CBD5E1", edgecolor="none", alpha=0.5)
        ax.add_patch(rect_shadow)
        rect = patches.FancyBboxPatch((x-w/2, y-h/2), w, h,
                                      boxstyle="round,pad=0.12,rounding_size=0.15",
                                      facecolor=c_card_bg, edgecolor=color, linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x, y + h/2 - 0.28, title, ha='center', va='center', fontsize=9.5, fontweight='bold', color=c_blue)
        if subtitle:
            ax.text(x, y + h/2 - 0.55, subtitle, ha='center', va='center', fontsize=7.5, fontweight='bold', color=color)
        y_text = y + h/2 - 0.85
        for d in details:
            ax.text(x - w/2 + 0.25, y_text, d, ha='left', va='center', fontsize=7.2, color='#334155')
            y_text -= 0.26

    # 1. TOP HUB: RECORDS UNIT
    draw_box(7, 8.8, 9.5, 1.8, 
             "CENTRAL RECORDS UNIT (THE DISPERSAL HUB)",
             "Patient Arrival ➔ Fast Cloud Search ➔ Shelf Retrieval ➔ Direct Dispersal Out",
             ["• Patient arrives at reception (Walk-in, Review, Specialist Referral, or Emergency).",
              "• Records Officer queries Cloud E-Archive in <100ms; Screen displays Shelf Coordinate: MR-1A-A1-1.",
              "• Folder pulled from shelf; barcode scanned out; cloud logs: 'CHECKED OUT / IN TRANSIT'.",
              "• 1-Hour automated countdown starts: survey link triggers to patient mobile 60 mins post-scan.",
              "• RECORDS DISPERSES FOLDER DIRECTLY TO THE ASSIGNED CLINICAL OR SERVICE UNIT."],
             c_blue)

    # Dispersal Banner
    ax.text(7, 7.3, "▼ FOLDER DISPERSED DIRECTLY TO ANY OF THE 12 HOSPITAL UNITS (NO CASHIER BOTTLENECK) ▼", 
            ha='center', va='center', fontsize=8.2, fontweight='bold', color=c_sky,
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#F0F9FF", edgecolor="#BAE6FD", lw=1))

    # Downward Fan-out Arrows from Records to the 4 Groups
    ax.annotate('', xy=(2.0, 6.2), xytext=(5.2, 7.1),
                arrowprops=dict(arrowstyle="->", color=c_sky, lw=1.8, mutation_scale=12))
    ax.annotate('', xy=(5.3, 6.2), xytext=(6.5, 7.1),
                arrowprops=dict(arrowstyle="->", color=c_sky, lw=1.8, mutation_scale=12))
    ax.annotate('', xy=(8.7, 6.2), xytext=(7.5, 7.1),
                arrowprops=dict(arrowstyle="->", color=c_sky, lw=1.8, mutation_scale=12))
    ax.annotate('', xy=(12.0, 6.2), xytext=(8.8, 7.1),
                arrowprops=dict(arrowstyle="->", color=c_sky, lw=1.8, mutation_scale=12))

    # 2. THE 4 DISPERSAL GROUPS (Covering all 12 destination units)
    
    # Col 1: Intake & Finance (Account & Oral Diagnosis)
    draw_box(2.0, 4.4, 2.7, 3.4,
             "TRIAGE & FINANCE",
             "Intake / Billing Destination",
             ["• Oral Diagnosis Clinic",
              "  (General Triage / Intake)",
              "• Account (Cashier)",
              "  (Fee Payment / NHIS)",
              "",
              "— Nurse/Cashier scans",
              "  folder barcode on PWA",
              "— Custody confirmed",
              "— Direct clinical/cashier service",
              "— Non-blocking routing"],
             c_teal)

    # Col 2: Restorative & Training
    draw_box(5.3, 4.4, 2.7, 3.4,
             "RESTORATIVE CLINICS",
             "Operative / Training Units",
             ["• Cons. Clinic",
              "  (Restorative / Fillings)",
              "• Advance Cons. Clinic",
              "  (Crowns / Root Canals)",
              "• Student's Clinic",
              "  (Undergraduate Care)",
              "• Resident's Clinic",
              "  (Postgrad Multi-care)",
              "",
              "— Nurse scans on arrival",
              "— Treatment performed"],
             c_blue)

    # Col 3: Surgery & Specialist
    draw_box(8.7, 4.4, 2.7, 3.4,
             "SURGICAL & SPECIALTY",
             "Surgical / Specialist Units",
             ["• Consultant Surgery 1",
              "  (Extractions / Biopsies)",
              "• Consultant Surgery 2",
              "  (Maxillofacial / Trauma)",
              "• Periodontic Clinic",
              "  (Gum Health & Surgery)",
              "• Orthodontic (Braces)",
              "• Paedodontic (Children)",
              "",
              "— Nurse confirms custody",
              "— Procedure concluded"],
             c_amber)

    # Col 4: Imaging & Diagnostic
    draw_box(12.0, 4.4, 2.7, 3.4,
             "RADIOLOGY & IMAGING",
             "Diagnostic Destination",
             ["• X-Ray Department",
              "  (Radiography Unit)",
              "",
              "• Panoramic (OPG) Scans",
              "• Periapical & Bitewings",
              "",
              "— Staff logs scan time",
              "— Radiograph completed",
              "— Film linked to folder",
              "— Folder ready to return"],
             c_purple)

    # Convergence Banner
    ax.text(7, 2.05, "▲ CARE CONCLUDED AT ANY UNIT ➔ PHYSICAL FOLDER RETURNED TO CENTRAL RECORDS ROOM ▲", 
            ha='center', va='center', fontsize=8.2, fontweight='bold', color=c_green,
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#ECFDF5", edgecolor="#A7F3D0", lw=1))

    # Return Arrows from all 4 columns to convergence
    ax.annotate('', xy=(5.2, 2.25), xytext=(2.0, 2.55),
                arrowprops=dict(arrowstyle="->", color=c_green, lw=1.8, mutation_scale=12))
    ax.annotate('', xy=(6.5, 2.25), xytext=(5.3, 2.55),
                arrowprops=dict(arrowstyle="->", color=c_green, lw=1.8, mutation_scale=12))
    ax.annotate('', xy=(7.5, 2.25), xytext=(8.7, 2.55),
                arrowprops=dict(arrowstyle="->", color=c_green, lw=1.8, mutation_scale=12))
    ax.annotate('', xy=(8.8, 2.25), xytext=(12.0, 2.55),
                arrowprops=dict(arrowstyle="->", color=c_green, lw=1.8, mutation_scale=12))

    # 3. BOTTOM BOX: ARCHIVAL RETURN & RE-SHELVING
    draw_box(7, 0.9, 9.5, 1.6,
             "CENTRAL RECORDS ARCHIVE: RETURN SCAN & PHYSICAL RE-SHELVING",
             "Location: Records Room Check-In Desk",
             ["• Clinical Orderly returns treated folders back to the central Records Room.",
              "• Records Officer scans folder barcode: Status changes to 'RETURNED TO ARCHIVE'.",
              "• Folder physically restored to Shelf MR-1A-A1-1; chain of custody safely closed.",
              "• Cloud increments Dean's daily footfall counter & verifies 100% archival reconciliation."],
             c_green)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Hub-and-Spoke Flowchart created at: {output_path}")

def set_cell_background(cell, fill_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def build_word_document():
    doc_path = r"d:\MYCODING FILES\KORLEBU PROJECTS\UGDS_Phase2_Master_Project_Document.docx"
    img_flowchart = r"d:\MYCODING FILES\KORLEBU PROJECTS\ugds_folder_flowchart.png"

    create_flowchart_image(img_flowchart)

    doc = docx.Document()

    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

    color_navy = RGBColor(0, 56, 102)     # #003866
    color_sky = RGBColor(2, 132, 199)     # #0284C7
    color_charcoal = RGBColor(30, 41, 59) # #1E293B

    # Header without author metadata
    p_inst = doc.add_paragraph()
    p_inst.paragraph_format.space_after = Pt(2)
    r_inst = p_inst.add_run("UNIVERSITY OF GHANA DENTAL SCHOOL — KORLE BU TEACHING HOSPITAL")
    r_inst.font.name = "Calibri"
    r_inst.font.size = Pt(10.5)
    r_inst.font.bold = True
    r_inst.font.color.rgb = color_sky

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_after = Pt(4)
    r_title = p_title.add_run("Phase 2 Master System Specification & Strategic Blueprint")
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(22)
    r_title.font.bold = True
    r_title.font.color.rgb = color_navy

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(14)
    r_sub = p_sub.add_run("Cloud E-Archive, Hub-and-Spoke Folder Dispersal, Staff Barcode PWA & Enterprise Cloud Hosting")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(12)
    r_sub.font.italic = True
    r_sub.font.color.rgb = color_charcoal

    # Executive Mandate Callout Box
    table_box = doc.add_table(rows=1, cols=1)
    table_box.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_box.autofit = False
    table_box.columns[0].width = Inches(7.0)
    cell = table_box.cell(0, 0)
    set_cell_background(cell, "EFF6FF")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)

    p_box = cell.paragraphs[0]
    p_box.paragraph_format.space_after = Pt(0)
    p_box.paragraph_format.line_spacing = 1.15
    r_b1 = p_box.add_run("Strategic Executive Mandate: ")
    r_b1.font.bold = True
    r_b1.font.size = Pt(10)
    r_b1.font.color.rgb = color_navy
    r_b2 = p_box.add_run(
        "Following the successful completion of Phase 1 (125,042 patient records migrated to the cloud, live customer experience "
        "dashboard deployed, and automated birthday CRM active), Phase 2 transforms clinical records operations across the hospital. "
        "It permanently replaces the legacy desktop eArchive software (MySQL 5.0 on port 3307) with an accessible Cloud E-Archive, "
        "establishes a direct Hub-and-Spoke Dispersal Model where the Records Unit pulls folders and dispatches them straight to any "
        "of the 12 clinical and diagnostic departments without bottleneck delays, equips staff with a mobile-first Barcode Progressive "
        "Web App (PWA) to track custody in real time, feeds live daily patient footfall intelligence directly into executive management, "
        "and formalizes the dedicated annual cloud production hosting on Vercel and Neon PostgreSQL."
    )
    r_b2.font.size = Pt(10)
    r_b2.font.color.rgb = color_charcoal

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # SECTION 1: LEGACY AUDIT
    h1 = doc.add_heading(level=1)
    r = h1.add_run("1. Legacy System Audit & Decommissioning Rationale")
    r.font.color.rgb = color_navy

    p_leg = doc.add_paragraph()
    p_leg.paragraph_format.line_spacing = 1.15
    p_leg.paragraph_format.space_after = Pt(6)
    p_leg.add_run(
        "For over fifteen years, the hospital records room has operated on a single desktop computer running legacy Visual Basic "
        "eArchive software connected to a localized MySQL 5.0 database on port 3307. A thorough systems evaluation revealed "
        "four severe operational risks that make Phase 2 an urgent clinical priority:"
    )

    bullets_leg = [
        ("Single Point of Failure: ", "All 125,042 patient folder histories sit on a single physical workstation in the records room. A hard drive crash or malware attack would instantly paralyze records retrieval across the entire dental school."),
        ("Zero Clinical Custody: ", "Once a physical folder exits the records room, records officers have no digital visibility of where it is. If a specialist in Consultant Surgery 1 requires a folder currently sitting in Periodontics, staff waste hours manually searching clinic by clinic."),
        ("No Patient Journey History: ", "The legacy program stores static registration numbers but fails to record longitudinal visit timelines—when the patient arrived, which clinic treated them, and turnaround durations."),
        ("Administrative Blindspot: ", "Management has no automated, real-time counters of daily, weekly, or monthly patient visits, leaving departmental staffing and resource allocation to guesswork.")
    ]
    for b_title, b_desc in bullets_leg:
        p_b = doc.add_paragraph(style='List Bullet')
        p_b.paragraph_format.space_after = Pt(4)
        p_b.paragraph_format.line_spacing = 1.15
        r_bt = p_b.add_run(b_title)
        r_bt.font.bold = True
        r_bt.font.color.rgb = color_navy
        p_b.add_run(b_desc)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # SECTION 2: THE 13 CLINICAL UNITS
    h2 = doc.add_heading(level=1)
    r = h2.add_run("2. Central Records Dispersal & The 13 UGDS Clinical Units")
    r.font.color.rgb = color_navy

    p_unit = doc.add_paragraph()
    p_unit.paragraph_format.line_spacing = 1.15
    p_unit.paragraph_format.space_after = Pt(6)
    p_unit.add_run(
        "Phase 2 reflects authentic hospital workflow: the Records Unit acts as the Central Archival and Dispersal Hub. "
        "When a patient arrives (walk-in, review appointment, specialist referral, or emergency), their folder is pulled from "
        "the shelf and dispersed DIRECTLY to whichever clinic or service point the patient needs to visit:"
    )

    unit_table_data = [
        ("No.", "Unit / Service Point", "Departmental Function", "Direct Dispersal & Custody Role"),
        ("1", "Records Unit (Hub)", "Central Archival & Dispersal Hub", "Pulls folder from Shelf (MR-1A-A1-1); scans barcode out; disperses directly to destination unit; audits returns."),
        ("2", "Account (Cashier)", "Billing & Financial Clearance", "Verifies active patient consultation and fee/NHIS receipt where billing is required."),
        ("3", "Oral Diagnosis Clinic", "Primary Intake & Triage", "Receives triage patients directly; diagnoses and routes patient to specialized clinical care."),
        ("4", "Cons. Clinic", "Conservative & Operative Dentistry", "Receives folders directly for operative procedures, cavity restorations, and routine conservative care."),
        ("5", "Student's Clinic", "Undergraduate Training Facility", "Receives folders directly for dental students performing supervised clinical work."),
        ("6", "Advance Cons. Clinic", "Endodontics & Prosthodontics", "Receives folders directly for complex multi-visit root canals, crowns, and bridge restorations."),
        ("7", "Resident's Clinic", "Postgraduate Specialized Care", "Receives folders directly for advanced referral cases and resident clinical procedure logs."),
        ("8", "Periodontic Clinic", "Gum Health & Periodontology", "Receives folders directly for deep scaling, periodontal surgery, and bone-loss care."),
        ("9", "Paedodontic Clinic", "Child & Adolescent Dentistry", "Receives folders directly for specialized child dentistry, pulpotomies, and preventive sealants."),
        ("10", "Orthodontic Clinic", "Malocclusion & Alignment", "Receives folders directly for monthly brace adjustments and craniofacial orthopedics follow-ups."),
        ("11", "Consultant Surgery 1", "Oral & Maxillofacial Surgery 1", "Receives folders directly for surgical extractions, impactions, and soft-tissue biopsies."),
        ("12", "Consultant Surgery 2", "Oral & Maxillofacial Surgery 2", "Receives folders directly for facial trauma review and specialized surgical consultations."),
        ("13", "X-Ray (Radiology)", "Dental Imaging & Radiography", "Receives folders directly for periapical, bitewing, and panoramic (OPG) imaging scans.")
    ]

    t_units = doc.add_table(rows=len(unit_table_data), cols=4)
    t_units.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_units.autofit = False

    col_widths = [Inches(0.4), Inches(1.8), Inches(2.2), Inches(2.6)]
    for row_idx, row_data in enumerate(unit_table_data):
        row = t_units.rows[row_idx]
        for col_idx, text in enumerate(row_data):
            cell = row.cells[col_idx]
            cell.width = col_widths[col_idx]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.05
            
            if row_idx == 0:
                set_cell_background(cell, "003866")
                set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
                r = p.add_run(text)
                r.font.bold = True
                r.font.color.rgb = RGBColor(255, 255, 255)
                r.font.size = Pt(8.5)
            else:
                bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
                set_cell_background(cell, bg)
                set_cell_margins(cell, top=60, bottom=60, left=100, right=100)
                r = p.add_run(text)
                r.font.size = Pt(8)
                if col_idx == 1:
                    r.font.bold = True
                    r.font.color.rgb = color_navy

    doc.add_page_break()

    # SECTION 3: VISUAL HUB-AND-SPOKE DISPERSAL FLOWCHART
    h3 = doc.add_heading(level=1)
    r = h3.add_run("3. Central Records Dispersal & Custody Flowchart")
    r.font.color.rgb = color_navy

    p_flow = doc.add_paragraph()
    p_flow.paragraph_format.line_spacing = 1.15
    p_flow.paragraph_format.space_after = Pt(8)
    p_flow.add_run(
        "The diagram below illustrates the direct Hub-and-Spoke Dispersal architecture: the patient arrives at the Records Desk, "
        "the folder is pulled and barcode-scanned, and Records disperses it directly to whichever clinic or service point the patient "
        "is visiting. Once treatment is completed, the folder returns directly to Records for archival re-shelving:"
    )

    if os.path.exists(img_flowchart):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_after = Pt(12)
        p_img.add_run().add_picture(img_flowchart, width=Inches(6.9))

    doc.add_page_break()

    # SECTION 4: EXACT USER SCREENS & OPERATIONAL WORKFLOW (WHAT & HOW)
    h4 = doc.add_heading(level=1)
    r = h4.add_run("4. Operational Walkthrough: What Each User Sees & How It Operates")
    r.font.color.rgb = color_navy

    p_walk_intro = doc.add_paragraph()
    p_walk_intro.paragraph_format.line_spacing = 1.15
    p_walk_intro.paragraph_format.space_after = Pt(8)
    p_walk_intro.add_run(
        "To ensure leadership and hospital staff visualize exactly how Phase 2 operates in daily hospital life, "
        "here is the breakdown of the interfaces, screens, and actions across each operational role:"
    )

    roles_walkthrough = [
        ("A. For the Records Officer (At the Central Records Desk)",
         "Screen Interface: Cloud E-Archive Desk (/archive)\n"
         "• Exact View: A high-speed search bar with live filtering across 125,042 patient records.\n"
         "• What Appears: When the officer types the folder number (e.g., 'K/13 5622') or patient name, the system instantly renders a prominent Shelf Coordinate Badge:\n"
         "      [ RACK: 1A  |  BAY: 1  |  SHELF: A1  |  SLOT: 1 ]\n"
         "• Action: The officer taps 'Check-Out', selects the destination clinic (e.g. Cons. Clinic, Surgery, Orthodontics, or Cashier), and scans the folder barcode.\n"
         "• Cloud Result: Status updates instantly to 'CHECKED OUT / IN TRANSIT'. The folder is dispersed directly to that clinic without manual paper ledgers."),

        ("B. For the Clinic Nurse & Dental Assistant (In Any of the Destination Clinics)",
         "Screen Interface: Staff Mobile Progressive Web App (PWA)\n"
         "• Exact View: A mobile-first web app installed on clinic smartphones, tablets, or workstation browsers.\n"
         "• Authentication: The nurse signs in with their staff PIN and selects their active clinic unit (e.g. 'Nurse Grace — Cons. Clinic').\n"
         "• What Appears: A live camera scanning viewfinder with a single button: 'Scan Arriving Folder'.\n"
         "• Action: When the folder arrives at the clinic door, the nurse points the camera at the folder barcode. The screen flashes green:\n"
         "      'Folder K/13 5622 Confirmed: In Custody at Cons. Clinic at 09:42 AM'\n"
         "• Cloud Result: Custody is digitally transferred in 0.2 seconds. The records room and executive dashboard immediately see the folder is safely in that clinic."),

        ("C. For the Dean & Executive Leadership (On the Master Dashboard)",
         "Screen Interface: Executive Overview Dashboard\n"
         "• Exact View: Real-time clinical KPI overview updating dynamically without manual compilation.\n"
         "• Metric 1 — Live Daily Footfall Counter: Displays the verified total of patients who visited the dental school today, this week, and this month.\n"
         "• Metric 2 — Departmental Workload Heatmap: A live bar chart displaying how many folders are currently sitting in each of the 13 clinical units.\n"
         "• Metric 3 — Patient Longitudinal Route: Clicking any patient displays their complete journey timeline for the day:\n"
         "      '08:15 AM: Arrival at Records ➔ Dispersed to Consultant Surgery 1 ➔ 08:40 AM: Custody Confirmed ➔ 10:15 AM: Re-shelved in Records'.")
    ]

    for r_title, r_desc in roles_walkthrough:
        h_r = doc.add_heading(level=2)
        r_rh = h_r.add_run(r_title)
        r_rh.font.color.rgb = color_sky
        r_rh.font.size = Pt(11)
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(8)
        p.add_run(r_desc)

    p_day_title = doc.add_paragraph()
    p_day_title.paragraph_format.space_after = Pt(4)
    r_day = p_day_title.add_run("A Typical Day in the Hospital (End-to-End Workflow):")
    r_day.font.bold = True
    r_day.font.size = Pt(10.5)
    r_day.font.color.rgb = color_navy

    daily_steps = [
        ("07:30 AM — Morning Pulls & Dispersal: ", "Records officers open /archive, query scheduled and arriving patients, pull physical folders from shelf coordinates, scan them out, and disperse them directly to the assigned clinics. The checkout scan arms an automated 60-minute cloud countdown for the patient's survey."),
        ("08:30 AM to 02:00 PM — Direct Clinic Arrival & Care: ", "Orderlies deliver folders directly to destination clinics. Nurses scan on arrival via the Staff PWA. Custody is confirmed in real time across the dental school without cashier delays."),
        ("60 Minutes Post-Checkout Scan — Automated Follow-up Survey: ", "Exactly one hour after the folder was first scanned at Records, the cloud engine dispatches the personalized 1-credit survey SMS: 'UGDS FEEDBACK: Dear {name}, thank you for visiting UGDS. Please rate your experience: {link}'. The patient receives it right as care is completing."),
        ("02:30 PM to 04:30 PM — Archival Check-In & Physical Re-Shelving: ", "Treated folders are returned from clinics back to the central records room. The records officer scans each folder back in, confirming safe return, and restores it to its physical shelf slot."),
        ("04:35 PM — Executive Attendance & Quality Reconciliation: ", "The Dean and management review the live dashboard, displaying verified daily patient footfall, clinic workload distribution, and real-time patient satisfaction ratings.")
    ]
    for d_title, d_desc in daily_steps:
        p_d = doc.add_paragraph(style='List Bullet')
        p_d.paragraph_format.space_after = Pt(4)
        p_d.paragraph_format.line_spacing = 1.15
        r_dt = p_d.add_run(d_title)
        r_dt.font.bold = True
        r_dt.font.color.rgb = color_navy
        p_d.add_run(d_desc)

    doc.add_page_break()

    # SECTION 5: THE PATIENT JOURNEY NARRATIVE STORY
    h5_story = doc.add_heading(level=1)
    r_story = h5_story.add_run("5. The Patient Journey: A Day with Mr. Kwesi Mensah at UGDS Dental School")
    r_story.font.color.rgb = color_navy

    p_story_intro = doc.add_paragraph()
    p_story_intro.paragraph_format.line_spacing = 1.15
    p_story_intro.paragraph_format.space_after = Pt(8)
    p_story_intro.add_run(
        "To understand how Phase 2 transforms the clinical atmosphere for both patients and healthcare workers, "
        "we follow the end-to-end hospital experience of Mr. Kwesi Mensah, a 48-year-old civil servant visiting "
        "the University of Ghana Dental School for his scheduled crown restoration:"
    )

    story_steps = [
        ("1. 08:00 AM — Patient Arrival & Reception: ",
         "Mr. Kwesi Mensah arrives at the UGDS reception desk. He gives his name and folder number (K/13 5622) to the front desk records officer."),

        ("2. 08:01 AM — Sub-Second Cloud Shelf Coordinate: ",
         "The records officer types 'K/13 5622' into the Cloud E-Archive desk (/archive). In less than 100 milliseconds, the screen highlights Mr. Mensah's exact physical shelf location: [ RACK: 1A | BAY: 2 | SHELF: B1 | SLOT: 8 ]. There is no flipping through paper ledgers or searching disorganized desktop windows."),

        ("3. 08:03 AM — Direct Dispersal & Survey Countdown Armed: ",
         "The officer walks to Shelf 1A-2-B1-8, retrieves the physical paper folder, and scans the barcode on the counter scanner. He selects 'Disperse to: Cons. Clinic'. Status updates hospital-wide to 'IN TRANSIT'. At this exact second, the cloud engine arms an automated 60-minute background timer linked to Mr. Mensah's mobile phone."),

        ("4. 08:15 AM — Arrival at Clinic & 0.2-Second Custody Scan: ",
         "An orderly transports the folder directly to the Conservative Clinic. At the doorway, Nurse Grace pulls out her smartphone, opens the Staff Barcode PWA, and taps the camera scanner on the folder barcode. Her screen chimes green: 'Folder K/13 5622 Confirmed: In Custody at Cons. Clinic at 08:15 AM'. The records room instantly sees that the folder has safely reached Nurse Grace."),

        ("5. 08:30 AM — Consultation & Restorative Treatment: ",
         "Dr. Boateng welcomes Mr. Mensah into the dental chair, reviews his historical treatment notes, and performs the crown fitting and polishing. Clinical care proceeds smoothly with full physical records in hand."),

        ("6. 09:03 AM — The 1-Hour Automated Feedback Prompt: ",
         "Exactly 60 minutes after the initial records scan, as Mr. Mensah is rinsing and Dr. Boateng is completing his clinical notes, Mr. Mensah's phone buzzes with a personalized SMS:\n"
         "      'UGDS FEEDBACK: Dear Kwesi, thank you for visiting UGDS. Please rate your experience: https://ugds-feedback.vercel.app/s/7x9q'\n"
         "Because the visit is fresh in his mind, Mr. Mensah taps the link on his phone, rates his experience 5 stars, praises the quick retrieval time, and submits the survey in 20 seconds."),

        ("7. 09:15 AM — Non-Blocking Service Clearance: ",
         "Mr. Mensah steps over to the Account / Cashier desk for fee payment. Because cashiering is an independent service point in the dispersal model, the cashier pulls up his active session, clears payment in 90 seconds, and hands him his receipt. Mr. Mensah departs the hospital pleased and satisfied."),

        ("8. 02:30 PM — Archival Return & Physical Re-Shelving: ",
         "At the close of clinical sessions, the orderly returns the day's treated folders to the Central Records Room. The records officer scans Mr. Mensah's folder back in: status switches to 'RETURNED TO ARCHIVE'. The officer returns the folder to its precise coordinate [ RACK: 1A | BAY: 2 | SHELF: B1 | SLOT: 8 ]. 100% of folders are accounted for."),

        ("9. 04:00 PM — Executive Leadership Oversight: ",
         "In his office, the Dean opens the Executive Dashboard. He sees that 192 patients were attended to today across all 13 clinics, zero folders are missing or unaccounted for, and Mr. Mensah's 5-star rating has been integrated into the hospital's live patient satisfaction score.")
    ]

    for s_title, s_desc in story_steps:
        p_s = doc.add_paragraph()
        p_s.paragraph_format.line_spacing = 1.15
        p_s.paragraph_format.space_after = Pt(6)
        r_st = p_s.add_run(s_title)
        r_st.font.bold = True
        r_st.font.color.rgb = color_navy
        p_s.add_run(s_desc)

    doc.add_page_break()

    # SECTION 6: ANNUAL CLOUD PRODUCTION PACKAGE (VERCEL + NEON)
    h6 = doc.add_heading(level=1)
    r = h6.add_run("6. Annual Enterprise Cloud Infrastructure Package (Vercel + Neon PostgreSQL)")
    r.font.color.rgb = color_navy

    p_infra = doc.add_paragraph()
    p_infra.paragraph_format.line_spacing = 1.15
    p_infra.paragraph_format.space_after = Pt(8)
    p_infra.add_run(
        "To ensure 100% operational reliability, zero downtime, and seamless performance across all 13 clinical departments, "
        "Phase 2 moves from temporary developer environments to a formal, dedicated Annual Enterprise Cloud Package. "
        "The hospital will budget directly for the official production packages on Vercel and Neon PostgreSQL:"
    )

    infra_table_data = [
        ("Cloud Component", "Provider & Tier", "Hospital Operational Purpose", "Enterprise Safeguards & Benefits"),
        ("Frontend & API Gateway", "Vercel Production Pro", "Hosts Customer Experience Portal, E-Archive Desk, and Serverless API.", "99.99% SLA uptime, high-speed regional CDN, custom UGDS domain with automated SSL, serverless scalability."),
        ("Central Database Repository", "Neon PostgreSQL Production", "Stores all 125,042 patient records, real-time folder movement logs, and staff data.", "Dedicated compute, automated point-in-time recovery (daily backups), connection pooling for all 13 clinics simultaneously."),
        ("Staff Mobile PWA", "Vercel PWA / Edge Cache", "Delivers the mobile camera barcode scanner to all clinic staff phones and tablets.", "Instant mobile loading, offline caching support, zero app store installation friction for nurses and assistants.")
    ]

    t_infra = doc.add_table(rows=len(infra_table_data), cols=4)
    t_infra.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_infra.autofit = False
    col_widths_infra = [Inches(1.5), Inches(1.5), Inches(2.2), Inches(1.8)]

    for row_idx, row_data in enumerate(infra_table_data):
        row = t_infra.rows[row_idx]
        for col_idx, text in enumerate(row_data):
            cell = row.cells[col_idx]
            cell.width = col_widths_infra[col_idx]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.05

            if row_idx == 0:
                set_cell_background(cell, "003866")
                set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
                r = p.add_run(text)
                r.font.bold = True
                r.font.color.rgb = RGBColor(255, 255, 255)
                r.font.size = Pt(8.5)
            else:
                bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
                set_cell_background(cell, bg)
                set_cell_margins(cell, top=60, bottom=60, left=100, right=100)
                r = p.add_run(text)
                r.font.size = Pt(8)
                if col_idx == 0:
                    r.font.bold = True
                    r.font.color.rgb = color_navy

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    p_why = doc.add_paragraph()
    p_why.paragraph_format.line_spacing = 1.15
    p_why.paragraph_format.space_after = Pt(6)
    r_whyt = p_why.add_run("Why the Annual Cloud Package is Essential for Hospital Leadership:")
    r_whyt.font.bold = True
    r_whyt.font.color.rgb = color_navy
    
    why_points = [
        ("Zero On-Premise Server Risk: ", "Eliminates the need for expensive physical server rooms, UPS batteries, and on-site hardware maintenance at Korle Bu. The database is shielded from power outages and local hardware crashes."),
        ("Automated Daily Backups: ", "Neon PostgreSQL provides continuous point-in-time recovery. Patient records and folder movement logs are continuously backed up and recoverable to the exact second."),
        ("Multi-Clinic Concurrent Access: ", "Built-in connection pooling ensures that all 13 clinical departments and the records room can search, scan, and retrieve records simultaneously without system slowdowns.")
    ]
    for w_title, w_desc in why_points:
        p_w = doc.add_paragraph(style='List Bullet')
        p_w.paragraph_format.space_after = Pt(4)
        p_w.paragraph_format.line_spacing = 1.15
        r_wt = p_w.add_run(w_title)
        r_wt.font.bold = True
        r_wt.font.color.rgb = color_navy
        p_w.add_run(w_desc)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # SECTION 7: IMPLEMENTATION ROADMAP
    h7 = doc.add_heading(level=1)
    r = h7.add_run("7. Implementation Phasing & 4-Week Technical Rollout")
    r.font.color.rgb = color_navy

    roadmap_data = [
        ("Sprint / Week", "Focus & Strategic Milestones", "Key Technical Deliverables", "Target Window"),
        ("Sprint 1 (Week 1)", "On-Site Daemon & Annual Cloud Setup", "Configure on-site daemon at Records PC (C:\\eArchive_Bible); activate Vercel Pro & Neon production packages; ingest 134 staff.", "Sprint 1"),
        ("Sprint 2 (Week 2)", "Cloud E-Archive Records Desk", "Deploy /archive module; sub-100ms 125k search; physical shelf locator; decommission legacy desktop MySQL 5.0.", "Sprint 2"),
        ("Sprint 3 (Week 3)", "Staff Barcode PWA Deployment", "Launch camera barcode PWA; roll out 1-tap check-in/out across Oral Diagnosis, Cons. Clinic, and Surgery.", "Sprint 3"),
        ("Sprint 4 (Week 4)", "Executive Analytics & Staff Handover", "Connect live visit footfall counters to Phase 1 Dashboard; conduct nursing staff training; executive leadership review.", "Sprint 4")
    ]

    t_road = doc.add_table(rows=len(roadmap_data), cols=4)
    t_road.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_road.autofit = False
    col_widths_road = [Inches(1.2), Inches(1.8), Inches(2.8), Inches(1.2)]

    for row_idx, row_data in enumerate(roadmap_data):
        row = t_road.rows[row_idx]
        for col_idx, text in enumerate(row_data):
            cell = row.cells[col_idx]
            cell.width = col_widths_road[col_idx]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.05

            if row_idx == 0:
                set_cell_background(cell, "003866")
                set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
                r = p.add_run(text)
                r.font.bold = True
                r.font.color.rgb = RGBColor(255, 255, 255)
                r.font.size = Pt(8.5)
            else:
                bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
                set_cell_background(cell, bg)
                set_cell_margins(cell, top=60, bottom=60, left=100, right=100)
                r = p.add_run(text)
                r.font.size = Pt(8)
                if col_idx == 0:
                    r.font.bold = True
                    r.font.color.rgb = color_navy

    doc.add_paragraph().paragraph_format.space_after = Pt(14)

    p_concl = doc.add_paragraph()
    p_concl.paragraph_format.line_spacing = 1.15
    r_ct = p_concl.add_run("Conclusion & Technical Readiness: ")
    r_ct.font.bold = True
    r_ct.font.color.rgb = color_navy
    p_concl.add_run(
        "Phase 2 establishes a modern, resilient foundation for the University of Ghana Dental School. "
        "By replacing legacy desktop software with high-availability cloud infrastructure (Vercel + Neon), "
        "empowering clinic staff with barcode scanning on their existing mobile devices, and providing executive "
        "leadership with real-time patient footfall intelligence, the hospital achieves full digital custody and operational excellence."
    )

    doc.save(doc_path)
    print(f"Phase 2 Word Document updated at: {doc_path}")

if __name__ == "__main__":
    build_word_document()
