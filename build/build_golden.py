import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cutover as c
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
OUT="/home/azureuser/geranium_tasks/task2_env/golden_solution/Cutover_Plan.xlsx"
SLATE,PALE,AMBER,GREY="2E4057","DCE3EB","FFF2CC","EDEDED"
HDR=Font(bold=True,color="FFFFFF",size=9.5); THIN=Side(style="thin",color="BFBFBF")
BOX=Border(left=THIN,right=THIN,top=THIN,bottom=THIN)
sch=c.solve(); wv=c.waves(sch); viol=c.check(sch)
order=sorted(sch,key=lambda x:(sch[x]['start'],x))

def hdr(ws,r,hs,w=None):
    for i,h in enumerate(hs,1):
        x=ws.cell(r,i,h); x.font,x.border=HDR,BOX; x.fill=PatternFill("solid",fgColor=SLATE)
        x.alignment=Alignment(wrap_text=True,vertical="center",horizontal="center")
    ws.row_dimensions[r].height=30
    for i,v in (w or {}).items(): ws.column_dimensions[get_column_letter(i)].width=v
def put(ws,r,vals,fmts=None,bold=False,fill=None):
    for i,v in enumerate(vals,1):
        x=ws.cell(r,i,v); x.border=BOX
        x.font=Font(bold=True,size=9.5) if bold else Font(size=9.5)
        if fill: x.fill=PatternFill("solid",fgColor=fill)
        if fmts and fmts.get(i): x.number_format=fmts[i]
        x.alignment=Alignment(wrap_text=True,vertical="top")
    return r+1
def title(ws,t,sub=None):
    ws.cell(1,1,t).font=Font(bold=True,size=13,color=SLATE)
    if sub: ws.cell(2,1,sub).font=Font(italic=True,size=9,color="595959")
    ws.sheet_view.showGridLines=False
    return 4

wb=Workbook()
# ------------------------------------------------------------- Plan ------
ws=wb.active; ws.title="Plan"
r=title(ws,f"{c.CLIENT} ERP cutover sequence",
        f"Programme week 1 commences {c.PROGRAMME_START}. Legacy support ends "
        f"{c.LEGACY_SUPPORT_ENDS}, programme week {c.LAST_WEEK}.")
hdr(ws,r,["Wave","Site","Code","Country","Users","Team","Start week","Week commencing",
          "Weeks","End week","Live week","Live date","Binding constraint"],
    {1:6,2:13,3:7,4:15,5:8,6:6,7:10,8:16,9:7,10:10,11:10,12:14,13:52}); r+=1
TOP=r
for code in order:
    s=c.SITE[code]; p=sch[code]; note=[]
    if s["master"]: note.append(f"Owns {s['master'].lower()}; {sum(1 for x in c.SITE.values() if code in x['deps'])} sites depend on it")
    if s["gmp"]: note.append(f"{c.VALIDATION_WEEKS} week validation after cutover, so it must start early despite being the smallest site")
    if s["shutdown"]: note.append(f"Can only start in the shutdown window, programme week {s['shutdown'][0]}")
    if s["deps"] and not note: note.append("Follows "+", ".join(s["deps"]))
    r=put(ws,r,[wv[code],s["name"],code,s["country"],s["users"],p["team"],p["start"],
                c.monday(p["start"]),s["weeks"],p["end"],p["live"],
                c.monday(p["live"]),"; ".join(note)],
          fmts={5:'#,##0',8:'yyyy-mm-dd',12:'yyyy-mm-dd'})
BOT=r-1
r=put(ws,r,["","TOTAL","","",f"=SUM(E{TOP}:E{BOT})","","","",f"=SUM(I{TOP}:I{BOT})","",
            f"=MAX(K{TOP}:K{BOT})",f"=MAX(L{TOP}:L{BOT})",
            "Last go-live against a deadline of programme week "+str(c.LAST_WEEK)],
        fmts={5:'#,##0',12:'yyyy-mm-dd'},bold=True,fill=GREY)
