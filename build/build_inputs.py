import sys, os, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tracker as t
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from docx import Document
from docx.shared import Pt, Inches, RGBColor
OUT = "/home/azureuser/geranium_tasks/task2_env/input_files"
os.makedirs(OUT, exist_ok=True)
PLUM = "5B2C4E"
HDR = Font(bold=True, color="FFFFFF", size=9)
THIN = Side(style="thin", color="BFBFBF"); BOX = Border(left=THIN,right=THIN,top=THIN,bottom=THIN)

def sheet(wb, title, headers, rows, widths=None, fmts=None, first=False, note=None):
    ws = wb.active if first else wb.create_sheet(); ws.title=title; r=1
    if note:
        c=ws.cell(1,1,note); c.font=Font(italic=True,size=8.5,color="595959")
        c.alignment=Alignment(wrap_text=True,vertical="top"); ws.row_dimensions[1].height=42; r=3
    for i,h in enumerate(headers,1):
        c=ws.cell(r,i,h); c.font,c.border=HDR,BOX; c.fill=PatternFill("solid",fgColor=PLUM)
        c.alignment=Alignment(wrap_text=True,vertical="center",horizontal="center")
    ws.row_dimensions[r].height=30
    for j,row in enumerate(rows,r+1):
        for i,v in enumerate(row,1):
            c=ws.cell(j,i,v); c.border=BOX; c.font=Font(size=9)
            if fmts and fmts.get(i): c.number_format=fmts[i]
    for i in range(1,len(headers)+1):
        ws.column_dimensions[get_column_letter(i)].width=(widths or {}).get(i,16)
    ws.freeze_panes=ws.cell(r+1,1); ws.sheet_view.showGridLines=False

def doc(title, sub=None):
    d=Document(); st=d.styles["Normal"]; st.font.name,st.font.size="Calibri",Pt(10.5)
    p=d.add_paragraph(); r=p.add_run(title); r.bold,r.font.size,r.font.color.rgb=True,Pt(14),RGBColor(0x5B,0x2C,0x4E)
    if sub:
        q=d.add_paragraph(); r2=q.add_run(sub); r2.italic,r2.font.size,r2.font.color.rgb=True,Pt(9),RGBColor(0x59,0x59,0x59)
    return d

def head(d,x,size=11.5):
    p=d.add_paragraph(); r=p.add_run(x); r.bold,r.font.size,r.font.color.rgb=True,Pt(size),RGBColor(0x5B,0x2C,0x4E)

rows = t.build_sample(); t.flag_quality(rows)

# ------------------------------------------------------------------ data --
cols = ["respondent_id","field_day","supplier","screener_version","loi_minutes","age_band","gender",
        "region","education","urbanicity","aware","consider","used_12m"] + [f"b{k}" for k in range(1,9)]
with open(f"{OUT}/Wave12_Data.csv","w",newline="") as f:
    wcsv=csv.DictWriter(f,fieldnames=cols,extrasaction="ignore"); wcsv.writeheader()
    for r in rows: wcsv.writerow(r)
print("Wave12_Data.csv rows:",len(rows))

# ------------------------------------------------------------ benchmarks --
wb=Workbook()
sheet(wb,"Age by Gender",["Age band","Gender","Population share"],
      [[a,g,v] for (a,g),v in t.AGE_GENDER.items()],
      widths={1:14,2:12,3:18},fmts={3:'0.0%'},first=True,
      note=("Current Population Survey, annual social and economic supplement, adults 18 and over, "
            "United States. Shares are interlocked and sum to one across the eight cells."))
sheet(wb,"Region",["Region","Population share"],[[k,v] for k,v in t.REGION.items()],
      widths={1:16,2:18},fmts={2:'0.0%'})
sheet(wb,"Education",["Highest attainment","Population share"],[[k,v] for k,v in t.EDUCATION.items()],
      widths={1:26,2:18},fmts={2:'0.0%'})
sheet(wb,"Other Reference",["Measure","Value","Source","Universe","Definition"],
      [["Category incidence",t.CATEGORY_INCIDENCE_SYNDICATED,
        "Brightmoor Syndicated Category Report, 2025 annual",
        "Adults 21 and over","Purchased the category in the past three months"]],
      widths={1:22,2:12,3:42,4:24,5:44},fmts={2:'0.0%'},
      note=("Supplied at the client's request for context. Note the universe and the recall window."))
