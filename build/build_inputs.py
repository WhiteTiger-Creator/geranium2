import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cutover as c
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from docx import Document
from docx.shared import Pt, Inches, RGBColor
OUT="/home/azureuser/geranium_tasks/task2_env/input_files"; os.makedirs(OUT,exist_ok=True)
SLATE="2E4057"
HDR=Font(bold=True,color="FFFFFF",size=9); THIN=Side(style="thin",color="BFBFBF")
BOX=Border(left=THIN,right=THIN,top=THIN,bottom=THIN)

def sheet(wb,title,headers,rows,widths=None,fmts=None,first=False,note=None):
    ws=wb.active if first else wb.create_sheet(); ws.title=title; r=1
    if note:
        x=ws.cell(1,1,note); x.font=Font(italic=True,size=8.5,color="595959")
        x.alignment=Alignment(wrap_text=True,vertical="top"); ws.row_dimensions[1].height=40; r=3
    for i,h in enumerate(headers,1):
        x=ws.cell(r,i,h); x.font,x.border=HDR,BOX; x.fill=PatternFill("solid",fgColor=SLATE)
        x.alignment=Alignment(wrap_text=True,vertical="center",horizontal="center")
    ws.row_dimensions[r].height=32
    for j,row in enumerate(rows,r+1):
        for i,v in enumerate(row,1):
            x=ws.cell(j,i,v); x.border=BOX; x.font=Font(size=9)
            if fmts and fmts.get(i): x.number_format=fmts[i]
    for i in range(1,len(headers)+1):
        ws.column_dimensions[get_column_letter(i)].width=(widths or {}).get(i,14)
    ws.freeze_panes=ws.cell(r+1,1); ws.sheet_view.showGridLines=False

def doc(t,sub=None):
    d=Document(); st=d.styles["Normal"]; st.font.name,st.font.size="Calibri",Pt(10.5)
    p=d.add_paragraph(); r=p.add_run(t); r.bold,r.font.size,r.font.color.rgb=True,Pt(14),RGBColor(0x2E,0x40,0x57)
    if sub:
        q=d.add_paragraph(); r2=q.add_run(sub); r2.italic,r2.font.size,r2.font.color.rgb=True,Pt(9),RGBColor(0x59,0x59,0x59)
    return d
def head(d,x,size=11.5):
    p=d.add_paragraph(); r=p.add_run(x); r.bold,r.font.size,r.font.color.rgb=True,Pt(size),RGBColor(0x2E,0x40,0x57)

# ------------------------------------------------------------- brief ------
d=doc("PROGRAMME BRIEF", f"{c.CLIENT} | ERP replacement programme | Issued to {c.INTEGRATOR} | "
      f"Marguerite Delahaye, Programme Director | 2026-08-24")
d.add_paragraph(
    "We are replacing the legacy ERP across all fourteen manufacturing and distribution sites. The "
    "software is selected, the core build is complete and the first site can take a cutover team from "
    "the week commencing 7 September 2026, which we are calling programme week 1. What I need from you "
    "is the sequence.")
d.add_paragraph(
    "I have had two attempts at this internally and both fell over. The first ran the biggest sites "
    "first, which felt right and turned out to be wrong. The second spread the sites evenly across the "
    "programme and put half of them into weeks we cannot touch. I would rather you built it from the "
    "constraints than from an instinct about which site is most important.")
head(d,"Deployment capacity")
d.add_paragraph(f"We have {c.TEAMS} deployment teams. A team runs one site at a time and cannot be "
                f"split. The number of weeks each site occupies a team is in the site profile and is "
                f"not negotiable; those durations came out of the pilot and finance has already "
                f"approved the resourcing against them.")
head(d,"Master data")
d.add_paragraph("Three sites own master data for the group. Bridgnorth owns material master, "
                "Halesworth owns customer master and Kinloss owns vendor master. A site that consumes "
                "a master data domain cannot cut over until the site that owns that domain has "
                "completed its own cutover. The dependencies for each site are in the site profile.")
