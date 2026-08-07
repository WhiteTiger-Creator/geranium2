import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tracker as t
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
OUT="/home/azureuser/geranium_tasks/task2_env/golden_solution/Wave12_Weighted.xlsx"
PLUM,PALE,GREY,AMBER="5B2C4E","F0E4EC","EDEDED","FFF2CC"
HDR=Font(bold=True,color="FFFFFF",size=9.5)
THIN=Side(style="thin",color="BFBFBF"); BOX=Border(left=THIN,right=THIN,top=THIN,bottom=THIN)
P2,P1,N3,N1='0.00%','0.0%','0.000','0.0'

def hdr(ws,r,hs,w=None):
    for i,h in enumerate(hs,1):
        c=ws.cell(r,i,h); c.font,c.border=HDR,BOX; c.fill=PatternFill("solid",fgColor=PLUM)
        c.alignment=Alignment(wrap_text=True,vertical="center",horizontal="center")
    ws.row_dimensions[r].height=30
    for i,v in (w or {}).items(): ws.column_dimensions[get_column_letter(i)].width=v

def put(ws,r,vals,fmts=None,bold=False,fill=None):
    for i,v in enumerate(vals,1):
        c=ws.cell(r,i,v); c.border=BOX
        c.font=Font(bold=True,size=9.5) if bold else Font(size=9.5)
        if fill: c.fill=PatternFill("solid",fgColor=fill)
        if fmts and fmts.get(i): c.number_format=fmts[i]
        c.alignment=Alignment(wrap_text=True,vertical="top")
    return r+1

def title(ws,tx,sub=None):
    ws.cell(1,1,tx).font=Font(bold=True,size=13,color=PLUM)
    if sub: ws.cell(2,1,sub).font=Font(italic=True,size=9,color="595959")
    ws.sheet_view.showGridLines=False
    return 4

rows=t.build_sample(); med,cut=t.flag_quality(rows); cl=t.cleaned(rows)
w0=t.rake(cl); w=t.trim_and_rerake(cl,w0)
n=len(cl); ESS=t.ess(w); DEFF=t.deff(w)

wb=Workbook()
# ------------------------------------------------------------- Estimates --
ws=wb.active; ws.title="Estimates"
r=title(ws,f"Halloway Brand Tracker, Wave {t.WAVE} weighted estimates",
        "All adults 18 and over. Weighted on the standing scheme. Margins of error on the effective "
        "sample size.")
for c,wd in {1:34,2:16,3:16,4:16,5:14,6:60}.items(): ws.column_dimensions[get_column_letter(c)].width=wd
hdr(ws,r,["Metric","Unweighted","Weighted","Wave 11","Change vs W11","Note"]); r+=1
DATA_LAST=4+n
for label,field,prior in [("Aware of the brand","aware",0.664),
                          ("Would consider","consider",None),
                          ("Used in past 12 months","used_12m",None)]:
    col={"aware":"K","consider":"L","used_12m":"M"}[field]
    r=put(ws,r,[label,
                f"=AVERAGE(Weighted_Data!{col}5:{col}{DATA_LAST})",
                f"=SUMPRODUCT(Weighted_Data!{col}5:{col}{DATA_LAST},Weighted_Data!$T$5:$T${DATA_LAST})"
                f"/SUM(Weighted_Data!$T$5:$T${DATA_LAST})",
                prior if prior else "",
                f"=IF(D{r}=\"\",\"\",C{r}-D{r})",
                "" if field!="aware" else
                "The unweighted figure is what the raw file returns. It is not comparable to prior waves."],
             fmts={2:P2,3:P2,4:P2,5:P2}); 
AW=r-3
r+=1
r=put(ws,r,["Apparent change on the unweighted figure","",f"=B{AW}-D{AW}","","",
            "This is the number that prompted the query. It is an artefact of who answered."],
      fmts={3:P2},bold=True)
r=put(ws,r,["Change on the weighted figure","",f"=C{AW}-D{AW}","","",
            "The brand is flat within the margin of error. There is no wave 12 collapse."],
      fmts={3:P2},bold=True,fill=AMBER)
