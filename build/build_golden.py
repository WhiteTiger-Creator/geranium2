"""Golden solution: Cordell_NSR_Analysis.xlsx, built on live formulas."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cordell as c
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

OUT = "/home/azureuser/geranium_tasks/task2_env/golden_solution/Cordell_NSR_Analysis.xlsx"
TEAL, PALE, GREY, AMBER = "1B4F5C", "DCE9ED", "EDEDED", "FFF2CC"
HDR = Font(bold=True, color="FFFFFF", size=10)
IN_F, CA_F = Font(color="0033CC", size=10), Font(color="000000", size=10)
THIN = Side(style="thin", color="BFBFBF"); BOX = Border(left=THIN,right=THIN,top=THIN,bottom=THIN)
M0,M2,P1,N2,N4 = '#,##0','#,##0.00','0.0%','0.00','0.0000'

def hdr(ws,r,hs,w=None):
    for i,h in enumerate(hs,1):
        x=ws.cell(r,i,h); x.font,x.border=HDR,BOX; x.fill=PatternFill("solid",fgColor=TEAL)
        x.alignment=Alignment(wrap_text=True,vertical="center",horizontal="center")
    ws.row_dimensions[r].height=32
    for i,v in (w or {}).items(): ws.column_dimensions[get_column_letter(i)].width=v

def put(ws,r,vals,fmts=None,inputs=(),bold=False,fill=None):
    for i,v in enumerate(vals,1):
        x=ws.cell(r,i,v); x.border=BOX
        x.font=Font(bold=True,size=10) if bold else (IN_F if i in inputs else CA_F)
        if fill: x.fill=PatternFill("solid",fgColor=fill)
        if fmts and fmts.get(i): x.number_format=fmts[i]
        x.alignment=Alignment(wrap_text=True,vertical="top")
    return r+1

def title(ws,t,sub=None):
    ws.cell(1,1,t).font=Font(bold=True,size=13,color=TEAL)
    if sub: ws.cell(2,1,sub).font=Font(italic=True,size=9,color="595959")
    ws.sheet_view.showGridLines=False
    return 4

def build():
    wb=Workbook(); A={}
    # ---------------------------------------------------------- A_Inputs ---
    ws=wb.active; ws.title="A_Inputs"
    r=title(ws,"Inputs","Blue cells are values taken from the issued documents. Black cells are formulas.")
    ws.column_dimensions['A'].width=58
    for cc in "BC": ws.column_dimensions[cc].width=16
    ws.column_dimensions['D'].width=62
    def row(k,l,v,f=None,src="",inp=True):
        nonlocal r
        A[k]=f"A_Inputs!$B${r}"; put(ws,r,[l,v,"",src],fmts={2:f},inputs=(2,) if inp else ()); r+=1
    ws.cell(r,1,"THRESHOLDS, CALVERT AIR REGULATION 5").font=Font(bold=True,color=TEAL); r+=1
    row("major","Major stationary source, VOC, tpy",c.MAJOR_VOC_TPY,M2,"5.02(a)")
    row("sig","Significant net emissions increase, VOC, tpy",c.SIGNIFICANT_VOC_TPY,M2,"5.03(a)")
    row("hap1","HAP major, single pollutant, tpy",c.HAP_SINGLE_TPY,M2,"5.09")
    row("hapagg","HAP major, aggregate, tpy",c.HAP_AGGREGATE_TPY,M2,"5.09")
    row("ratio","Offset ratio",c.OFFSET_RATIO,N2,"5.06")
    r+=1
    ws.cell(r,1,"EXISTING FACILITY").font=Font(bold=True,color=TEAL); r+=1
    row("cap","Permitted facility-wide VOC potential to emit, tpy",c.PERMITTED_VOC_CAP_TPY,M2,"Permit 3.1")
    row("fug","Fugitive VOC, tpy",c.FUGITIVE_VOC_TPY,M2,"07_Facility_Emissions")
    row("xex","Existing xylene potential to emit, tpy",c.EXISTING_HAP_TPY["Xylene"],M2,"07_Facility_Emissions")
    row("tex","Existing toluene potential to emit, tpy",c.EXISTING_HAP_TPY["Toluene"],M2,"07_Facility_Emissions")
    r+=1
    ws.cell(r,1,"LINE 4").font=Font(bold=True,color=TEAL); r+=1
    row("gal","Maximum design coating rate, gal/day",c.L4_DESIGN_GAL_DAY,M2,"02_Line4_Design_Data")
    row("days","Days per year for potential to emit",c.PTE_DAYS_PER_YEAR,'0',
        "8,760 hours. Reg 5.02(b): an unpermitted schedule is not counted")
    row("vocg","Coating VOC less water, lb/gal",c.COATING["voc_less_water_lb_gal"],M2,
        "03_Coating_Data_Sheets. The as-supplied value includes water and is not the regulatory basis")
    row("xyg","Coating xylene less water, lb/gal",c.COATING["xylene_less_water_lb_gal"],M2,"03_Coating_Data_Sheets")
    row("clg","Cleanup solvent, gal/month",c.CLEANUP["gal_per_month"],M2,"02_Line4_Design_Data")
    row("clv","Cleanup solvent VOC, lb/gal",c.CLEANUP["voc_lb_gal"],M2,"03_Coating_Data_Sheets")
    row("clt","Cleanup solvent toluene, lb/gal",c.CLEANUP["toluene_lb_gal"],M2,"03_Coating_Data_Sheets")
    r+=1
    ws.cell(r,1,"CONTROLS").font=Font(bold=True,color=TEAL); r+=1
    row("dre","Oxidiser destruction efficiency",c.RTO_DESTRUCTION,P1,"06_Control_Equipment")
    row("cap1","Capture, hood arrangement as quoted",c.RTO_CAPTURE_AS_DESIGNED,P1,"06_Control_Equipment")
    row("cap2","Capture, permanent total enclosure",c.ENCLOSURE_CAPTURE,P1,"06_Control_Equipment")
    r+=1
    ws.cell(r,1,"CONTEMPORANEOUS ACTIVITY").font=Font(bold=True,color=TEAL); r+=1
    row("l2","Line 2 debottleneck, VOC increase, tpy",c.LINE2_DEBOTTLENECK["voc_tpy"],M2,
        "Aug 2025, unpermitted. Reg 5.03(b) aggregates changes within three years")
    row("l2x","Line 2 debottleneck, xylene increase, tpy",c.LINE2_DEBOTTLENECK["xylene_tpy"],M2,"")
    row("l1","Line 1 shutdown, VOC decrease, tpy",c.LINE1_SHUTDOWN["voc_tpy"],M2,
        "Not creditable. Relied upon in full in revision R-23-0412, and Reg 5.04(b) removes netting here")

    # ------------------------------------------------------- B_Line4_PTE ---
    ws=wb.create_sheet("B_Line4_PTE")
    r=title(ws,"Line 4 potential to emit",
            "Potential to emit uses maximum design capacity and 8,760 hours. The plant's one-shift "
            "schedule is not a permit condition and under Regulation 5.02(b) cannot be counted.")
    hdr(ws,r,["Stream","Quantity","Unit","VOC lb/gal","Uncontrolled lb/yr","Uncontrolled tpy",
              "Controlled?","Overall control","Controlled tpy"],
        {1:30,2:12,3:10,4:12,5:18,6:16,7:12,8:14,9:14}); r+=1
    put(ws,r,["Coating application",f"={A['gal']}*{A['days']}","gal/yr",f"={A['vocg']}",
              f"=B{r}*D{r}",f"=E{r}/2000","Yes",f"={A['cap1']}*{A['dre']}",f"=F{r}*(1-H{r})"],
        fmts={2:M0,4:M2,5:M0,6:M2,8:N4,9:M2}); coat=r; r+=1
    put(ws,r,["Cleanup solvent",f"={A['clg']}*12","gal/yr",f"={A['clv']}",f"=B{r}*D{r}",
              f"=E{r}/2000","No",0,f"=F{r}"],
        fmts={2:M0,4:M2,5:M0,6:M2,8:N4,9:M2}); clean=r; r+=1
    A["l4"]=f"B_Line4_PTE!$I${r}"
    put(ws,r,["Line 4 potential to emit","","","","","","","",f"=I{coat}+I{clean}"],
        fmts={9:M2},bold=True,fill=AMBER); r+=2
    put(ws,r,["With a permanent total enclosure","","","","","",
              "",f"={A['cap2']}*{A['dre']}",f"=F{coat}*(1-H{r})+I{clean}"],
        fmts={8:N4,9:M2},bold=True); A["l4e"]=f"B_Line4_PTE!$I${r}"; r+=2
    put(ws,r,["Note",f"Using the as-supplied VOC content of {c.COATING['voc_as_supplied_lb_gal']:.2f} "
              f"lb/gal instead of the less-water value would understate the coating stream by about "
              f"{(1-c.COATING['voc_as_supplied_lb_gal']/c.COATING['voc_less_water_lb_gal']):.0%}. "
              f"Crediting the 98 percent destruction efficiency without applying capture would "
              f"understate it further.","","","","","","",""],bold=True,fill=PALE)

    # ------------------------------------------------------ C_Applicability
    ws=wb.create_sheet("C_Applicability")
    r=title(ws,"Applicability under Calvert Air Regulation 5")
    hdr(ws,r,["Step","Value, tpy","Threshold, tpy","Test","Conclusion"],
        {1:52,2:14,3:16,4:14,5:60}); r+=1
    put(ws,r,["Line 4 potential to emit",f"={A['l4']}","","",
              "New emission unit, so the increase equals the potential to emit"],fmts={2:M2}); r+=1
    put(ws,r,["Line 2 debottleneck, aggregated under 5.03(b)",f"={A['l2']}","","",
              "Completed within three years and unpermitted. Aggregation does not depend on whether a "
              "permit was obtained"],fmts={2:M2}); r+=1
    A["proj"]=f"C_Applicability!$B${r}"
    put(ws,r,["PROJECT EMISSIONS INCREASE",f"=B{r-2}+B{r-1}",f"={A['sig']}",
              f'=IF(B{r}>=C{r},"at or above","below")',
              "Below the significance threshold. This is the figure the client relied on and it is not "
              "the operative test"],fmts={2:M2,3:M2},bold=True); r+=1
    put(ws,r,["Existing permitted facility potential to emit",f"={A['cap']}","","",
              "Federally enforceable synthetic minor limit, Permit condition 3.1"],fmts={2:M2}); r+=1
    put(ws,r,["Fugitive emissions",f"={A['fug']}","","",
              "EXCLUDED. Reg 5.02(c): surface coating manufacture is not a listed category, so "
              "fugitives are not counted in the major source determination"],fmts={2:M2}); r+=1
    A["fac"]=f"C_Applicability!$B${r}"
    put(ws,r,["FACILITY POTENTIAL TO EMIT AFTER THE PROJECT",f"={A['cap']}+{A['proj']}",f"={A['major']}",
              f'=IF(B{r}>=C{r},"MAJOR","minor")',
              "The project takes the facility across the major source threshold"],
        fmts={2:M2,3:M2},bold=True,fill=AMBER); r+=1
    put(ws,r,["Netting against the 2022 Line 1 shutdown","","","Not available",
              "Two independent reasons. Reg 5.04(b) removes netting where a project makes a minor "
              "source major, and Reg 5.05 bars a decrease already relied upon in revision R-23-0412"],
        bold=True); r+=2
    put(ws,r,["GOVERNING CONCLUSION","","","",
              "The project is reviewed as a NEW MAJOR STATIONARY SOURCE under Reg 5.04(b). The whole "
              "project is subject to review, lowest achievable emission rate applies and offsets are "
              "required. The significance threshold is irrelevant because the source is not already "
              "major."],bold=True,fill=AMBER); r+=2
    put(ws,r,["If fugitives were wrongly included",f"={A['fac']}+{A['fug']}",f"={A['major']}",
              f'=IF(B{r}>=C{r},"MAJOR","minor")',"Shown to demonstrate the sensitivity"],
        fmts={2:M2,3:M2}); r+=1
    put(ws,r,["If the one-shift schedule were wrongly credited",
              f"={A['cap']}+{A['l4']}*{c.CLIENT_STATED_DAYS}/{A['days']}+{A['l2']}",f"={A['major']}",
              f'=IF(B{r}>=C{r},"MAJOR","minor")',
              "Still major, and in any event not permissible under Reg 5.02(b)"],
        fmts={2:M2,3:M2}); r+=1

    # ------------------------------------------------------------ D_HAP ---
    ws=wb.create_sheet("D_HAP")
    r=title(ws,"Hazardous air pollutants")
    hdr(ws,r,["Pollutant","Existing tpy","Line 4 tpy","Line 2 tpy","Total tpy","Threshold","Test"],
        {1:16,2:14,3:14,4:14,5:14,6:14,7:14}); r+=1
    put(ws,r,["Xylene",f"={A['xex']}",
              f"={A['gal']}*{A['days']}*{A['xyg']}/2000*(1-{A['cap1']}*{A['dre']})",f"={A['l2x']}",
              f"=B{r}+C{r}+D{r}",f"={A['hap1']}",f'=IF(E{r}>=F{r},"major","below")'],
        fmts={2:M2,3:M2,4:M2,5:M2,6:M2}); xr=r; r+=1
    put(ws,r,["Toluene",f"={A['tex']}",f"={A['clg']}*12*{A['clt']}/2000",0,
              f"=B{r}+C{r}+D{r}",f"={A['hap1']}",f'=IF(E{r}>=F{r},"major","below")'],
        fmts={2:M2,3:M2,4:M2,5:M2,6:M2}); tr=r; r+=1
    put(ws,r,["Aggregate","","","",f"=E{xr}+E{tr}",f"={A['hapagg']}",
              f'=IF(E{r}>=F{r},"major","below")'],fmts={5:M2,6:M2},bold=True); r+=2
    put(ws,r,["Conclusion","The facility does not become major for hazardous air pollutants under "
              "either control option. Xylene is the closer of the two and should be re-checked if the "
              "coating formulation changes.","","","","",""],bold=True,fill=PALE)

    # ------------------------------------------------------- E_Options ----
    ws=wb.create_sheet("E_Options")
    r=title(ws,"Options and cost")
    hdr(ws,r,["Option","Facility PTE after, tpy","Result","Capital and services","Offsets",
              "Total","Months","Assessment"],
        {1:34,2:16,3:12,4:18,5:14,6:16,7:12,8:58}); r+=1
    put(ws,r,["A. Accept major source review",f"={A['fac']}",'="MAJOR"',
              f"={c.COSTS['Lowest achievable emission rate control upgrade']}+"
              f"{c.COSTS['Major source permitting, modelling and application']}",
              f"={A['proj']}*{A['ratio']}*{c.OFFSET_COST_PER_TON}",f"=D{r}+E{r}",
              f"{c.SCHEDULE_MONTHS['major source review'][0]} to {c.SCHEDULE_MONTHS['major source review'][1]}",
              "Lowest achievable emission rate plus offsets. The schedule alone defeats the second "
              "quarter start the client needs."],
        fmts={2:M2,4:M0,5:M0,6:M0}); optA=r; r+=1
    put(ws,r,["B. Cap Line 4 throughput",f"={A['cap']}+{c.MAJOR_VOC_TPY-0.1-c.PERMITTED_VOC_CAP_TPY}",
              '="minor"',f"={c.COSTS['Minor permit revision, dispersion modelling and application']}",0,
              f"=D{r}+E{r}",
              f"{c.SCHEDULE_MONTHS['minor revision'][0]} to {c.SCHEDULE_MONTHS['minor revision'][1]}",
              f"Requires a federally enforceable limit of about {c.capped_throughput_gal_day():.0f} "
              f"gal/day, which is {c.capped_throughput_gal_day()/c.L4_DESIGN_GAL_DAY:.0%} of the design "
              f"rate. Cheap to permit and expensive to live with."],
        fmts={2:M2,4:M0,5:M0,6:M0}); r+=1
    put(ws,r,["C. Permanent total enclosure",f"={A['cap']}+{A['l4e']}+{A['l2']}",
              f'=IF(B{r}>={A["major"]},"MAJOR","minor")',
              f"={c.COSTS['Permanent total enclosure and ductwork, Line 4']}+"
              f"{c.COSTS['Regenerative thermal oxidiser capacity upsizing']}+"
              f"{c.COSTS['Minor permit revision, dispersion modelling and application']}",0,
              f"=D{r}+E{r}",
              f"{c.SCHEDULE_MONTHS['minor revision'][0]} to {c.SCHEDULE_MONTHS['minor revision'][1]}",
              "RECOMMENDED. Raises overall control from 90.2 to 98 percent, keeps the facility below "
              "the threshold at full design throughput, and permits as a minor revision."],
        fmts={2:M2,4:M0,5:M0,6:M0},bold=True,fill=AMBER); optC=r; r+=1
    r+=1
    put(ws,r,["Option A less Option C","","","","",f"=F{optA}-F{optC}","",
              "The enclosure pays for itself several times over against the major source route, before "
              "the schedule is considered."],fmts={6:M0},bold=True); r+=1
    put(ws,r,["Margin to the threshold under Option C",f"={A['major']}-{A['cap']}-{A['l4e']}-{A['l2']}",
              "","","","","","Headroom in tons per year. Thin enough that the Line 2 change must be "
              "permitted and the enclosure must be verified to the agency's criteria."],
        fmts={2:M2},bold=True)

    # ------------------------------------------------------- 00_Answer ----
    ws=wb.create_sheet("00_Answer",0)
    ws.column_dimensions['A'].width=56; ws.column_dimensions['B'].width=18
    ws.column_dimensions['C'].width=78; ws.sheet_view.showGridLines=False
    ws.cell(1,1,f"{c.FACILITY} - Line 4 New Source Review applicability").font=Font(bold=True,size=15,color=TEAL)
    ws.cell(2,1,f"{c.LOCATION} | Prepared by {FIRM_} | May 2026").font=Font(italic=True,size=9,color="595959")
    r=4
    for lbl,val,note,fmt in [
        ("Project emissions increase",f"={A['proj']}",
         "Line 4 plus the Line 2 debottleneck, aggregated under Regulation 5.03(b). Below the 40 tpy "
         "significance threshold, which is the figure the client relied on.",M2),
        ("Facility potential to emit after the project",f"={A['fac']}",
         "Against a 100 tpy major source threshold. The project takes the facility over it.",M2),
        ("ANSWER","Major source review is triggered",
         "Not as a major modification. Under Regulation 5.04(b) a project that makes a minor source "
         "major is reviewed as a new major stationary source, the whole project is subject to review, "
         "and netting is not available. The significance threshold never comes into it.",None),
        ("","","",None),
        ("Recommended course","Permanent total enclosure",
         "Raising capture from 92 to 100 percent lifts overall control from 90.2 to 98 percent and "
         "brings the facility back under the threshold at full design throughput.",None),
        ("Facility potential to emit under the recommendation",f"={A['cap']}+{A['l4e']}+{A['l2']}",
         "Below 100 tpy, so the project permits as a minor revision.",M2),
        ("Cost of the recommendation",f"='E_Options'!$F${optC}",
         "Enclosure, oxidiser upsizing and the permit revision.",M0),
        ("Cost avoided against major source review",f"='E_Options'!$F${optA}-'E_Options'!$F${optC}",
         "Before counting the ten month schedule difference, which on its own defeats the client's "
         "second quarter start.",M0),
        ("","","",None),
        ("Fugitive emissions","Excluded",
         "Surface coating manufacture is not a listed category under Regulation 5.02(c). Including the "
         "4.20 tpy of fugitives would push the recommended option back over the threshold, so this is "
         "not a presentational point.",None),
        ("The one-shift schedule","Cannot be credited",
         "Regulation 5.02(b) counts an operating limitation only if it is federally enforceable. No "
         "permit condition restricts hours. Potential to emit uses 8,760 hours.",None),
        ("The 2022 Line 1 shutdown","Not creditable",
         "Already relied upon in full in revision R-23-0412, and netting is unavailable in any event "
         "where a project makes a minor source major.",None),
        ("The Line 2 debottleneck","Must be permitted",
         "Completed August 2025 without an application, contrary to permit condition 7.2. It is "
         "aggregated with this project and should be resolved in the same application.",None),
        ("Hazardous air pollutants","Below thresholds",
         "Xylene is the closer of the two and should be re-checked on any formulation change.",None),
    ]:
        if lbl=="": r+=1; continue
        x=ws.cell(r,1,lbl); x.font=Font(bold=True,size=10.5,color=TEAL); x.alignment=Alignment(vertical="top")
        b=ws.cell(r,2,val); b.font=Font(bold=True,size=11); b.alignment=Alignment(vertical="top",horizontal="right",wrap_text=True)
        if fmt: b.number_format=fmt
        d=ws.cell(r,3,note); d.alignment=Alignment(wrap_text=True,vertical="top"); d.font=Font(size=9.5)
        ws.row_dimensions[r].height=max(16,12.4*(len(note)//92+1))
        r+=1
    wb.save(OUT); print("workbook written:",OUT)
    print("tabs:",[s.title for s in wb.worksheets])

FIRM_ = c.FIRM
if __name__=="__main__": build()