head(d,"Financial blackouts")
d.add_paragraph("No cutover may run during a financial blackout. A blackout covers the week containing "
                "a quarter end and the week before it, and the first three weeks of January for the "
                "annual close. A cutover may not start in a blackout week and may not run through one; "
                "if a site's cutover would span a blackout, it has to sit entirely before or entirely "
                "after.")
head(d,"Plant shutdowns")
d.add_paragraph("Two sites run continuous process plant and cannot take a cutover while producing. "
                "Mobile and Sarnia can only begin a cutover in their annual maintenance shutdown, and "
                "the shutdown week for each is in the site profile. Those windows do not move; they are "
                "set by the turnaround contractors a year in advance.")
head(d,"Regulated site")
d.add_paragraph(f"Cork manufactures under GMP. After the technical cutover completes, Cork requires a "
                f"{c.VALIDATION_WEEKS} week computer system validation period before it may transact on "
                f"the new system. The site is not live until validation completes. Validation does not "
                f"occupy a deployment team.")
head(d,"The date that matters")
d.add_paragraph("Every site must be live on the new system before the legacy vendor's support ends. "
                "The vendor's notice is attached. Live means transacting, which for Cork means after "
                "validation and not after the technical cutover.")
head(d,"What I want back")
d.add_paragraph("The sequence: which site, in which wave, on which team, starting which programme week. "
                "I want to be able to see the team loading week by week, and I want each constraint "
                "shown as satisfied rather than asserted, because I will be taking this to a steering "
                "committee that has already rejected two plans.")
d.save(f"{OUT}/Programme_Brief.docx")

# ------------------------------------------------------ site profile -----
wb=Workbook()
rows=[]
for code,s in c.SITE.items():
    rows.append([code, s["name"], s["country"], s["users"], s["master"] or "",
                 ", ".join(s["deps"]) or "", s["weeks"],
                 s["shutdown"][0] if s["shutdown"] else "", "Yes" if s["gmp"] else "No"])
sheet(wb,"Sites",["Code","Site","Country","Named users","Master data owned",
                  "Depends on","Cutover weeks","Shutdown window, programme week",
                  "GMP regulated"],rows,
      widths={1:8,2:14,3:16,4:13,5:18,6:14,7:13,8:18,9:13},first=True,
      note=("Verwood Specialty Chemicals, site profile for the ERP programme. Cutover weeks are the "
            "weeks a site occupies a deployment team, taken from the pilot. Dependencies are master "
            "data consumption relationships."))
sheet(wb,"Programme Calendar",["Programme week","Week commencing"],
      [[w, c.monday(w)] for w in range(1,50)],
      widths={1:16,2:20},fmts={2:'yyyy-mm-dd'},
      note="Programme week 1 commences 2026-09-07. Weeks run Monday to Sunday.")
wb.save(f"{OUT}/Site_Profile.xlsx")

# ---------------------------------------------------- vendor notice ------
d=doc("NOTICE OF END OF SUPPORT", "Calderstone Business Systems Limited to Verwood Specialty "
      "Chemicals | Reference CBS-EOS-2451 | 2026-04-30")
d.add_paragraph(
    "This notice is given under clause 14.2 of the support agreement between Calderstone Business "
    "Systems Limited and Verwood Specialty Chemicals dated 3 March 2016.")
head(d,"End of support")
d.add_paragraph(f"Calderstone will cease all support for the Calderstone Enterprise product line, "
                f"including corrective maintenance, regulatory updates and security patching, with "
                f"effect from {c.LEGACY_SUPPORT_ENDS.strftime('%d %B %Y')}. No incident raised after "
                f"that date will be accepted, whether or not the underlying fault arose before it.")
head(d,"Extended support")
d.add_paragraph("Calderstone does not offer extended support for this product line. The product is "
                "being withdrawn rather than transitioned and no successor arrangement is available at "
                "any price. Enquiries about extension will not be entertained.")
head(d,"Effect on the licence")
d.add_paragraph("The perpetual licence survives the end of support. The customer may continue to "
                "operate the software unsupported at its own risk. Verwood should note that the "
                "product will no longer receive statutory or fiscal updates, which in most "
                "jurisdictions makes continued use impracticable for a trading entity.")
d.save(f"{OUT}/Vendor_Notice.docx")
print("\n".join(sorted(os.listdir(OUT))))
