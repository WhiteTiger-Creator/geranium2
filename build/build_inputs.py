"""Generate the nine input files for the Cordell NSR applicability task."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cordell as c
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from docx import Document
from docx.shared import Pt, Inches, RGBColor

OUT = "/home/azureuser/geranium_tasks/task2_env/input_files"
os.makedirs(OUT, exist_ok=True)
TEAL = "1B4F5C"
HDR = Font(bold=True, color="FFFFFF", size=9)
THIN = Side(style="thin", color="BFBFBF"); BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

def sheet(wb, title, headers, rows, widths=None, fmts=None, first=False, note=None):
    ws = wb.active if first else wb.create_sheet(); ws.title = title; r = 1
    if note:
        x = ws.cell(1,1,note); x.font = Font(italic=True, size=8.5, color="595959")
        x.alignment = Alignment(wrap_text=True, vertical="top"); ws.row_dimensions[1].height = 40; r = 3
    for i,h in enumerate(headers,1):
        x = ws.cell(r,i,h); x.font, x.border = HDR, BOX
        x.fill = PatternFill("solid", fgColor=TEAL)
        x.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
    ws.row_dimensions[r].height = 32
    for j,row in enumerate(rows, r+1):
        for i,v in enumerate(row,1):
            x = ws.cell(j,i,v); x.border = BOX; x.font = Font(size=9)
            if fmts and fmts.get(i): x.number_format = fmts[i]
    for i in range(1,len(headers)+1):
        ws.column_dimensions[get_column_letter(i)].width = (widths or {}).get(i,14)
    ws.freeze_panes = ws.cell(r+1,1); ws.sheet_view.showGridLines = False

def doc_new(t, sub=None):
    d = Document(); st = d.styles["Normal"]; st.font.name, st.font.size = "Calibri", Pt(10.5)
    p = d.add_paragraph(); run = p.add_run(t)
    run.bold, run.font.size, run.font.color.rgb = True, Pt(15), RGBColor(0x1B,0x4F,0x5C)
    if sub:
        q = d.add_paragraph(); r2 = q.add_run(sub)
        r2.italic, r2.font.size, r2.font.color.rgb = True, Pt(9.5), RGBColor(0x59,0x59,0x59)
    return d

def head(d,t,size=11.5):
    p = d.add_paragraph(); r = p.add_run(t)
    r.bold, r.font.size, r.font.color.rgb = True, Pt(size), RGBColor(0x1B,0x4F,0x5C)

def f01():
    d = doc_new("CORDELL SPECIALTY COATINGS", "Request to Wren & Balfour Environmental Engineering")
    t = d.add_table(rows=4, cols=2); t.style = "Table Grid"
    for i,(k,v) in enumerate([("From","Anselm Vieira, Plant Manager"),("Date","May 11, 2026"),
                              ("Subject","Line 4 project, air permitting"),
                              ("Site",f"{c.FACILITY}, {c.LOCATION}")]):
        t.rows[i].cells[0].width = Inches(0.8); t.rows[i].cells[1].width = Inches(5.9)
        t.rows[i].cells[0].text=""; t.rows[i].cells[0].paragraphs[0].add_run(k).bold=True
        t.rows[i].cells[1].text = v
    d.add_paragraph()
    d.add_paragraph(
        "We have board approval to install a fourth topcoat line and the equipment order goes in at the "
        "end of June. Before it does I need to know what we are walking into on the air permit, because "
        "our corporate counsel has told me that if this turns into a major source review the schedule "
        "is dead and the project goes back to the board.")
    d.add_paragraph(
        "My own arithmetic says we are fine. The new line adds about thirty tons a year of solvent "
        "after the oxidiser, which is comfortably under the forty ton figure our last consultant told "
        "me was the number that matters. I would like that confirmed or corrected before I commit "
        "capital.")
    head(d, "What I need")
    for x in ["Whether the project triggers major source review, and the arithmetic behind it rather "
              "than a conclusion.",
              "If it does, what our options are and what each one costs. I would rather spend money on "
              "equipment than on offsets and lawyers.",
              "How long each option takes to permit. The line has to be running by the second quarter "
              "of next year.",
              "Anything else the project drags in that we have not thought about."]:
        d.add_paragraph(x, style="List Number")
    head(d, "Things you should know")
    for x in ["We run Line 4 the same way we run the others, one shift, five days a week, about two "
              "hundred and fifty days a year. Nobody here has ever run a coating line around the clock.",
              "We debottlenecked Line 2 last August, mostly a new pump skid and a wider oven. Throughput "
              "went up. I do not believe we filed anything for it because nobody told us we had to.",
              "We shut Line 1 down permanently in 2022 and I have always understood we had credit "
              "banked from that. If we can use it here, use it.",
              "The oxidiser vendor has quoted the hood arrangement we use on Lines 1 through 3. If a "
              "different arrangement helps us, say so, but it has to be in the same building."]:
        d.add_paragraph(x, style="List Bullet")
    d.add_paragraph("- Anselm")
    d.save(f"{OUT}/01_Client_Request.docx")

def f02():
    wb = Workbook()
    rows = [["Maximum design coating application rate", c.L4_DESIGN_GAL_DAY, "gal/day",
             "Nameplate rating, vendor data sheet CL4-002"],
            ["Coating applied", c.COATING["name"], "", "Single product, no alternates specified"],
            ["Cleanup solvent usage", c.CLEANUP["gal_per_month"], "gal/month",
             "Based on Lines 1 to 3 experience at equivalent throughput"],
            ["Cleanup solvent", c.CLEANUP["name"], "", ""],
            ["Oven", "Natural gas, 2.4 MMBtu/hr", "", "Combustion emissions permitted separately"],
            ["Planned operating schedule", c.CLIENT_STATED_DAYS, "days/year",
             "One shift, five days per week, as advised by the plant manager"],
            ["Hours in a calendar year", 8760, "hr/year", ""],
            ["Installation", "New line, no existing equipment replaced", "", ""]]
    sheet(wb, "Line 4 Design", ["Parameter","Value","Unit","Note"], rows,
          widths={1:44,2:22,3:14,4:56}, first=True,
          note=("Wren & Balfour project file, Cordell Line 4. Figures taken from the vendor proposal "
                "and from the plant manager's advice. No permit condition presently limits the "
                "operating schedule of any line at this facility."))
    sheet(wb, "Line 2 Change", ["Parameter","Value","Unit","Note"],
          [["Date completed","2025-08","","Pump skid replacement and oven extension"],
           ["Increase in potential VOC emissions", c.LINE2_DEBOTTLENECK["voc_tpy"],"tpy",
            "Calculated by Wren & Balfour from the revised throughput"],
           ["Increase in potential xylene emissions", c.LINE2_DEBOTTLENECK["xylene_tpy"],"tpy",""],
           ["Permit application filed","No","","No record in the agency file or the plant records"]],
          widths={1:40,2:20,3:12,4:56}, fmts={2:'0.00'})
    wb.save(f"{OUT}/02_Line4_Design_Data.xlsx")

def f03():
    wb = Workbook()
    sheet(wb, "Cordelan 7300", ["Property","Value","Unit"],
          [["Product", c.COATING["name"], ""],
           ["Density", 9.42, "lb/gal"],
           ["Volatile organic compound content, as supplied", c.COATING["voc_as_supplied_lb_gal"], "lb/gal"],
           ["Volatile organic compound content, less water and exempt compounds",
            c.COATING["voc_less_water_lb_gal"], "lb/gal"],
           ["Water content by volume", 23.7, "percent"],
           ["Xylene, less water and exempt compounds", c.COATING["xylene_less_water_lb_gal"], "lb/gal"],
           ["Xylene, CAS", "1330-20-7", ""],
           ["Solids by volume", 41.2, "percent"]],
          widths={1:56,2:18,3:12}, fmts={2:'0.00'}, first=True,
          note=("Manufacturer technical data sheet, revision 4, issued 2025-11. Two volatile organic "
                "compound values are reported. The as-supplied value includes water; the second "
                "excludes water and exempt compounds."))
    sheet(wb, "Cordelan CS-40", ["Property","Value","Unit"],
          [["Product", c.CLEANUP["name"], ""],
           ["Density", 7.14, "lb/gal"],
           ["Volatile organic compound content", c.CLEANUP["voc_lb_gal"], "lb/gal"],
           ["Toluene", c.CLEANUP["toluene_lb_gal"], "lb/gal"],
           ["Toluene, CAS", "108-88-3", ""],
           ["Water content", 0.0, "percent"],
           ["Application", "Manual wipe and spray gun flush", ""],
           ["Capture", "Not ducted to the oxidiser", ""]],
          widths={1:44,2:18,3:12}, fmts={2:'0.00'})
    wb.save(f"{OUT}/03_Coating_Data_Sheets.xlsx")

def f04():
    d = doc_new("AIR PERMIT TO OPERATE", f"Permit A-2019-0884, {c.FACILITY}, {c.LOCATION} | Issued by "
                f"the {c.AGENCY} | Effective 2019-06-01, renewed 2024-05-30")
    head(d, "Condition 3.1, Facility-wide emission limitation")
    d.add_paragraph(
        f"Emissions of volatile organic compounds from all emission units at the facility, excluding "
        f"fugitive emissions, shall not exceed {c.PERMITTED_VOC_CAP_TPY:.1f} tons in any consecutive "
        f"twelve month period. This limitation is federally enforceable and is accepted by the "
        f"permittee for the purpose of establishing that the facility is not a major stationary source "
        f"under Calvert Air Regulation 5.")
    head(d, "Condition 3.2, Recordkeeping")
    d.add_paragraph(
        "The permittee shall maintain monthly records of coating and solvent usage by product, and "
        "shall compute emissions using the volatile organic compound content less water and exempt "
        "compounds reported on the manufacturer's data sheet.")
    head(d, "Condition 4.4, Control equipment")
    d.add_paragraph(
        "Emission units 1 through 3 shall be vented to the regenerative thermal oxidiser at all times "
        "the units are in operation. The oxidiser shall maintain a destruction efficiency of not less "
        "than 98 percent. No capture efficiency is specified in this permit for units 1 through 3.")
    head(d, "Condition 5.1, Operating schedule")
    d.add_paragraph(
        "No condition of this permit restricts the hours of operation of any emission unit.")
    head(d, "Condition 7.2, Modifications")
    d.add_paragraph(
        "The permittee shall not construct, install or modify any emission unit at the facility without "
        "first obtaining a revision to this permit. An application shall be filed not less than ninety "
        "days before construction commences.")
    d.save(f"{OUT}/04_Existing_Permit.docx")

def f05():
    d = doc_new("CALVERT AIR REGULATION 5", "New Source Review | Extract of definitions and "
                "applicability provisions | Calvert Division of Air Quality, 2024 edition")
    for t,b in [
        ("5.02(a), Major stationary source",
         f"A stationary source located in an area designated nonattainment for ozone and classified "
         f"moderate is a major stationary source for volatile organic compounds where its potential to "
         f"emit equals or exceeds {c.MAJOR_VOC_TPY:.0f} tons per year."),
        ("5.02(b), Potential to emit",
         "The maximum capacity of a stationary source to emit a pollutant under its physical and "
         "operational design. Any physical or operational limitation on the capacity of the source to "
         "emit a pollutant, including a restriction on hours of operation or on the type or amount of "
         "material processed, shall be treated as part of its design only if the limitation is "
         "federally enforceable. An operating schedule that is not the subject of a permit condition "
         "shall not be taken into account."),
        ("5.02(c), Fugitive emissions",
         "Emissions which could not reasonably pass through a stack, chimney, vent or other "
         "functionally equivalent opening. Fugitive emissions shall not be included in determining "
         "whether a stationary source is a major stationary source unless the source belongs to one of "
         "the categories listed at Appendix 5-A. The manufacture of surface coatings is not a listed "
         "category."),
        ("5.02(d), Control efficiency",
         "Where emissions are reduced by an add-on control device, the reduction credited shall be the "
         "product of the capture efficiency of the collection system and the destruction or removal "
         "efficiency of the device. Neither may be credited unless it is made a condition of the "
         "permit."),
        ("5.03(a), Significant net emissions increase",
         f"For volatile organic compounds, a net emissions increase of {c.SIGNIFICANT_VOC_TPY:.0f} tons "
         f"per year or more is significant."),
        ("5.03(b), Aggregation of changes",
         "Two or more physical changes or changes in the method of operation that are substantially "
         "related to one another, or that occur within a period of three years, shall be treated as a "
         "single project for the purposes of this regulation, whether or not a permit was obtained for "
         "any of them."),
        ("5.04(a), Applicability at an existing major source",
         "A physical change at an existing major stationary source that results in a significant net "
         "emissions increase is a major modification and is subject to review under this regulation. "
         "In determining the net emissions increase, contemporaneous creditable increases and "
         "decreases may be taken into account."),
        ("5.04(b), Applicability where a source becomes major",
         "Where a project at a source that is not a major stationary source would result in the source "
         "becoming a major stationary source, the project shall be reviewed as a new major stationary "
         "source. The emissions of the entire project shall be subject to review and the netting "
         "provisions of subsection 5.04(a) shall not be available."),
        ("5.05, Creditable decreases",
         "A decrease in actual emissions is creditable only to the extent that it is federally "
         "enforceable, that it has approximately the same qualitative significance for public health "
         "as the increase, and that it has not previously been relied upon in any determination under "
         "this regulation."),
        ("5.06, Requirements for a major stationary source",
         f"An applicant subject to review as a major stationary source shall apply the lowest "
         f"achievable emission rate, shall obtain emission reduction offsets at a ratio of "
         f"{c.OFFSET_RATIO:.2f} to one, and shall demonstrate that all other sources owned by the "
         f"applicant in the state are in compliance."),
        ("5.09, Hazardous air pollutants",
         f"A source is major for hazardous air pollutants where the potential to emit any single listed "
         f"pollutant equals or exceeds {c.HAP_SINGLE_TPY:.0f} tons per year, or where the potential to "
         f"emit any combination of listed pollutants equals or exceeds {c.HAP_AGGREGATE_TPY:.0f} tons "
         f"per year. Xylene and toluene are listed pollutants."),
    ]:
        head(d,t,size=10.5); d.add_paragraph(b)
    d.save(f"{OUT}/05_Air_Regulation_5.docx")

def f06():
    d = doc_new("CONTROL EQUIPMENT EVALUATION", "Thurlow Combustion Systems | Issued to Wren & Balfour "
                "| 2026-05-06 | Cordell Line 4")
    head(d, "Existing oxidiser")
    d.add_paragraph(
        f"The existing regenerative thermal oxidiser has demonstrated a destruction efficiency of "
        f"{c.RTO_DESTRUCTION:.0%} on the most recent stack test and has sufficient thermal capacity to "
        f"accept the Line 4 exhaust without modification, provided the collected volume does not "
        f"increase beyond the present arrangement.")
    head(d, "Option 1, hood arrangement as used on Lines 1 to 3")
    d.add_paragraph(
        f"Side draft hoods with a partial enclosure over the application zone. Measured capture "
        f"efficiency on Line 3 under the same arrangement was {c.RTO_CAPTURE_AS_DESIGNED:.0%}. This is "
        f"the arrangement in our base quotation. No change to the oxidiser is required.")
    head(d, "Option 2, permanent total enclosure")
    d.add_paragraph(
        f"A permanent total enclosure around the application zone and flash-off, built and verified to "
        f"the agency's enclosure criteria, achieves a capture efficiency of "
        f"{c.ENCLOSURE_CAPTURE:.0%} by definition. The enclosure raises the collected air volume by "
        f"roughly forty percent, which exceeds the present oxidiser capacity, so the oxidiser would "
        f"require upsizing. Both items are priced in the cost schedule.")
    d.add_paragraph(
        "We are not able to advise which arrangement the project requires. That depends on the "
        "applicability calculation rather than on the equipment.", style="Intense Quote")
    head(d, "Cleanup solvent")
    d.add_paragraph(
        "Manual wipe cleaning and gun flushing are carried out at a bench outside the application zone "
        "and are not ducted to the oxidiser under either option. No practical collection arrangement "
        "was identified.")
    d.save(f"{OUT}/06_Control_Equipment.docx")

def f07():
    wb = Workbook()
    rows = [["Emission units 1 to 3, coating lines", 71.4, "Vented to the oxidiser"],
            ["Mix room and raw material storage", 6.1, "Vented to the oxidiser"],
            ["Cleanup solvent, Lines 1 to 3", 4.5, "Not ducted"],
            ["Wastewater collection sumps", 2.7, "Fugitive"],
            ["Truck loading rack", 1.5, "Fugitive"]]
    sheet(wb, "VOC by Source", ["Emission unit or activity","2025 actual emissions, tpy","Note"], rows,
          widths={1:44,2:24,3:34}, fmts={2:'0.0'}, first=True,
          note=("Cordell annual emission statement for calendar year 2025 as submitted to the agency. "
                "Actual emissions, not potential. The facility-wide permitted limit is a potential to "
                "emit limitation and is reported separately in the permit."))
    sheet(wb, "HAP", ["Pollutant","2025 actual, tpy","Potential to emit, tpy","Source"],
          [["Xylene", 2.74, c.EXISTING_HAP_TPY["Xylene"], "Coatings, Lines 1 to 3"],
           ["Toluene", 1.52, c.EXISTING_HAP_TPY["Toluene"], "Cleanup solvent"]],
          widths={1:18,2:18,3:22,4:30}, fmts={2:'0.00',3:'0.00'})
    sheet(wb, "Fugitive Detail", ["Activity","tpy","Basis"],
          [["Wastewater collection sumps", 2.70, "Water 9 emission model, 2024 characterisation"],
           ["Truck loading rack", 1.50, "AP-42 loading loss equation, submerged fill"],
           ["Total fugitive VOC", c.FUGITIVE_VOC_TPY, ""]],
          widths={1:34,2:12,3:52}, fmts={2:'0.00'})
    wb.save(f"{OUT}/07_Facility_Emissions.xlsx")

def f08():
    wb = Workbook()
    rows = [[k, v, "Capital" if "permit" not in k.lower() else "Professional services"]
            for k, v in c.COSTS.items()]
    rows.append(["Emission reduction offsets, cost per ton", c.OFFSET_COST_PER_TON,
                 "Market rate, Calvert offset registry, Q1 2026"])
    sheet(wb, "Costs", ["Item","Amount, USD","Category"], rows,
          widths={1:62,2:18,3:38}, fmts={2:'#,##0'}, first=True,
          note=("Wren & Balfour estimating file, May 2026. Capital items from vendor quotations. "
                "Offset pricing from the most recent three registry transactions. Excludes escalation "
                "and owner's costs."))
    sheet(wb, "Schedule", ["Permitting route","Months, low","Months, high","Note"],
          [["Minor permit revision", *c.SCHEDULE_MONTHS["minor revision"],
            "Agency has ninety days to act on a complete application"],
           ["Major stationary source review", *c.SCHEDULE_MONTHS["major source review"],
            "Includes lowest achievable emission rate analysis, offset procurement, dispersion "
            "modelling and public comment"]],
          widths={1:34,2:14,3:14,4:62}, fmts={2:'0',3:'0'})
    wb.save(f"{OUT}/08_Cost_Estimates.xlsx")

def f09():
    d = doc_new("PERMIT AND ENFORCEMENT HISTORY", f"{c.FACILITY} | Compiled by Wren & Balfour from the "
                f"{c.AGENCY} public file | 2026-05-08")
    for t,b in [
        ("2019-06-01, Permit A-2019-0884 issued",
         f"Initial permit to operate. Facility-wide volatile organic compound limitation of "
         f"{c.PERMITTED_VOC_CAP_TPY:.1f} tons per twelve month period accepted by the permittee to "
         f"avoid classification as a major stationary source."),
        ("2022-04, Line 1 permanently shut down",
         f"Coating Line 1 was dismantled and removed. The agency file records a reduction in potential "
         f"emissions of {abs(c.LINE1_SHUTDOWN['voc_tpy']):.1f} tons per year associated with the "
         f"shutdown."),
        ("2023-09-14, Permit revision R-23-0412",
         f"Revision issued to authorise the Line 3 coating changeover. The agency's determination "
         f"letter states that the emissions increase from the changeover was offset by the reduction "
         f"associated with the 2022 shutdown of Line 1, and that the reduction was relied upon in full "
         f"in making that determination."),
        ("2024-05-30, Permit renewed",
         "Renewed without change to the facility-wide limitation."),
        ("2025-08, Line 2 modification",
         "No application appears in the agency file for the Line 2 pump skid and oven extension. The "
         "plant confirms the work was completed in August 2025 and that throughput increased "
         "thereafter."),
        ("Compliance",
         "No notices of violation, consent orders or penalty actions appear in the file. The most "
         "recent annual emission statement was filed on time. The most recent stack test on the "
         "oxidiser was witnessed by the agency on 2024-10-08."),
    ]:
        head(d,t,size=10.5); d.add_paragraph(b)
    d.save(f"{OUT}/09_Permit_History.docx")

for fn in (f01,f02,f03,f04,f05,f06,f07,f08,f09):
    fn(); print("built", fn.__name__)