wb.save(f"{OUT}/Benchmarks.xlsx")

# ---------------------------------------------------------- field report --
d=doc("FIELDWORK REPORT",f"Halloway Brand Tracker, Wave {t.WAVE} | {t.AGENCY} | Field 4 to 12 May 2026")
d.add_paragraph("Field closed on 12 May with 1,334 completes against a target of 1,300. Three matters "
                "arose during fieldwork that the analysis team should be aware of.")
head(d,"1. Panel supplier substitution")
d.add_paragraph("Sample was ordered from Meridian Panels as in previous waves. Meridian advised on the "
                "evening of day 3 that it could not deliver the remaining completes within the field "
                "window. The balance was sourced from Colwyn Audience, which is on our approved list "
                "but has not been used on this tracker before. Colwyn supplied from day 4 onwards. "
                "Colwyn's panel is understood to be more heavily weighted towards younger and more "
                "urban respondents than Meridian's.")
head(d,"2. Quota shortfalls")
d.add_paragraph(f"Two interlocking quota cells closed short. The 65 and over cell achieved against a "
                f"target of {t.QUOTA_TARGETS['65+']} and the Northeast cell against a target of "
                f"{t.QUOTA_TARGETS['Northeast']}. Colwyn was unable to deliver further completes in "
                f"either cell within the field window and the client declined an extension.")
head(d,"3. Screener wording")
d.add_paragraph("An editing error meant that on days 1 and 2 the category screener at Q2 asked about "
                "purchase in the past three months rather than the past twelve months, which is the "
                "standing wording. The error was identified on the morning of day 3 and corrected. "
                "Respondents interviewed on days 1 and 2 carry screener_version v1_3month in the data "
                "file; all others carry v2_12month. The error affected only Q2. Screening for the "
                "survey overall is on age and country of residence and was unaffected, so the achieved "
                "sample remains a general adult sample.")
head(d,"4. Data quality")
d.add_paragraph("No quality removals have been applied to the delivered file. Length of interview is "
                "recorded in minutes and the eight-item battery is delivered as recorded. The analysis "
                "team should apply the standing rules.")
d.save(f"{OUT}/Field_Report.docx")

# ------------------------------------------------------------ method note -
d=doc("TRACKER METHOD NOTE",f"Halloway Brand Tracker | {t.AGENCY} | Standing methodology, revision 4")
head(d,"Universe and base")
d.add_paragraph("The tracker measures adults 18 and over in the United States. The base for all "
                "headline metrics is all adults, not category users. Awareness, consideration and "
                "past twelve month use are reported on that base.")
head(d,"Quality removals")
d.add_paragraph(f"Removals are applied before weighting, in this order. First, any respondent whose "
                f"length of interview is below one third of the median length of interview for the "
                f"wave. Second, any respondent giving an identical response to all "
                f"{t.BATTERY_ITEMS} items of the attribute battery. A respondent failing both rules "
                f"is removed once.")
head(d,"Weighting")
d.add_paragraph(f"Weights are produced by iterative proportional fitting to three margins: age band "
                f"by gender interlocked, region, and highest educational attainment. Weights are "
                f"scaled to a mean of one. After fitting, weights are trimmed at "
                f"{t.TRIM_LOW:.2f} and {t.TRIM_HIGH:.2f} and the fit is repeated, for up to "
                f"{t.TRIM_CYCLES} cycles. Margins not listed above are not used as weighting margins, "
                f"whatever reference data may be available for them.")
head(d,"Precision")
d.add_paragraph("Effective sample size is the square of the sum of the weights divided by the sum of "
                "the squared weights. The design effect is the achieved sample size divided by the "
                "effective sample size. Margins of error are reported at ninety five percent "
                "confidence and are computed on the effective sample size, not on the achieved sample "
                "size.")
head(d,"Trend")
d.add_paragraph("Waves are comparable only where the same weighting scheme has been applied. Prior "
                "wave awareness on this scheme was as follows.")
for k,v in sorted(t.PRIOR_WAVES.items()):
    p=d.add_paragraph(style="List Bullet"); p.add_run(f"Wave {k}: {v*100:.1f} per cent")
d.save(f"{OUT}/Method_Note.docx")
print("\n".join(sorted(os.listdir(OUT))))