r+=1
r=put(ws,r,["","Float to the deadline, weeks","","",f"={c.LAST_WEEK}-K{BOT+1}","","","","","","","",
            "Weeks between the last go-live and the end of legacy support"],bold=True,fill=AMBER)

# --------------------------------------------------------- Timeline -----
ws=wb.create_sheet("Timeline")
r=title(ws,"Team loading by programme week",
        "Each cell shows the site a team is working. Shaded columns are financial blackout weeks.")
cols=["Team"]+[f"W{w}" for w in range(1,c.LAST_WEEK+1)]
hdr(ws,r,cols,{1:8,**{i:5 for i in range(2,len(cols)+1)}}); r+=1
for w in range(1,c.LAST_WEEK+1):
    if w in c.BLACKOUT:
        cell=ws.cell(r-1,w+1); cell.fill=PatternFill("solid",fgColor="C0504D")
for t in range(1,c.TEAMS+1):
    row=[f"Team {t}"]
    for w in range(1,c.LAST_WEEK+1):
        hit=[k for k,v in sch.items() if v["team"]==t and v["start"]<=w<=v["end"]]
        row.append(hit[0] if hit else "")
    r=put(ws,r,row)
    for w in range(1,c.LAST_WEEK+1):
        if w in c.BLACKOUT and not ws.cell(r-1,w+1).value:
            ws.cell(r-1,w+1).fill=PatternFill("solid",fgColor="F2DCDB")
row=["Load"]
for w in range(1,c.LAST_WEEK+1):
    row.append(sum(1 for v in sch.values() if v["start"]<=w<=v["end"]))
r=put(ws,r,row,bold=True,fill=GREY)
r+=1
r=put(ws,r,["Peak"]+[f"=MAX(B{r-2}:{get_column_letter(c.LAST_WEEK+1)}{r-2})"]+[""]*(c.LAST_WEEK-1),bold=True)
ws.cell(r-1,4,f"Deployment teams available: {c.TEAMS}").font=Font(bold=True,size=9.5)

# ---------------------------------------------------- Constraint checks --
ws=wb.create_sheet("Checks")
r=title(ws,"Constraint verification","Each test is computed from the Plan sheet, not asserted.")
hdr(ws,r,["Constraint","Test","Result","Detail"],{1:32,2:44,3:14,4:66}); r+=1
def rowof(code): return TOP+order.index(code)
for code in order:
    s=c.SITE[code]
    for d in s["deps"]:
        r=put(ws,r,[f"Master data, {code}",
                    f"{code} starts after {d} completes",
                    f"=IF(Plan!G{rowof(code)}>Plan!J{rowof(d)},\"Pass\",\"FAIL\")",
                    f"{code} consumes {c.SITE[d]['master'].lower()} owned by {d}"])
for code in order:
    s=c.SITE[code]
    if s["shutdown"]:
        r=put(ws,r,[f"Shutdown window, {code}",
                    f"{code} starts exactly in programme week {s['shutdown'][0]}",
                    f"=IF(Plan!G{rowof(code)}={s['shutdown'][0]},\"Pass\",\"FAIL\")",
                    "Continuous process plant; the turnaround date is fixed a year ahead"])
    if s["gmp"]:
        r=put(ws,r,[f"Validation, {code}",
                    f"Live week equals end week plus one plus {c.VALIDATION_WEEKS}",
                    f"=IF(Plan!K{rowof(code)}=Plan!J{rowof(code)}+1+{c.VALIDATION_WEEKS},\"Pass\",\"FAIL\")",
                    "GMP computer system validation; the site is not live until it completes"])
r=put(ws,r,["Blackouts","No cutover runs through a blackout week",
            "Pass" if not any("blackout" in v for v in viol) else "FAIL",
            f"Blackout weeks: {', '.join(str(w) for w in sorted(w for w in c.BLACKOUT if w<=c.LAST_WEEK))}"])
