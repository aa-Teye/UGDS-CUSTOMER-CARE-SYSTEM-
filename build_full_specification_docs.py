import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

# -------------------------------------------------------------
# 1. CREATE 300-DPI HIGH-RES FLOWCHART
# -------------------------------------------------------------
def create_flowchart_image(output_path):
    fig, ax = plt.subplots(figsize=(14, 11), dpi=300)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 11)
    ax.axis('off')

    c_blue = "#003866"       # UGDS Navy Blue
    c_sky = "#0284C7"        # Medical Sky Blue
    c_teal = "#0D9488"       # Teal
    c_amber = "#D97706"      # Amber
    c_purple = "#7C3AED"     # Purple
    c_green = "#059669"      # Emerald Green
    c_card_bg = "#F8FAFC"    # Slate Light

    # Header
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
    draw_box(7, 8.8, 9.8, 1.85, 
             "CENTRAL RECORDS UNIT (THE DISPERSAL HUB)",
             "Patient Arrival / Pre-Load ➔ Fast Search ➔ Shelf Retrieval ➔ Scan & Dispatch Out",
             ["• Pre-loaded morning pull list ready at 07:30 AM; walk-ins queried sub-100ms on /archive.",
              "• Exact Shelf Coordinate displayed instantly: [ RACK: 1A | BAY: 1 | SHELF: A1 | SLOT: 1 ].",
              "• Folder pulled, barcode scanned, and destination selected. Status: 'CHECKED OUT / IN TRANSIT'.",
              "• 60-Minute background countdown arms automatically: survey triggers to patient phone in 1 hour.",
              "• RECORDS DISPERSES FOLDER DIRECTLY TO ASSIGNED CLINIC OR SERVICE UNIT."],
             c_blue)

    # Dispersal Banner
    ax.text(7, 7.3, "▼ FOLDER DISPERSED DIRECTLY TO ANY OF THE 12 HOSPITAL UNITS (NO CASHIER BOTTLENECK) ▼", 
            ha='center', va='center', fontsize=8.2, fontweight='bold', color=c_sky,
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#F0F9FF", edgecolor="#BAE6FD", lw=1))

    # Fan-out arrows
    ax.annotate('', xy=(2.0, 6.2), xytext=(5.2, 7.1),
                arrowprops=dict(arrowstyle="->", color=c_sky, lw=1.8, mutation_scale=12))
    ax.annotate('', xy=(5.3, 6.2), xytext=(6.5, 7.1),
                arrowprops=dict(arrowstyle="->", color=c_sky, lw=1.8, mutation_scale=12))
    ax.annotate('', xy=(8.7, 6.2), xytext=(7.5, 7.1),
                arrowprops=dict(arrowstyle="->", color=c_sky, lw=1.8, mutation_scale=12))
    ax.annotate('', xy=(12.0, 6.2), xytext=(8.8, 7.1),
                arrowprops=dict(arrowstyle="->", color=c_sky, lw=1.8, mutation_scale=12))

    # Col 1: Triage & Finance
    draw_box(2.0, 4.4, 2.7, 3.4,
             "TRIAGE & FINANCE",
             "Intake / Billing Destination",
             ["• Oral Diagnosis Clinic",
              "  (General Triage / Intake)",
              "• Account (Cashier)",
              "  (Fee Payment / NHIS)",
              "",
              "— Staff/Nurse scans",
              "  barcode via Mobile PWA",
              "— Custody confirmed in 0.2s",
              "— Live queue display updates",
              "— Offline-first local TXT sync"],
             c_teal)

    # Col 2: Restorative & Training
    draw_box(5.3, 4.4, 2.7, 3.4,
             "RESTORATIVE CLINICS",
             "Operative / Training Units",
             ["• Cons. Clinic",
              "  (Restorative / Fillings)",
              "• Advance Cons. Clinic",
              "  (Crowns / Root Canals)",
              "• Students Clinic",
              "  (Undergraduate Care)",
              "• Residents Clinic",
              "  (Postgrad Multi-care)",
              "",
              "— Nurse scans on arrival",
              "— Live clinic queue updates",
              "— Procedure conducted"],
             c_blue)

    # Col 3: Surgical & Specialty
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
              "— In Treatment status logged",
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
              "— Staff logs scan arrival",
              "— Radiograph completed",
              "— Film linked to folder",
              "— Folder ready to return"],
             c_purple)

    # Convergence Banner
    ax.text(7, 2.05, "▲ CARE CONCLUDED AT ANY UNIT ➔ PHYSICAL FOLDER RETURNED TO CENTRAL RECORDS ROOM ▲", 
            ha='center', va='center', fontsize=8.2, fontweight='bold', color=c_green,
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#ECFDF5", edgecolor="#A7F3D0", lw=1))

    # Return Arrows
    ax.annotate('', xy=(5.2, 2.25), xytext=(2.0, 2.55),
                arrowprops=dict(arrowstyle="->", color=c_green, lw=1.8, mutation_scale=12))
    ax.annotate('', xy=(6.5, 2.25), xytext=(5.3, 2.55),
                arrowprops=dict(arrowstyle="->", color=c_green, lw=1.8, mutation_scale=12))
    ax.annotate('', xy=(7.5, 2.25), xytext=(8.7, 2.55),
                arrowprops=dict(arrowstyle="->", color=c_green, lw=1.8, mutation_scale=12))
    ax.annotate('', xy=(8.8, 2.25), xytext=(12.0, 2.55),
                arrowprops=dict(arrowstyle="->", color=c_green, lw=1.8, mutation_scale=12))

    # 3. BOTTOM BOX: ARCHIVE RETURN
    draw_box(7, 0.9, 9.8, 1.6,
             "CENTRAL RECORDS ARCHIVE: RETURN SCAN & PHYSICAL RE-SHELVING",
             "Location: Records Room Check-In Desk",
             ["• Orderly returns completed folders back to the central Records Room.",
              "• Records Officer scans folder barcode: Status switches to 'RETURNED TO ARCHIVE'.",
              "• Folder physically re-shelved in Shelf Slot (e.g. MR-1A-A1-1); chain of custody safely closed.",
              "• Cloud increments Dean's verified daily footfall counter & reconciles 100% of day's folders."],
             c_green)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Flowchart created at: {output_path}")


# -------------------------------------------------------------
# 2. HELPER FUNCTIONS FOR WORD DOCUMENT (.DOCX)
# -------------------------------------------------------------
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

def add_callout_box(doc, text_runs, bg_hex="EFF6FF", border_hex="0284C7"):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = Inches(7.0)
    cell = table.cell(0, 0)
    set_cell_background(cell, bg_hex)
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
    
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="none"/>'
        f'<w:left w:val="single" w:sz="36" w:space="0" w:color="{border_hex}"/>'
        f'<w:bottom w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)

    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.15
    for txt, bold, italic, color_rgb, size_pt in text_runs:
        r = p.add_run(txt)
        r.bold = bold
        r.italic = italic
        r.font.size = Pt(size_pt)
        r.font.color.rgb = color_rgb

def create_styled_table(doc, data, col_widths, navy_rgb, charcoal_rgb):
    table = doc.add_table(rows=len(data), cols=len(col_widths))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    for row_idx, row_data in enumerate(data):
        row = table.rows[row_idx]
        for col_idx, text in enumerate(row_data):
            cell = row.cells[col_idx]
            cell.width = Inches(col_widths[col_idx])
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.1

            if row_idx == 0:
                set_cell_background(cell, "003866")
                set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
                r = p.add_run(text)
                r.bold = True
                r.font.color.rgb = RGBColor(255, 255, 255)
                r.font.size = Pt(8.5)
            else:
                bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
                set_cell_background(cell, bg)
                set_cell_margins(cell, top=60, bottom=60, left=100, right=100)
                r = p.add_run(text)
                r.font.size = Pt(8.5)
                if col_idx == 0 and len(col_widths) > 2:
                    r.font.color.rgb = navy_rgb
                elif col_idx == 0 and len(col_widths) <= 2:
                    r.bold = True
                    r.font.color.rgb = navy_rgb
                elif col_idx == 1 and len(col_widths) > 2:
                    r.bold = True
                    r.font.color.rgb = navy_rgb
                else:
                    r.font.color.rgb = charcoal_rgb

    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    return table


# -------------------------------------------------------------
# 3. BUILD COMPLETE WORD DOCUMENT (.DOCX)
# -------------------------------------------------------------
def build_word_document(doc_path, img_flowchart):
    doc = docx.Document()

    for s in doc.sections:
        s.top_margin = Inches(0.7)
        s.bottom_margin = Inches(0.7)
        s.left_margin = Inches(0.7)
        s.right_margin = Inches(0.7)

    c_navy = RGBColor(0, 56, 102)     # #003866
    c_sky = RGBColor(2, 132, 199)     # #0284C7
    c_charcoal = RGBColor(30, 41, 59) # #1E293B

    # Header section
    p_inst = doc.add_paragraph()
    p_inst.paragraph_format.space_after = Pt(2)
    r_inst = p_inst.add_run("UNIVERSITY OF GHANA DENTAL SCHOOL")
    r_inst.font.name = "Calibri"
    r_inst.font.size = Pt(13)
    r_inst.bold = True
    r_inst.font.color.rgb = c_navy

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_after = Pt(4)
    r_title = p_title.add_run("Phase 2 — Master System Specification & Strategic Blueprint")
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(20)
    r_title.bold = True
    r_title.font.color.rgb = c_navy

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(3)
    r_sub = p_sub.add_run("Cloud E-Archive  |  Hub-and-Spoke Dispersal  |  Barcode PWA  |  Executive Dashboard")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(11)
    r_sub.bold = True
    r_sub.font.color.rgb = c_sky

    p_phase1 = doc.add_paragraph()
    p_phase1.paragraph_format.space_after = Pt(14)
    r_p1 = p_phase1.add_run("Built on Phase 1: 125,042 patient records migrated  |  Live CRM dashboard  |  Automated birthday messaging")
    r_p1.font.name = "Calibri"
    r_p1.font.size = Pt(9.5)
    r_p1.italic = True
    r_p1.font.color.rgb = c_charcoal

    # Executive Summary Heading
    h_exec = doc.add_heading(level=1)
    r_exh = h_exec.add_run("EXECUTIVE SUMMARY")
    r_exh.font.color.rgb = c_navy

    p_exec1 = doc.add_paragraph()
    p_exec1.paragraph_format.line_spacing = 1.15
    p_exec1.paragraph_format.space_after = Pt(6)
    p_exec1.add_run(
        "Phase 2 transforms clinical records operations at the University of Ghana Dental School. Building on Phase 1 — "
        "which migrated 125,042 patient records to the cloud and deployed a live CRM dashboard — Phase 2 permanently replaces "
        "the 15-year-old legacy desktop eArchive software with a cloud-native system that gives every stakeholder in the hospital "
        "real-time visibility of every patient folder, from the moment it is pulled from the shelf to the moment it is returned."
    )

    p_exec2 = doc.add_paragraph()
    p_exec2.paragraph_format.line_spacing = 1.15
    p_exec2.paragraph_format.space_after = Pt(8)
    p_exec2.add_run(
        "The system is built around a single core principle: "
    )
    r_principle = p_exec2.add_run("one scan, one destination selection, and everything updates everywhere simultaneously — ")
    r_principle.bold = True
    p_exec2.add_run("the clinic queue, the records room, and the executive dashboard.")

    # Callout: X-Ray patients
    add_callout_box(doc, [
        ("Out of Scope Notice: ", True, False, c_navy, 9.5),
        ("X-Ray patients (who do not have folders) are captured as a future user requirement and are out of scope for Phase 2. "
         "They will be addressed as a standalone lightweight check-in module in a subsequent phase.", False, True, c_charcoal, 9.0)
    ], bg_hex="EFF6FF", border_hex="0284C7")

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # 1. WHY PHASE 2: THE LEGACY SYSTEM PROBLEM
    h1 = doc.add_heading(level=1)
    r1 = h1.add_run("1. WHY PHASE 2: THE LEGACY SYSTEM PROBLEM")
    r1.font.color.rgb = c_navy

    p_why = doc.add_paragraph()
    p_why.paragraph_format.line_spacing = 1.15
    p_why.paragraph_format.space_after = Pt(6)
    p_why.add_run(
        "For over fifteen years, all 125,042 patient folder histories have lived on a single desktop PC running Visual Basic "
        "eArchive software connected to a local MySQL 5.0 database on port 3307. This creates four critical operational risks:"
    )

    table_risks = [
        ("Risk", "Impact"),
        ("Single Point of Failure", "One hard drive crash or malware attack instantly paralyses records retrieval across all 13 departments."),
        ("Zero Clinical Custody", "Once a folder leaves the records room, no one knows where it is. Staff waste hours searching clinic by clinic."),
        ("No Patient Journey History", "The legacy system stores registration numbers only. It cannot record when a patient arrived, which clinic treated them, or how long they waited."),
        ("Management Blindspot", "The Dean and leadership have no real-time counters of daily patient visits, forcing staffing decisions based on guesswork.")
    ]
    create_styled_table(doc, table_risks, [2.2, 4.8], c_navy, c_charcoal)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # 2. THE 13 UGDS CLINICAL UNITS
    h2 = doc.add_heading(level=1)
    r2 = h2.add_run("2. THE 13 UGDS CLINICAL UNITS")
    r2.font.color.rgb = c_navy

    p_units = doc.add_paragraph()
    p_units.paragraph_format.line_spacing = 1.15
    p_units.paragraph_format.space_after = Pt(6)
    p_units.add_run(
        "The Records Unit acts as the Central Archival and Dispersal Hub. All 12 clinical and service departments are spokes "
        "that receive folders directly from Records and return them directly to Records after treatment:"
    )

    table_units = [
        ("No.", "Unit", "Function", "Role in Dispersal Model"),
        ("1", "Records Unit (Hub)", "Central Archival & Dispersal", "Pulls folders; scans out; selects destination; audits all returns."),
        ("2", "Account (Cashier)", "Billing & Financial Clearance", "Independent service point; does not block clinical flow."),
        ("3", "Oral Diagnosis Clinic", "Primary Intake & Triage", "Receives and routes new patients to specialist care."),
        ("4", "Cons. Clinic", "Conservative & Operative Dentistry", "Receives folders for restorations and routine care."),
        ("5", "Students Clinic", "Undergraduate Training", "Receives folders for supervised student clinical work."),
        ("6", "Advance Cons. Clinic", "Endodontics & Prosthodontics", "Receives folders for root canals, crowns, and bridges."),
        ("7", "Residents Clinic", "Postgraduate Specialized Care", "Receives folders for advanced referral cases."),
        ("8", "Periodontic Clinic", "Gum Health & Periodontology", "Receives folders for scaling, surgery, and bone-loss care."),
        ("9", "Paedodontic Clinic", "Child & Adolescent Dentistry", "Receives folders for child dentistry and preventive care."),
        ("10", "Orthodontic Clinic", "Malocclusion & Alignment", "Receives folders for brace adjustments and follow-ups."),
        ("11", "Consultant Surgery 1", "Oral & Maxillofacial Surgery", "Receives folders for surgical extractions and biopsies."),
        ("12", "Consultant Surgery 2", "Oral & Maxillofacial Surgery", "Receives folders for facial trauma and surgical consultations."),
        ("13", "X-Ray (Radiology)", "Dental Imaging", "Receives folders for periapical, bitewing, and OPG imaging.")
    ]
    create_styled_table(doc, table_units, [0.4, 2.0, 2.2, 2.4], c_navy, c_charcoal)

    doc.add_page_break()

    # Flowchart insert
    h_flow = doc.add_heading(level=2)
    rf = h_flow.add_run("Central Records Dispersal & Custody Flowchart")
    rf.font.color.rgb = c_sky
    rf.font.size = Pt(13)

    p_flow_txt = doc.add_paragraph()
    p_flow_txt.paragraph_format.line_spacing = 1.15
    p_flow_txt.paragraph_format.space_after = Pt(8)
    p_flow_txt.add_run(
        "The diagram below illustrates the direct Hub-and-Spoke Dispersal architecture: Records pulls from shelf coordinates, "
        "scans out to any of the 12 destination units, arming the 60-minute patient survey, and converges back to Records for re-shelving:"
    )

    if os.path.exists(img_flowchart):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_after = Pt(12)
        p_img.add_run().add_picture(img_flowchart, width=Inches(6.8))

    doc.add_page_break()

    # 3. THE SEVEN SYSTEM COMPONENTS
    h3 = doc.add_heading(level=1)
    r3 = h3.add_run("3. THE SEVEN SYSTEM COMPONENTS")
    r3.font.color.rgb = c_navy

    # 3.1 Cloud E-Archive
    h3_1 = doc.add_heading(level=2)
    r3_1 = h3_1.add_run("3.1 Cloud E-Archive — Records Desk Interface")
    r3_1.font.color.rgb = c_sky
    r3_1.font.size = Pt(11)

    p_3_1 = doc.add_paragraph()
    p_3_1.paragraph_format.line_spacing = 1.15
    p_3_1.paragraph_format.space_after = Pt(4)
    p_3_1.add_run("The records officer's primary interface. Replaces the legacy desktop software entirely.")

    t_3_1 = [
        ("Feature", "Detail"),
        ("Patient Search", "Sub-100ms search across all 125,042 records by folder number or patient name."),
        ("Shelf Coordinate Locator", "Instantly displays the exact physical location: RACK | BAY | SHELF | SLOT so the officer walks directly to the right shelf."),
        ("Scan & Dispatch", "Officer scans the folder barcode, selects the destination clinic from a dropdown. One action triggers everything."),
        ("Status Tracking", "Folder status updates hospital-wide: PULLED / IN TRANSIT / IN CUSTODY / RETURNED TO ARCHIVE.")
    ]
    create_styled_table(doc, t_3_1, [2.2, 4.8], c_navy, c_charcoal)

    # 3.2 Morning Pre-Load & Pull List
    h3_2 = doc.add_heading(level=2)
    r3_2 = h3_2.add_run("3.2 Morning Pre-Load & Pull List — Appointment Scheduling")
    r3_2.font.color.rgb = c_sky
    r3_2.font.size = Pt(11)

    p_3_2 = doc.add_paragraph()
    p_3_2.paragraph_format.line_spacing = 1.15
    p_3_2.paragraph_format.space_after = Pt(4)
    p_3_2.add_run("Every patient at UGDS falls into one of two categories:")

    t_3_2 = [
        ("Patient Type", "How They Are Handled"),
        ("Appointment Patient", "Has a pre-booked session with a specific doctor. Their folder is pre-loaded into the system the night before or early morning so Records can prepare the morning pull list in advance."),
        ("Walk-in Patient", "Arrives without an appointment. Folder is pulled and dispatched on arrival using the same scan-and-select flow.")
    ]
    create_styled_table(doc, t_3_2, [2.2, 4.8], c_navy, c_charcoal)

    add_callout_box(doc, [
        ("Operational Rule: ", True, False, c_navy, 9.5),
        ("Even appointment patients must go through the scan-and-select step at Records before their folder moves. "
         "The pre-load simply means Records knows in advance which folders to prepare.", False, False, c_charcoal, 9.0)
    ], bg_hex="EFF6FF", border_hex="0284C7")
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # 3.3 Hub-and-Spoke Dispersal
    h3_3 = doc.add_heading(level=2)
    r3_3 = h3_3.add_run("3.3 Hub-and-Spoke Dispersal — The Core Workflow")
    r3_3.font.color.rgb = c_sky
    r3_3.font.size = Pt(11)

    p_3_3 = doc.add_paragraph()
    p_3_3.paragraph_format.line_spacing = 1.15
    p_3_3.paragraph_format.space_after = Pt(4)
    p_3_3.add_run(
        "This is the central operational change Phase 2 delivers. The Records officer scans the folder barcode "
        "and selects the destination clinic from a dropdown. That single action triggers four simultaneous events:"
    )

    t_3_3 = [
        ("What Happens", "Where It Occurs"),
        ("Folder status changes to IN TRANSIT", "Records desk and all system views"),
        ("Patient is added to that clinic's daily queue", "Clinic PC / laptop display"),
        ("Executive dashboard updates workload count", "Dean's dashboard in real time"),
        ("60-minute SMS survey countdown begins", "Cloud engine (background dispatch)")
    ]
    create_styled_table(doc, t_3_3, [3.5, 3.5], c_navy, c_charcoal)

    # 3.4 Clinic Queue Display
    h3_4 = doc.add_heading(level=2)
    r3_4 = h3_4.add_run("3.4 Clinic Queue Display — On Each Clinic PC / Laptop")
    r3_4.font.color.rgb = c_sky
    r3_4.font.size = Pt(11)

    p_3_4 = doc.add_paragraph()
    p_3_4.paragraph_format.line_spacing = 1.15
    p_3_4.paragraph_format.space_after = Pt(4)
    p_3_4.add_run(
        "Each of the 13 clinics has its own display on their PC or laptop showing their patient queue for the day. "
        "This screen updates live as the Records desk dispatches folders throughout the morning."
    )

    t_3_4 = [
        ("Queue Status", "What the Clinic Sees"),
        ("Expected", "Patients dispatched from Records, folder in transit to this clinic."),
        ("Arrived", "Folder scanned in by clinic nurse via the PWA. Patient confirmed in custody."),
        ("In Treatment", "Patient currently being attended to by the doctor."),
        ("Completed", "Treatment done. Folder awaiting return to Records."),
        ("Did Not Attend", "Patient was expected but folder was never scanned in at the clinic.")
    ]
    create_styled_table(doc, t_3_4, [2.0, 5.0], c_navy, c_charcoal)

    p_queue_foot = doc.add_paragraph()
    p_queue_foot.paragraph_format.line_spacing = 1.15
    p_queue_foot.paragraph_format.space_after = Pt(6)
    p_queue_foot.add_run(
        "The clinic can see at a glance: how many patients are expected today, how many have arrived, "
        "how many have been seen, and how many are still outstanding."
    )

    doc.add_page_break()

    # 3.5 Offline-First Local Sync
    h3_5 = doc.add_heading(level=2)
    r3_5 = h3_5.add_run("3.5 Offline-First Local Sync — Clinic Data Resilience")
    r3_5.font.color.rgb = c_sky
    r3_5.font.size = Pt(11)

    p_3_5 = doc.add_paragraph()
    p_3_5.paragraph_format.line_spacing = 1.15
    p_3_5.paragraph_format.space_after = Pt(4)
    p_3_5.add_run("The clinic queue and all scan activity at each clinic operates offline-first. This means:")

    t_3_5 = [
        ("Scenario", "What Happens"),
        ("Internet is available", "All scans and queue updates sync to the central Neon PostgreSQL database in real time."),
        ("Internet drops", "All activity continues normally. Scans and updates are saved immediately to a local TXT file on the clinic laptop. No data is lost."),
        ("Internet is restored", "The system automatically detects the connection and syncs all locally saved records to the central database. No manual action required.")
    ]
    create_styled_table(doc, t_3_5, [2.2, 4.8], c_navy, c_charcoal)

    # 3.6 Staff Barcode PWA
    h3_6 = doc.add_heading(level=2)
    r3_6 = h3_6.add_run("3.6 Staff Barcode PWA — Clinic Nurse & Assistant Interface")
    r3_6.font.color.rgb = c_sky
    r3_6.font.size = Pt(11)

    p_3_6 = doc.add_paragraph()
    p_3_6.paragraph_format.line_spacing = 1.15
    p_3_6.paragraph_format.space_after = Pt(4)
    p_3_6.add_run(
        "A mobile-first Progressive Web App that runs on any clinic smartphone, tablet, or PC browser. "
        "No app store installation required."
    )

    t_3_6 = [
        ("Feature", "Detail"),
        ("Authentication", "Nurse or assistant signs in with their staff PIN and selects their active clinic unit."),
        ("Folder Arrival Scan", "Live camera viewfinder with a single Scan Arriving Folder button. When the folder arrives, the nurse scans the barcode."),
        ("Custody Confirmation", "Screen flashes green: Folder K/13 5622 Confirmed — In Custody at Cons. Clinic at 09:42 AM."),
        ("Instant Sync", "Custody transfers in 0.2 seconds. Records room and executive dashboard update immediately.")
    ]
    create_styled_table(doc, t_3_6, [2.2, 4.8], c_navy, c_charcoal)

    # 3.7 Executive Dashboard
    h3_7 = doc.add_heading(level=2)
    r3_7 = h3_7.add_run("3.7 Executive Dashboard — Dean & Management View")
    r3_7.font.color.rgb = c_sky
    r3_7.font.size = Pt(11)

    p_3_7 = doc.add_paragraph()
    p_3_7.paragraph_format.line_spacing = 1.15
    p_3_7.paragraph_format.space_after = Pt(4)
    p_3_7.add_run("Real-time operational intelligence for the Dean and hospital leadership. No manual compilation required.")

    t_3_7 = [
        ("Metric", "What It Shows"),
        ("Live Daily Footfall", "Verified total patients who visited today, this week, and this month across all 13 departments."),
        ("Departmental Workload", "Live count of how many folders are currently held in each of the 13 clinical units."),
        ("Patient Journey Timeline", "Full day timeline for any individual patient: 08:15 Arrival at Records > Dispatched to Surgery 1 > 08:40 Custody Confirmed > 10:15 Returned to Archive."),
        ("Patient Satisfaction", "Live satisfaction scores from automated SMS surveys, integrated in real time.")
    ]
    create_styled_table(doc, t_3_7, [2.2, 4.8], c_navy, c_charcoal)

    doc.add_page_break()

    # 4. A TYPICAL DAY: END-TO-END WORKFLOW
    h4 = doc.add_heading(level=1)
    r4 = h4.add_run("4. A TYPICAL DAY: END-TO-END WORKFLOW")
    r4.font.color.rgb = c_navy

    t_day = [
        ("Time", "Who", "Action"),
        ("07:30 AM", "Records Officers", "Open /archive. Pre-loaded appointment list is ready. Officers pull folders for scheduled patients and begin scanning and dispatching to clinics."),
        ("08:00 AM onwards", "Walk-in Patients", "Arrive at reception. Records officer searches folder, pulls from shelf coordinate, scans out, selects clinic. Patient added to that clinic's queue instantly."),
        ("08:15 AM", "Clinic Nurse", "Opens Staff PWA. Sees incoming folders on clinic queue. Scans each folder barcode as it arrives. Custody confirmed in 0.2 seconds."),
        ("08:30 AM – 02:00 PM", "Doctors & Staff", "Attend to patients. Clinic queue tracks who has been seen and who is still waiting in real time."),
        ("60 Min Post-Scan", "Cloud Engine", "Automated SMS dispatched to patient: personalized feedback survey link: 'UGDS FEEDBACK: Dear {name}, thank you for visiting UGDS. Please rate your experience: {link}'."),
        ("02:30 PM – 04:30 PM", "Records Officers", "Treated folders returned from clinics. Officer scans each one back in. Status returns to ARCHIVED. Folder returned to exact shelf slot."),
        ("04:35 PM", "Dean / Leadership", "Reviews executive dashboard: total patients seen, clinic workload distribution, folder accountability, live satisfaction scores.")
    ]
    create_styled_table(doc, t_day, [1.5, 1.6, 3.9], c_navy, c_charcoal)

    # Illustrative Story: Mr. Kwesi Mensah
    h4_story = doc.add_heading(level=2)
    r4_s = h4_story.add_run("The Patient Experience: A Day with Mr. Kwesi Mensah")
    r4_s.font.color.rgb = c_sky
    r4_s.font.size = Pt(11)

    p_story = doc.add_paragraph()
    p_story.paragraph_format.line_spacing = 1.15
    p_story.paragraph_format.space_after = Pt(4)
    p_story.add_run(
        "To see these seven components working in harmony, consider Mr. Kwesi Mensah (Folder K/13 5622) arriving at 08:00 AM. "
        "At Records, the officer searches his name in <100ms, walks straight to Shelf [ RACK: 1A | BAY: 2 | SHELF: B1 | SLOT: 8 ], "
        "scans the barcode, and selects 'Cons. Clinic'. Instantly, Mr. Mensah appears on the Conservative Clinic PC queue as 'Expected'. "
        "At 08:15 AM, the orderly arrives; Nurse Grace scans the barcode on her PWA camera, moving him to 'Arrived'. "
        "At 08:30 AM, Dr. Boateng attends to him ('In Treatment'). At 09:03 AM — exactly 60 minutes after his initial records scan — "
        "Mr. Mensah's phone buzzes with the feedback survey link. He submits a 5-star rating while rinsing. "
        "At 02:30 PM, his folder is scanned back into Records and restored to Shelf 1A-2-B1-8. In his office, the Dean sees today's "
        "attendance hit 192, with 100% of folders accounted for."
    )

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # 5. PATIENT TYPES & SYSTEM SCOPE
    h5 = doc.add_heading(level=1)
    r5 = h5.add_run("5. PATIENT TYPES & SYSTEM SCOPE")
    r5.font.color.rgb = c_navy

    t_scope = [
        ("Patient Type", "Folder?", "Pre-Load?", "Scan Flow?", "Phase"),
        ("Walk-in", "Yes", "No — pulled on arrival", "Full scan-and-select", "Phase 2 (Active)"),
        ("Appointment", "Yes", "Yes — pre-loaded night before or morning", "Full scan-and-select (mandatory)", "Phase 2 (Active)"),
        ("X-Ray Only", "No", "N/A", "Future requirement — out of scope", "Deferred to Future Phase")
    ]
    create_styled_table(doc, t_scope, [1.5, 0.8, 2.0, 1.5, 1.2], c_navy, c_charcoal)

    doc.add_page_break()

    # 6. CLOUD INFRASTRUCTURE
    h6 = doc.add_heading(level=1)
    r6 = h6.add_run("6. CLOUD INFRASTRUCTURE")
    r6.font.color.rgb = c_navy

    p_infra = doc.add_paragraph()
    p_infra.paragraph_format.line_spacing = 1.15
    p_infra.paragraph_format.space_after = Pt(4)
    p_infra.add_run(
        "Phase 2 moves from the single-PC legacy environment to a dedicated annual enterprise cloud package "
        "on Vercel and Neon PostgreSQL:"
    )

    t_infra = [
        ("Component", "Provider & Tier", "Purpose", "Key Safeguards"),
        ("Frontend & API", "Vercel Production Pro", "Hosts E-Archive desk, clinic queues, and serverless API.", "99.99% SLA uptime, regional CDN, automated SSL, custom UGDS domain."),
        ("Central Database", "Neon PostgreSQL Production", "Stores all 125,042 patient records, folder movement logs, and staff data.", "Automated point-in-time recovery, daily backups, connection pooling for all 13 clinics simultaneously."),
        ("Staff PWA", "Vercel PWA / Edge Cache", "Delivers the mobile barcode scanner to all clinic devices.", "Instant mobile loading, offline caching, no app store installation required.")
    ]
    create_styled_table(doc, t_infra, [1.5, 1.5, 2.0, 2.0], c_navy, c_charcoal)

    # 7. IMPLEMENTATION: 4-WEEK ROLLOUT
    h7 = doc.add_heading(level=1)
    r7 = h7.add_run("7. IMPLEMENTATION: 4-WEEK ROLLOUT")
    r7.font.color.rgb = c_navy

    t_rollout = [
        ("Sprint", "Focus", "Key Deliverables"),
        ("Week 1", "Foundation & Cloud Setup", "Configure on-site daemon at Records PC. Activate Vercel Pro and Neon production packages. Ingest 134 staff profiles. Set up appointment pre-load system."),
        ("Week 2", "Cloud E-Archive Deployment", "Deploy /archive module with sub-100ms search and shelf coordinate locator. Decommission legacy MySQL 5.0 desktop software."),
        ("Week 3", "Clinic Queue & PWA Launch", "Launch clinic queue displays on all 13 clinic PCs. Deploy Staff Barcode PWA. Activate offline-first local TXT sync. Roll out across Oral Diagnosis, Cons. Clinic, and Surgery."),
        ("Week 4", "Executive Dashboard & Handover", "Connect live footfall counters to Phase 1 dashboard. Conduct nursing staff training. Executive leadership review and sign-off.")
    ]
    create_styled_table(doc, t_rollout, [1.2, 1.8, 4.0], c_navy, c_charcoal)

    # 8. FUTURE REQUIREMENTS (OUT OF SCOPE — PHASE 2)
    h8 = doc.add_heading(level=1)
    r8 = h8.add_run("8. FUTURE REQUIREMENTS (OUT OF SCOPE — PHASE 2)")
    r8.font.color.rgb = c_navy

    add_callout_box(doc, [
        ("Formally Captured Requirement: ", True, False, c_navy, 9.5),
        ("The following requirement has been formally captured and deferred to a future development phase. "
         "It does not affect Phase 2 delivery.", False, False, c_charcoal, 9.0)
    ], bg_hex="EFF6FF", border_hex="0284C7")
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    t_future = [
        ("Requirement", "Description", "Reason Deferred"),
        ("X-Ray Patient Tracking", "X-Ray patients do not have physical folders. A lightweight check-in system is needed to log their visits for daily footfall counts without triggering the standard folder scan-and-dispatch flow.", "Different workflow from folder-based patients. Requires separate design and will be scoped as a standalone feature in the next phase.")
    ]
    create_styled_table(doc, t_future, [1.8, 2.8, 2.4], c_navy, c_charcoal)

    # Document Footer
    doc.add_paragraph().paragraph_format.space_after = Pt(14)
    p_foot = doc.add_paragraph()
    p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_ft1 = p_foot.add_run("University of Ghana Dental School\nPhase 2 Master System Specification  |  2026\n")
    r_ft1.bold = True
    r_ft1.font.size = Pt(9.5)
    r_ft1.font.color.rgb = c_navy
    r_ft2 = p_foot.add_run("Cloud E-Archive  |  Hub-and-Spoke Dispersal  |  Barcode PWA  |  Executive Dashboard")
    r_ft2.italic = True
    r_ft2.font.size = Pt(8.5)
    r_ft2.font.color.rgb = c_sky

    try:
        doc.save(doc_path)
        print(f"Phase 2 Word Document built at: {doc_path}")
    except PermissionError:
        alt_path = doc_path.replace(".docx", "_Updated.docx")
        doc.save(alt_path)
        print(f"Note: {doc_path} is currently open in Microsoft Word.")
        print(f"Phase 2 Word Document built at: {alt_path}")


# -------------------------------------------------------------
# 4. BUILD COMPLETE PDF DOCUMENT (.PDF)
# -------------------------------------------------------------
def build_pdf_document(pdf_path, img_flowchart):
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    c_primary = colors.HexColor("#003866")     # UGDS Navy Blue
    c_secondary = colors.HexColor("#0284C7")   # Medical Blue
    c_dark = colors.HexColor("#1E293B")        # Charcoal Text
    c_light_bg = colors.HexColor("#EFF6FF")    # Soft Blue Accent
    c_border_blue = colors.HexColor("#BFDBFE")

    title_style = ParagraphStyle(
        'DocTitle', parent=styles['Heading1'],
        fontName='Helvetica-Bold', fontSize=18, leading=22,
        textColor=c_primary, spaceAfter=3
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=9.5, leading=12,
        textColor=c_secondary, spaceAfter=2
    )

    p1_badge_style = ParagraphStyle(
        'DocBadge', parent=styles['Normal'],
        fontName='Helvetica-Oblique', fontSize=8, leading=10,
        textColor=colors.HexColor("#64748B"), spaceAfter=10
    )

    h1_style = ParagraphStyle(
        'H1', parent=styles['Heading2'],
        fontName='Helvetica-Bold', fontSize=11.5, leading=15,
        textColor=c_primary, spaceBefore=10, spaceAfter=5, keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2', parent=styles['Heading3'],
        fontName='Helvetica-Bold', fontSize=9.5, leading=13,
        textColor=c_secondary, spaceBefore=7, spaceAfter=3, keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8, leading=11,
        textColor=c_dark, spaceAfter=4
    )

    table_header = ParagraphStyle(
        'TH', fontName='Helvetica-Bold', fontSize=7.5, leading=9.5, textColor=colors.white
    )

    table_cell = ParagraphStyle(
        'TC', fontName='Helvetica', fontSize=7.0, leading=9.0, textColor=c_dark
    )

    table_cell_bold = ParagraphStyle(
        'TCB', fontName='Helvetica-Bold', fontSize=7.0, leading=9.0, textColor=c_primary
    )

    elements = []

    # Title Banner
    elements.append(Paragraph("UNIVERSITY OF GHANA DENTAL SCHOOL", subtitle_style))
    elements.append(Paragraph("Phase 2 — Master System Specification & Strategic Blueprint", title_style))
    elements.append(Paragraph("Cloud E-Archive  |  Hub-and-Spoke Dispersal  |  Barcode PWA  |  Executive Dashboard", subtitle_style))
    elements.append(Paragraph("Built on Phase 1: 125,042 patient records migrated  |  Live CRM dashboard  |  Automated birthday messaging", p1_badge_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=c_primary, spaceBefore=2, spaceAfter=8))

    # Executive Summary
    elements.append(Paragraph("EXECUTIVE SUMMARY", h1_style))
    elements.append(Paragraph(
        "Phase 2 transforms clinical records operations at the University of Ghana Dental School. Building on Phase 1 — "
        "which migrated 125,042 patient records to the cloud and deployed a live CRM dashboard — Phase 2 permanently replaces "
        "the 15-year-old legacy desktop eArchive software with a cloud-native system that gives every stakeholder in the hospital "
        "real-time visibility of every patient folder, from the moment it is pulled from the shelf to the moment it is returned.",
        body_style
    ))
    elements.append(Paragraph(
        "The system is built around a single core principle: <b>one scan, one destination selection, and everything updates everywhere "
        "simultaneously — the clinic queue, the records room, and the executive dashboard.</b>",
        body_style
    ))

    # Callout: X-Ray
    callout_txt = (
        "<b>Out of Scope Notice:</b> <i>X-Ray patients (who do not have folders) are captured as a future user requirement and "
        "are out of scope for Phase 2. They will be addressed in a subsequent phase.</i>"
    )
    t_callout = Table([[Paragraph(callout_txt, body_style)]], colWidths=[540])
    t_callout.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_light_bg),
        ('BOX', (0,0), (-1,-1), 1, c_border_blue),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(t_callout)
    elements.append(Spacer(1, 6))

    # 1. Why Phase 2
    elements.append(Paragraph("1. WHY PHASE 2: THE LEGACY SYSTEM PROBLEM", h1_style))
    elements.append(Paragraph(
        "For over fifteen years, all 125,042 patient folder histories have lived on a single desktop PC running Visual Basic "
        "eArchive software connected to a local MySQL 5.0 database on port 3307. This creates four critical operational risks:",
        body_style
    ))

    def make_table(data_rows, col_widths):
        formatted = []
        for r_idx, row in enumerate(data_rows):
            row_cells = []
            for c_idx, text in enumerate(row):
                if r_idx == 0:
                    row_cells.append(Paragraph(text, table_header))
                else:
                    if c_idx == 0 and len(col_widths) > 2:
                        row_cells.append(Paragraph(text, table_cell))
                    elif c_idx == 0 and len(col_widths) <= 2:
                        row_cells.append(Paragraph(text, table_cell_bold))
                    elif c_idx == 1 and len(col_widths) > 2:
                        row_cells.append(Paragraph(text, table_cell_bold))
                    else:
                        row_cells.append(Paragraph(text, table_cell))
            formatted.append(row_cells)
        t = Table(formatted, colWidths=col_widths)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), c_primary),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LEFTPADDING', (0,0), (-1,-1), 4),
            ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ]))
        return t

    t1_data = [
        ["Risk", "Impact"],
        ["Single Point of Failure", "One hard drive crash or malware attack instantly paralyses records retrieval across all 13 departments."],
        ["Zero Clinical Custody", "Once a folder leaves the records room, no one knows where it is. Staff waste hours searching clinic by clinic."],
        ["No Patient Journey History", "The legacy system stores registration numbers only. It cannot record when a patient arrived, which clinic treated them, or how long they waited."],
        ["Management Blindspot", "The Dean and leadership have no real-time counters of daily patient visits, forcing staffing decisions based on guesswork."]
    ]
    elements.append(make_table(t1_data, [150, 390]))
    elements.append(Spacer(1, 6))

    # 2. The 13 UGDS Clinical Units
    elements.append(Paragraph("2. THE 13 UGDS CLINICAL UNITS", h1_style))
    elements.append(Paragraph(
        "The Records Unit acts as the Central Archival and Dispersal Hub. All 12 clinical and service departments are spokes "
        "that receive folders directly from Records and return them directly to Records after treatment:",
        body_style
    ))

    t2_data = [
        ["No.", "Unit", "Function", "Role in Dispersal Model"],
        ["1", "Records Unit (Hub)", "Central Archival & Dispersal", "Pulls folders; scans out; selects destination; audits all returns."],
        ["2", "Account (Cashier)", "Billing & Financial Clearance", "Independent service point; does not block clinical flow."],
        ["3", "Oral Diagnosis Clinic", "Primary Intake & Triage", "Receives and routes new patients to specialist care."],
        ["4", "Cons. Clinic", "Conservative & Operative Dentistry", "Receives folders for restorations and routine care."],
        ["5", "Students Clinic", "Undergraduate Training", "Receives folders for supervised student clinical work."],
        ["6", "Advance Cons. Clinic", "Endodontics & Prosthodontics", "Receives folders for root canals, crowns, and bridges."],
        ["7", "Residents Clinic", "Postgraduate Specialized Care", "Receives folders for advanced referral cases."],
        ["8", "Periodontic Clinic", "Gum Health & Periodontology", "Receives folders for scaling, surgery, and bone-loss care."],
        ["9", "Paedodontic Clinic", "Child & Adolescent Dentistry", "Receives folders for child dentistry and preventive care."],
        ["10", "Orthodontic Clinic", "Malocclusion & Alignment", "Receives folders for brace adjustments and follow-ups."],
        ["11", "Consultant Surgery 1", "Oral & Maxillofacial Surgery", "Receives folders for surgical extractions and biopsies."],
        ["12", "Consultant Surgery 2", "Oral & Maxillofacial Surgery", "Receives folders for facial trauma and surgical consultations."],
        ["13", "X-Ray (Radiology)", "Dental Imaging", "Receives folders for periapical, bitewing, and OPG imaging."]
    ]
    elements.append(make_table(t2_data, [24, 126, 170, 220]))

    # PAGE 2: FLOWCHART
    elements.append(PageBreak())
    elements.append(Paragraph("Central Records Dispersal & Custody Flowchart", h1_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=6))
    elements.append(Paragraph(
        "The diagram below illustrates the direct Hub-and-Spoke Dispersal architecture: Records pulls from shelf coordinates, "
        "scans out to any of the 12 destination units, arming the 60-minute patient survey, and converges back to Records for re-shelving:",
        body_style
    ))
    elements.append(Spacer(1, 4))
    if os.path.exists(img_flowchart):
        elements.append(Image(img_flowchart, width=7.2*inch, height=8.2*inch))

    # PAGE 3: THE SEVEN SYSTEM COMPONENTS
    elements.append(PageBreak())
    elements.append(Paragraph("3. THE SEVEN SYSTEM COMPONENTS", h1_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=6))

    # 3.1 Cloud E-Archive
    elements.append(Paragraph("3.1 Cloud E-Archive — Records Desk Interface", h2_style))
    elements.append(Paragraph("The records officer's primary interface. Replaces the legacy desktop software entirely.", body_style))
    t3_1_data = [
        ["Feature", "Detail"],
        ["Patient Search", "Sub-100ms search across all 125,042 records by folder number or patient name."],
        ["Shelf Coordinate Locator", "Instantly displays exact physical location: RACK | BAY | SHELF | SLOT so officer walks directly to the right shelf."],
        ["Scan & Dispatch", "Officer scans the folder barcode, selects destination clinic from dropdown. One action triggers everything."],
        ["Status Tracking", "Folder status updates hospital-wide: PULLED / IN TRANSIT / IN CUSTODY / RETURNED TO ARCHIVE."]
    ]
    elements.append(make_table(t3_1_data, [150, 390]))
    elements.append(Spacer(1, 4))

    # 3.2 Morning Pre-load
    elements.append(Paragraph("3.2 Morning Pre-Load & Pull List — Appointment Scheduling", h2_style))
    elements.append(Paragraph("Every patient at UGDS falls into one of two categories:", body_style))
    t3_2_data = [
        ["Patient Type", "How They Are Handled"],
        ["Appointment Patient", "Has a pre-booked session with a specific doctor. Folder is pre-loaded into the system the night before or early morning so Records can prepare the morning pull list in advance."],
        ["Walk-in Patient", "Arrives without an appointment. Folder is pulled and dispatched on arrival using the same scan-and-select flow."]
    ]
    elements.append(make_table(t3_2_data, [150, 390]))
    elements.append(Paragraph("<i>Even appointment patients must go through the scan-and-select step at Records before their folder moves. The pre-load simply means Records knows in advance which folders to prepare.</i>", p1_badge_style))

    # 3.3 Hub-and-Spoke
    elements.append(Paragraph("3.3 Hub-and-Spoke Dispersal — The Core Workflow", h2_style))
    elements.append(Paragraph("The Records officer scans the barcode and selects the destination clinic from a dropdown. That single action triggers four simultaneous events:", body_style))
    t3_3_data = [
        ["What Happens", "Where It Occurs"],
        ["Folder status changes to IN TRANSIT", "Records desk and all system views"],
        ["Patient is added to that clinic's daily queue", "Clinic PC / laptop display"],
        ["Executive dashboard updates workload count", "Dean's dashboard in real time"],
        ["60-minute SMS survey countdown begins", "Cloud engine (background dispatch)"]
    ]
    elements.append(make_table(t3_3_data, [270, 270]))
    elements.append(Spacer(1, 4))

    # 3.4 Clinic Queue Display
    elements.append(Paragraph("3.4 Clinic Queue Display — On Each Clinic PC / Laptop", h2_style))
    elements.append(Paragraph("Each of the 13 clinics has its own display on their PC or laptop showing their patient queue for the day:", body_style))
    t3_4_data = [
        ["Queue Status", "What the Clinic Sees"],
        ["Expected", "Patients dispatched from Records, folder in transit to this clinic."],
        ["Arrived", "Folder scanned in by clinic nurse via the PWA. Patient confirmed in custody."],
        ["In Treatment", "Patient currently being attended to by the doctor."],
        ["Completed", "Treatment done. Folder awaiting return to Records."],
        ["Did Not Attend", "Patient was expected but folder was never scanned in at the clinic."]
    ]
    elements.append(make_table(t3_4_data, [140, 400]))

    # PAGE 4: COMPONENTS 3.5 - 3.7 & WORKFLOW
    elements.append(PageBreak())

    # 3.5 Offline-First Local Sync
    elements.append(Paragraph("3.5 Offline-First Local Sync — Clinic Data Resilience", h2_style))
    elements.append(Paragraph("The clinic queue and all scan activity at each clinic operates offline-first. This means:", body_style))
    t3_5_data = [
        ["Scenario", "What Happens"],
        ["Internet is available", "All scans and queue updates sync to the central Neon PostgreSQL database in real time."],
        ["Internet drops", "All activity continues normally. Scans and updates are saved immediately to a local TXT file on the clinic laptop. No data is lost."],
        ["Internet is restored", "The system automatically detects the connection and syncs all locally saved records to the central database. No manual action required."]
    ]
    elements.append(make_table(t3_5_data, [150, 390]))
    elements.append(Spacer(1, 4))

    # 3.6 Staff Barcode PWA
    elements.append(Paragraph("3.6 Staff Barcode PWA — Clinic Nurse & Assistant Interface", h2_style))
    elements.append(Paragraph("A mobile-first Progressive Web App that runs on any clinic smartphone, tablet, or PC browser. No app store installation required.", body_style))
    t3_6_data = [
        ["Feature", "Detail"],
        ["Authentication", "Nurse or assistant signs in with their staff PIN and selects their active clinic unit."],
        ["Folder Arrival Scan", "Live camera viewfinder with a single Scan Arriving Folder button. Nurse scans barcode upon arrival."],
        ["Custody Confirmation", "Screen flashes green: Folder K/13 5622 Confirmed — In Custody at Cons. Clinic at 09:42 AM."],
        ["Instant Sync", "Custody transfers in 0.2 seconds. Records room and executive dashboard update immediately."]
    ]
    elements.append(make_table(t3_6_data, [150, 390]))
    elements.append(Spacer(1, 4))

    # 3.7 Executive Dashboard
    elements.append(Paragraph("3.7 Executive Dashboard — Dean & Management View", h2_style))
    elements.append(Paragraph("Real-time operational intelligence for the Dean and hospital leadership. No manual compilation required.", body_style))
    t3_7_data = [
        ["Metric", "What It Shows"],
        ["Live Daily Footfall", "Verified total patients who visited today, this week, and this month across all 13 departments."],
        ["Departmental Workload", "Live count of how many folders are currently held in each of the 13 clinical units."],
        ["Patient Journey Timeline", "Full day timeline for any individual patient: 08:15 Records > Dispatched > 08:40 Confirmed > 10:15 Archived."],
        ["Patient Satisfaction", "Live satisfaction scores from automated SMS surveys, integrated in real time."]
    ]
    elements.append(make_table(t3_7_data, [150, 390]))
    elements.append(Spacer(1, 6))

    # 4. A Typical Day
    elements.append(Paragraph("4. A TYPICAL DAY: END-TO-END WORKFLOW", h1_style))
    t4_data = [
        ["Time", "Who", "Action"],
        ["07:30 AM", "Records Officers", "Open /archive. Pre-loaded appointment list is ready. Officers pull folders for scheduled patients and begin scanning and dispatching to clinics."],
        ["08:00 AM+", "Walk-in Patients", "Arrive at reception. Records officer searches folder, pulls from shelf coordinate, scans out, selects clinic. Patient added to clinic queue instantly."],
        ["08:15 AM", "Clinic Nurse", "Opens Staff PWA. Sees incoming folders on clinic queue. Scans each folder barcode as it arrives. Custody confirmed in 0.2s."],
        ["08:30 – 14:00", "Doctors & Staff", "Attend to patients. Clinic queue tracks who has been seen and who is still waiting in real time."],
        ["60 Min Post", "Cloud Engine", "Automated SMS dispatched to patient: personalized feedback survey link."],
        ["14:30 – 16:30", "Records Officers", "Treated folders returned from clinics. Officer scans each one back in. Status returns to ARCHIVED. Folder returned to exact shelf slot."],
        ["16:35 PM", "Dean / Leadership", "Reviews executive dashboard: total patients seen, clinic workload distribution, folder accountability, live satisfaction scores."]
    ]
    elements.append(make_table(t4_data, [80, 110, 350]))

    # PAGE 5: PATIENT TYPES, CLOUD, ROLLOUT, FUTURE REQUIREMENTS
    elements.append(PageBreak())

    # 5. Patient Types & System Scope
    elements.append(Paragraph("5. PATIENT TYPES & SYSTEM SCOPE", h1_style))
    t5_data = [
        ["Patient Type", "Folder?", "Pre-Load?", "Scan Flow?", "Phase"],
        ["Walk-in", "Yes", "No — pulled on arrival", "Full scan-and-select", "Phase 2 (Active)"],
        ["Appointment", "Yes", "Yes — pre-loaded night before/morning", "Full scan-and-select (mandatory)", "Phase 2 (Active)"],
        ["X-Ray Only", "No", "N/A", "Future requirement — out of scope", "Deferred to Future Phase"]
    ]
    elements.append(make_table(t5_data, [100, 50, 160, 130, 100]))
    elements.append(Spacer(1, 6))

    # 6. Cloud Infrastructure
    elements.append(Paragraph("6. CLOUD INFRASTRUCTURE", h1_style))
    elements.append(Paragraph("Phase 2 moves from the single-PC legacy environment to a dedicated annual enterprise cloud package on Vercel and Neon PostgreSQL:", body_style))
    t6_data = [
        ["Component", "Provider & Tier", "Purpose", "Key Safeguards"],
        ["Frontend & API", "Vercel Production Pro", "Hosts E-Archive desk, clinic queues, and serverless API.", "99.99% SLA uptime, regional CDN, automated SSL, custom UGDS domain."],
        ["Central Database", "Neon PostgreSQL Production", "Stores 125,042 patient records, folder movement logs, and staff data.", "Automated point-in-time recovery, daily backups, connection pooling for all 13 clinics."],
        ["Staff PWA", "Vercel PWA / Edge Cache", "Delivers the mobile barcode scanner to all clinic devices.", "Instant mobile loading, offline caching, no app store installation required."]
    ]
    elements.append(make_table(t6_data, [110, 110, 160, 160]))
    elements.append(Spacer(1, 6))

    # 7. Implementation: 4-Week Rollout
    elements.append(Paragraph("7. IMPLEMENTATION: 4-WEEK ROLLOUT", h1_style))
    t7_data = [
        ["Sprint", "Focus", "Key Deliverables"],
        ["Week 1", "Foundation & Cloud Setup", "Configure on-site daemon at Records PC. Activate Vercel Pro and Neon production packages. Ingest 134 staff profiles. Set up appointment pre-load system."],
        ["Week 2", "Cloud E-Archive Deployment", "Deploy /archive module with sub-100ms search and shelf coordinate locator. Decommission legacy MySQL 5.0 desktop software."],
        ["Week 3", "Clinic Queue & PWA Launch", "Launch clinic queue displays on all 13 clinic PCs. Deploy Staff Barcode PWA. Activate offline-first local TXT sync. Roll out across Oral Diagnosis, Cons. Clinic, and Surgery."],
        ["Week 4", "Executive Dashboard & Handover", "Connect live footfall counters to Phase 1 dashboard. Conduct nursing staff training. Executive leadership review and sign-off."]
    ]
    elements.append(make_table(t7_data, [70, 130, 340]))
    elements.append(Spacer(1, 6))

    # 8. Future Requirements
    elements.append(Paragraph("8. FUTURE REQUIREMENTS (OUT OF SCOPE — PHASE 2)", h1_style))
    t8_data = [
        ["Requirement", "Description", "Reason Deferred"],
        ["X-Ray Patient Tracking", "X-Ray patients do not have physical folders. A lightweight check-in system is needed to log their visits for daily footfall counts without triggering standard folder scan-and-dispatch.", "Different workflow from folder-based patients. Requires separate design and will be scoped as a standalone feature in the next phase."]
    ]
    elements.append(make_table(t8_data, [130, 230, 180]))
    elements.append(Spacer(1, 10))

    # Footer
    elements.append(Paragraph("<b>University of Ghana Dental School</b> — Phase 2 Master System Specification  |  2026", subtitle_style))
    elements.append(Paragraph("<i>Cloud E-Archive  |  Hub-and-Spoke Dispersal  |  Barcode PWA  |  Executive Dashboard</i>", p1_badge_style))

    try:
        doc.build(elements)
        print(f"Phase 2 PDF built at: {pdf_path}")
    except PermissionError:
        alt_pdf = pdf_path.replace(".pdf", "_Updated.pdf")
        doc_alt = SimpleDocTemplate(alt_pdf, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
        doc_alt.build(elements)
        print(f"Note: {pdf_path} is currently locked by a viewer.")
        print(f"Phase 2 PDF built at: {alt_pdf}")


# -------------------------------------------------------------
# 5. MAIN EXECUTION
# -------------------------------------------------------------
if __name__ == "__main__":
    base_dir = r"d:\MYCODING FILES\KORLEBU PROJECTS"
    doc_path = os.path.join(base_dir, "UGDS_Phase2_Master_Project_Document.docx")
    pdf_path = os.path.join(base_dir, "UGDS_Phase2_Project_Document.pdf")
    img_flowchart = os.path.join(base_dir, "ugds_folder_flowchart.png")

    print("Step 1: Creating 300-DPI Hub-and-Spoke Dispersal Flowchart...")
    create_flowchart_image(img_flowchart)

    print("Step 2: Building Microsoft Word Document (.docx)...")
    build_word_document(doc_path, img_flowchart)

    print("Step 3: Building Official Styled PDF (.pdf)...")
    build_pdf_document(pdf_path, img_flowchart)

    print("All documents generated successfully!")