r+=1
r=put(ws,r,["Margin of error at 95%, on effective sample size","",
            f"=1.96*SQRT(0.25/Diagnostics!$B$8)","","",
            "Applied to a proportion near 50%. Computing this on the achieved sample would overstate "
            "precision."],fmts={3:P2},bold=True)
r+=2
for x in [
  "The wave 12 sample is not the population. Meridian delivered only the first three days and the "
  "balance came from Colwyn, whose panel is younger and more urban. Under 35s are 47.2% of the cleaned "
  "sample against 28.8% of the population, and the over 65s are 9.7% against 22.2%.",
  "Awareness rises steeply with age in this category, so a young sample reports low awareness. That is "
  "the whole of the apparent decline.",
  "The 65 and over and Northeast quota cells closed short, which the weighting corrects but at a cost "
  "in precision: the design effect is 1.31 and the effective sample is roughly 950 against 1,241 "
  "achieved.",
  "The syndicated category incidence figure in the benchmark file has not been used as a weighting "
  "margin. It is drawn from adults 21 and over on a three month recall window, neither of which "
  "matches this tracker, and category use is a measured outcome here rather than a demographic frame.",
  "Past twelve month use is reported on days 3 to 9 only. The screener wording on days 1 and 2 asked "
  "about three months, so those responses do not measure the same thing."]:
    c=ws.cell(r,1,x); c.alignment=Alignment(wrap_text=True,vertical="top")
    ws.merge_cells(start_row=r,start_column=1,end_row=r,end_column=6)
    ws.row_dimensions[r].height=max(14,12.2*(len(x)//118+1)); r+=1

# ------------------------------------------------------- Weighted_Data ----
ws=wb.create_sheet("Weighted_Data")
r=title(ws,"Cleaned respondent file with final weights",
        "Quality removals applied before weighting, per the method note. The weight column is the "
        "output of the iterative fit and is a value; everything derived from it is a formula.")
cols=["respondent_id","field_day","supplier","screener_version","loi_minutes","age_band","gender",
      "region","education","urbanicity","aware","consider","used_12m","b1","b2","b3","b4","b5",
      "raw_weight","final_weight"]
hdr(ws,r,cols,{1:14,2:9,3:11,4:15,5:11,6:10,7:9,8:12,9:20,10:11,11:8,12:9,13:11,
               14:6,15:6,16:6,17:6,18:6,19:12,20:12}); r+=1
for rec,a,b in zip(cl,w0,w):
    put(ws,r,[rec["respondent_id"],rec["field_day"],rec["supplier"],rec["screener_version"],
              rec["loi_minutes"],rec["age_band"],rec["gender"],rec["region"],rec["education"],
              rec["urbanicity"],rec["aware"],rec["consider"],rec["used_12m"],
              rec["b1"],rec["b2"],rec["b3"],rec["b4"],rec["b5"],round(a,6),round(b,6)],
        fmts={5:N1,19:N3,20:N3}); r+=1
ws.freeze_panes=ws.cell(5,1)

# ---------------------------------------------------------- Cleaning ------
ws=wb.create_sheet("Cleaning")
r=title(ws,"Quality removals","Applied before weighting, in the order set out in the method note.")
for c,wd in {1:44,2:14,3:70}.items(): ws.column_dimensions[get_column_letter(c)].width=wd
hdr(ws,r,["Step","Count","Note"]); r+=1
sp=sum(1 for x in rows if x["_speeder"]); st=sum(1 for x in rows if x["_straight"])
both=sum(1 for x in rows if x["_speeder"] and x["_straight"])
r=put(ws,r,["Completes delivered",len(rows),""])
r=put(ws,r,["Median length of interview, minutes",med,"Computed on all delivered completes"],fmts={2:N1})
r=put(ws,r,["Speeder threshold, minutes",cut,"One third of the median"],fmts={2:'0.00'})
r=put(ws,r,["Removed as speeders",sp,""])
r=put(ws,r,["Removed as straightliners",st,f"Identical response to all {t.BATTERY_ITEMS} battery items"])
r=put(ws,r,["Failing both rules",both,"Removed once, not twice"])
r=put(ws,r,["Cleaned base for weighting",n,""],bold=True,fill=AMBER)

# ---------------------------------------------------------- Margins -------
ws=wb.create_sheet("Margins")
r=title(ws,"Weighting margins","Achieved against benchmark, before and after fitting.")
for c,wd in {1:16,2:14,3:14,4:16,5:16,6:16,7:16}.items(): ws.column_dimensions[get_column_letter(c)].width=wd
for name,target in t.MARGINS:
    ws.cell(r,1,name.replace("_"," ").title()).font=Font(bold=True,color=PLUM); r+=1
    hdr(ws,r,["Cell","","Benchmark","Achieved n","Achieved share","Weighted share","Deviation"]); r+=1
    for k,v in target.items():
        cnt=sum(1 for x in cl if t.key(x,name)==k)
        wt=sum(wi for x,wi in zip(cl,w) if t.key(x,name)==k)/sum(w)
        lab=k if isinstance(k,str) else k[0]; lab2="" if isinstance(k,str) else k[1]
        r=put(ws,r,[lab,lab2,v,cnt,cnt/n,wt,wt-v],
              fmts={3:P1,5:P1,6:P1,7:'0.000%'})
    r+=1

# ------------------------------------------------------- Diagnostics ------
ws=wb.create_sheet("Diagnostics")
r=title(ws,"Weight diagnostics and precision")
for c,wd in {1:46,2:16,3:74}.items(): ws.column_dimensions[get_column_letter(c)].width=wd
hdr(ws,r,["Measure","Value","Note"]); r+=1
L=4+n
r=put(ws,r,["Cleaned sample size",n,""])
r=put(ws,r,["Minimum weight",f"=MIN(Weighted_Data!T5:T{L})",""],fmts={2:N3})
r=put(ws,r,["Maximum weight",f"=MAX(Weighted_Data!T5:T{L})",
            f"Trim bounds are {t.TRIM_LOW:.2f} and {t.TRIM_HIGH:.2f}"],fmts={2:N3})
r=put(ws,r,["Mean weight",f"=AVERAGE(Weighted_Data!T5:T{L})","Scaled to one"],fmts={2:N3})
r=put(ws,r,["Weights above the cap before trimming",
            sum(1 for x in w0 if x>t.TRIM_HIGH),"Trimmed, then the fit repeated"])
ESS_ROW=r
r=put(ws,r,["Effective sample size",
            f"=SUM(Weighted_Data!T5:T{L})^2/SUMPRODUCT(Weighted_Data!T5:T{L},Weighted_Data!T5:T{L})",""],
      fmts={2:N1},bold=True,fill=AMBER)
r=put(ws,r,["Design effect",f"=B5/B{ESS_ROW}","Achieved over effective"],fmts={2:N3},bold=True)
r=put(ws,r,["Margin of error at 95%, effective base",f"=1.96*SQRT(0.25/B{ESS_ROW})",
            "The figure to report"],fmts={2:P2},bold=True,fill=AMBER)
r=put(ws,r,["Margin of error if computed on the achieved base",f"=1.96*SQRT(0.25/B5)",
            "Understates the error. Not to be reported."],fmts={2:P2})

# ------------------------------------------------------------- Trend ------
ws=wb.create_sheet("Trend")
r=title(ws,"Awareness trend","Waves 9 to 11 as previously reported. Wave 12 on the same scheme.")
for c,wd in {1:12,2:18,3:18,4:66}.items(): ws.column_dimensions[get_column_letter(c)].width=wd
hdr(ws,r,["Wave","Awareness","Change","Note"]); r+=1
prev=None
for k in sorted(t.PRIOR_WAVES):
    v=t.PRIOR_WAVES[k]
    r=put(ws,r,[f"Wave {k}",v,"" if prev is None else v-prev,""],fmts={2:P1,3:P2}); prev=v
r=put(ws,r,["Wave 12","=Estimates!C5",f"=B{r}-B{r-1}",
            "On the weighted basis. Within the margin of error of wave 11."],
      fmts={2:P1,3:P2},bold=True,fill=AMBER)
r=put(ws,r,["Wave 12","=Estimates!B5",f"=B{r}-B{r-2}",
            "On the unweighted basis, for reference only. Not comparable to prior waves."],
      fmts={2:P1,3:P2})
wb.save(OUT); print("written:",OUT); print("tabs:",[s.title for s in wb.worksheets])