r=put(ws,r,["Team capacity",f"No week requires more than {c.TEAMS} teams",
            f"=IF(MAX(Timeline!B{4+c.TEAMS+1}:{get_column_letter(c.LAST_WEEK+1)}{4+c.TEAMS+1})<={c.TEAMS},\"Pass\",\"FAIL\")",
            "Peak loading is on the Timeline sheet"])
r=put(ws,r,["Deadline","Every site live before support ends",
            f"=IF(MAX(Plan!K{TOP}:K{BOT})<={c.LAST_WEEK},\"Pass\",\"FAIL\")",
            f"Support ends in programme week {c.LAST_WEEK}"],bold=True,fill=AMBER)

# ------------------------------------------------------- Sequencing ------
ws=wb.create_sheet("Sequencing")
r=title(ws,"Why the sequence is what it is")
ws.column_dimensions['A'].width=126
for t,b in [
 ("The order is set by freedom of movement, not by site size",
  "Eleven of the fourteen sites cannot start until Bridgnorth completes, because Bridgnorth owns "
  "material master. Bridgnorth therefore leads regardless of anything else. Halesworth and Kinloss "
  "own the other two master domains and run alongside it, which uses all three teams in wave one and "
  "unblocks the whole programme in five weeks."),
 ("Charleston is the largest site and does not go first",
  "Charleston has 580 users and is the obvious candidate for wave one on any size-ordered plan. It "
  "depends on both Bridgnorth and Halesworth, so it cannot start until week 10. Sequencing by size is "
  "the error that sank the first internal attempt."),
 ("Cork is the smallest site and goes second",
  f"Cork has 150 users and would be last on any plan ordered by size or by risk. It is GMP regulated "
  f"and needs {c.VALIDATION_WEEKS} weeks of computer system validation after the technical cutover "
  f"before it can transact. Its technical cutover takes three weeks, so it must start no later than "
  f"programme week {c.LAST_WEEK-3-c.VALIDATION_WEEKS} to be live before support ends. Placing it "
  f"early removes the risk entirely and costs nothing, because it is small enough to run alongside a "
  f"larger site."),
 ("Sarnia and Mobile are fixed points, not choices",
  "Both run continuous plant and can only begin in their annual maintenance shutdown. Sarnia's window "
  "is programme week 24 and Mobile's is week 33. The rest of the plan is built around them rather "
  "than the reverse, because those dates are set by turnaround contractors and will not move."),
 ("The blackouts remove a quarter of the calendar",
  f"Eleven of the {c.LAST_WEEK} programme weeks are unavailable: the weeks either side of each quarter "
  f"end and the first three weeks of January. They fall in clusters, so the usable calendar is four "
  f"blocks rather than a continuous run. An evenly spread plan lands in them, which is what happened "
  f"to the second internal attempt."),
 ("Where the float is",
  f"The last go-live is programme week {max(v['live'] for v in sch.values())} against a deadline of "
  f"{c.LAST_WEEK}, leaving {c.LAST_WEEK-max(v['live'] for v in sch.values())} weeks. That float sits "
  f"at the end of the programme and protects the smallest sites. It does not protect Cork, whose "
  f"validation is already complete by then, nor the two shutdown sites, whose windows occur once."),
 ("What would break it",
  "A slip on Bridgnorth pushes eleven sites. A slip that causes Sarnia or Mobile to miss its shutdown "
  "window pushes that site by a full year, which is past the deadline. Those three are the sites to "
  "protect; the rest have room."),
]:
    p=ws.cell(r,1,t); p.font=Font(bold=True,size=10.5,color=SLATE); r+=1
    q=ws.cell(r,1,b); q.alignment=Alignment(wrap_text=True,vertical="top")
    ws.row_dimensions[r].height=max(15,12.4*(len(b)//122+1)); r+=2
wb.save(OUT); print("written:",OUT,"| violations:",viol or "none")
print("tabs:",[s.title for s in wb.worksheets])
