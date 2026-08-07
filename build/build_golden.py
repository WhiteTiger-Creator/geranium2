"""Build the golden solution: Fairlead_Phase_II_Evaluation_Memo.docx"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import site_data as s
import evaluate as e

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT = "/home/azureuser/geranium_tasks/task2_env/golden_solution/Fairlead_Phase_II_Evaluation_Memo.docx"
GREEN = RGBColor(0x1F, 0x4E, 0x3D)
MUTED = RGBColor(0x89, 0x87, 0x81)

ex = e.soil_exceedances()
real = [x for x in ex if x["kind"] not in ("background", "indeterminate")]
gwex = e.gw_exceedances()
vols = e.volumes()
CY = sum(r["cy"] for r in vols)
TONS = sum(r["tons"] for r in vols)
items, sub, cont, TOT = e.cost_estimate()
_, sub2, _, TOT_SSD = e.cost_estimate(include_ssd=True)
sc = e.schedule()

# alternatives -----------------------------------------------------------------
ALT1_CY = (2600 * 10 + 1200 * 10 + 400 * 10) / 27.0
ALT1 = ((e.unit("Mobilisation") + ALT1_CY * e.unit("Excavation")
         + ALT1_CY * s.SOIL_DENSITY * e.unit("Transport and disposal, non-haz")
         + ALT1_CY * e.unit("Certified") + 20 * e.unit("Confirmation")
         + 40000 + 78000 + 8 * e.unit("Quarterly")) * (1 + s.CONTINGENCY))
ALT3 = ((e.unit("Activity") + e.unit("Vapour") + s.MONITORING_ROUNDS * e.unit("Quarterly") + 18000)
        * (1 + s.CONTINGENCY))
HAZ_DELTA = TONS * (e.unit("Transport and disposal, RCRA") - e.unit("Transport and disposal, non-haz"))

dc_hits = sorted({(x["aoc"], x["analyte"]) for x in real if "direct contact" in x["kind"]})
areas = sorted({x["aoc"] for x in real})
analytes = sorted({x["analyte"] for x in real})


def maxconc(aoc, analyte):
    v = [x["value"] for x in real if x["aoc"] == aoc and x["analyte"] == analyte]
    return max(v) if v else None


def build():
    d = Document()
    st = d.styles["Normal"]; st.font.name, st.font.size = "Calibri", Pt(10)
    for sec in d.sections:
        sec.top_margin = sec.bottom_margin = Inches(0.65)
        sec.left_margin = sec.right_margin = Inches(0.75)
        fp = sec.footer.paragraphs[0]; fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pre = fp.add_run("Marchbank Environmental, Inc.  |  Project 26-0431  |  "
                         "Privileged and confidential - prepared at the direction of counsel  |  Page ")
        pre.font.size, pre.font.color.rgb = Pt(7.5), MUTED
        for instr in ("PAGE", "NUMPAGES"):
            run = fp.add_run(); run.font.size, run.font.color.rgb = Pt(7.5), MUTED
            fld = OxmlElement('w:fldSimple'); fld.set(qn('w:instr'), f' {instr} ')
            t = OxmlElement('w:t'); t.text = "1"; fld.append(t)
            run._r.addnext(fld)
            if instr == "PAGE":
                sep = fp.add_run(" of "); sep.font.size, sep.font.color.rgb = Pt(7.5), MUTED

    def H(text, size=11.5):
        p = d.add_paragraph(); p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(text); r.bold, r.font.size, r.font.color.rgb = True, Pt(size), GREEN

    def T(headers, rows, widths, size=8.5):
        t = d.add_table(rows=1, cols=len(headers)); t.style = "Light Grid Accent 3"
        for i, h in enumerate(headers):
            c = t.rows[0].cells[i]; c.text = ""
            r = c.paragraphs[0].add_run(h); r.bold, r.font.size = True, Pt(size)
        for row in rows:
            cells = t.add_row().cells
            for i, v in enumerate(row):
                cells[i].text = ""
                cells[i].paragraphs[0].add_run(str(v)).font.size = Pt(size)
        for i, w in enumerate(widths):
            for row in t.rows:
                row.cells[i].width = Inches(w)
        d.add_paragraph()
        return t

    p = d.add_paragraph(); r = p.add_run("MEMORANDUM")
    r.bold, r.font.size, r.font.color.rgb = True, Pt(15), GREEN
    t = d.add_table(rows=5, cols=2); t.style = "Table Grid"
    for i, (k, v) in enumerate([
        ("To", "Marisa Quintanilla, Kestrel Industrial Partners LLC; "
               "Ben Oyediran, Oyediran Vance LLP"),
        ("From", "Dee Ferraro, PG, Marchbank Environmental, Inc."),
        ("Date", "March 16, 2026"),
        ("Subject", f"Phase II ESA data evaluation, remedial cost estimate and recommendation - "
                    f"{s.SITE}, {s.CITY}"),
        ("Project", "26-0431"),
    ]):
        t.rows[i].cells[0].width = Inches(0.7); t.rows[i].cells[1].width = Inches(6.3)
        t.rows[i].cells[0].text = ""; t.rows[i].cells[0].paragraphs[0].add_run(k).bold = True
        t.rows[i].cells[1].text = v

    # 1 -------------------------------------------------------------------
    H("1.  Conclusions")
    d.add_paragraph(
        f"The property is impactable but closeable. Three of the four areas of concern carry soil "
        f"concentrations above the applicable criteria, groundwater beneath the east and north yards is "
        f"impacted by tetrachloroethene, and neither condition prevents the warehouse from being built. "
        f"What they do is cost money and consume time, and on the present schedule there is not enough "
        f"of the second to be certain about the first.")
    d.add_paragraph(
        f"Our recommended course is a targeted excavation of the three impacted areas above the water "
        f"table, an activity and use limitation restricting the property to commercial and industrial "
        f"use, a vapour intrusion evaluation before the slab is designed, and four quarters of "
        f"groundwater monitoring. We estimate that at ${TOT:,.0f} including a twenty percent "
        f"contingency, rising to ${TOT_SSD:,.0f} if the vapour evaluation shows that a sub-slab "
        f"depressurisation system is needed.")
    d.add_paragraph(
        f"Both figures exceed the ${s.ESCROW_CAP:,.0f} environmental escrow under Section 9.1. The "
        f"shortfall is ${TOT - s.ESCROW_CAP:,.0f} on the base case and ${TOT_SSD - s.ESCROW_CAP:,.0f} "
        f"if mitigation proves necessary, and under Section 9.1 that excess sits with Kestrel.")
    d.add_paragraph(
        f"Two things cannot be resolved inside the current due diligence period. Vinyl chloride was "
        f"reported as not detected in every soil sample, but at a reporting limit above the criterion "
        f"that applies to it, so those results do not demonstrate compliance. And the vapour intrusion "
        f"question has to be answered before the building is designed, not after. Together those need "
        f"about {sc['critical']} days from today against the {sc['available']} that remain. We "
        f"recommend exercising the Section 4.3 extension.")

    # 2 -------------------------------------------------------------------
    H("2.  Which criteria apply, and why")
    d.add_paragraph(
        "Choosing the criteria is the single decision that most affects the cost of this transaction, "
        "so we have set out the basis for each.")
    T(["Pathway", "Criteria applied", "Basis"], [
        ["Soil, direct contact", "Industrial and commercial",
         "Zoning is M-2 and residential occupancy is not a permitted use. Kestrel's use is a "
         "distribution warehouse. ODEQ permits the industrial column where an activity and use "
         "limitation is recorded, and Kestrel has confirmed it will accept one."],
        ["Soil, leaching", "Soil to groundwater",
         "Applied at every property irrespective of use classification, per Table 3-1. This pathway, "
         "not direct contact, drives most of the footprint here."],
        ["Groundwater", "GW-2 and GW-3; GW-1 not applied",
         "The surficial aquifer is mapped Class II-B, not a current or potential potable source. The "
         "property and its neighbours are on the Brayton municipal system and no private supply wells "
         "were identified within one mile. GW-2 applies because the planned building will sit over the "
         "impacted groundwater."],
    ], [1.3, 1.7, 4.0])
    d.add_paragraph(
        f"The distinction matters. Measured against GW-1, ten additional results across all three "
        f"downgradient wells would appear to exceed, including chromium and lead at TW-01 and the "
        f"full chlorinated ethene suite at TW-02 and TW-03. Applying GW-1 here would point toward "
        f"aquifer restoration, which is neither required nor useful at a property where nobody drinks "
        f"the groundwater. It would also, on our estimating basis, roughly double the cost.")

    # 3 -------------------------------------------------------------------
    H("3.  Data usability")
    d.add_paragraph(
        "Calderwood did not validate the data and four items in the case narrative bear on how the "
        "results should be read. Two of them remove apparent exceedances; one of them removes our "
        "ability to draw a conclusion at all.")
    mc = [(sid, s.soil_result(sid, b, top, "Methylene chloride")[0])
          for sid, b, aoc, top, bot in s.soil_samples()
          if not s.soil_result(sid, b, top, "Methylene chloride")[1]]
    T(["Finding", "Effect on the conclusions"], [
        ["Methylene chloride in the soil volatile method blank at "
         f"{s.METHOD_BLANK['Methylene chloride']:g} ug/kg",
         f"Methylene chloride was detected in {len(mc)} samples between "
         f"{min(v for _, v in mc):,.0f} and {max(v for _, v in mc):,.0f} ug/kg. Every detection is "
         f"below five times the blank concentration, the conventional threshold for a common "
         f"laboratory contaminant, and all are qualified as not detected. Taken at face value they "
         f"would each have exceeded the "
         f"{s.SOIL_SL['Methylene chloride'][2]*1000:,.0f} ug/kg leaching criterion and would have "
         f"added a fourth constituent to the remedy across both buildings. They are laboratory "
         f"artefact, not site condition."],
        [f"Vinyl chloride reporting limit of {s.SOIL_RL['Vinyl chloride']:g} ug/kg",
         f"That limit is {s.SOIL_RL['Vinyl chloride']/1000:g} mg/kg. The soil to groundwater criterion "
         f"is {s.SOIL_SL['Vinyl chloride'][2]:g} mg/kg. A non-detect at a limit above the criterion "
         f"does not demonstrate compliance, and ODEQ says so expressly in the application notes. Vinyl "
         f"chloride is the terminal daughter product of the tetrachloroethene degradation we can see in "
         f"groundwater, so this is not a theoretical gap. Selected ion monitoring reaches roughly "
         f"2 ug/kg on ten business days' turnaround and should be run on the AOC-2 and AOC-3 samples."],
        ["TW-03 volatile aliquot analysed seventeen days after collection",
         "Three days beyond holding time. Detected results carry a J qualifier and are biased low. "
         "TW-03 still exceeds the GW-2 criterion for tetrachloroethene as reported, so the exceedance "
         "stands, but the magnitude is understated and TW-03 cannot be used to bound the plume. "
         "Re-collect at the first monitoring round."],
        ["Field duplicate FD-01, lead",
         f"Relative percent difference of "
         f"{s.rpd(s.SOIL_HITS[(s.FIELD_DUP[0], s.FIELD_DUP[1])]['Lead'], s.FIELD_DUP[3]['Lead']):.0f} "
         f"percent against a thirty percent limit, with laboratory control recoveries in range. This is "
         f"fill heterogeneity rather than laboratory performance. It does not change any conclusion, "
         f"because both the parent and the duplicate exceed the same criteria, but it means single "
         f"lead results should not be used to draw a tight excavation boundary. We have allowed for "
         f"that in the confirmation sampling."],
    ], [2.4, 4.6])

    # 4 -------------------------------------------------------------------
    H("4.  What exceeds, and where")
    d.add_paragraph(
        f"After the qualifications above, {len(real)} soil results exceed an applicable criterion. They "
        f"involve {len(analytes)} constituents and fall entirely within AOC-1, AOC-2 and AOC-3. "
        f"Maximum concentrations by area are below; the full screening table is attached.")
    rows = []
    for aoc in areas:
        for a in analytes:
            mx = maxconc(aoc, a)
            if mx is None:
                continue
            dc, s2g = e.soil_criteria(a)
            paths = []
            if mx > dc:
                paths.append("direct contact")
            if mx > s2g:
                paths.append("leaching")
            rows.append([aoc, a, f"{mx:,.3g}", f"{dc:g}", f"{s2g:g}", " and ".join(paths)])
    T(["Area", "Constituent", "Max (mg/kg)", "Industrial DC", "Soil to GW", "Pathway exceeded"],
      rows, [0.7, 1.7, 1.0, 1.0, 1.0, 1.6])
    d.add_paragraph(
        f"Two observations. First, the leaching pathway drives this site: only "
        f"{len(dc_hits)} area and constituent combinations exceed the industrial direct contact "
        f"levels, while every listed constituent exceeds its soil to groundwater level. Second, "
        f"AOC-4 is clean. Neither boring in the former tank basin found anything above criteria, which "
        f"is worth noting because AOC-4 is the one area the indemnity does not cover.")
    d.add_paragraph(
        "In groundwater, tetrachloroethene exceeds the GW-2 vapour criterion at TW-02 and TW-03. "
        "Nothing else exceeds an applicable criterion in any well.")
    T(["Well", "Constituent", "Result (ug/L)", "GW-2 (ug/L)", "Note"],
      [[g["well"], g["analyte"], f"{g['value']:,.0f}", f"{g['crit']:g}",
        "Estimated, holding time exceedance" if g["qual"] else ""] for g in gwex],
      [0.8, 1.7, 1.3, 1.2, 2.0])
    d.add_paragraph(
        "Because the planned warehouse footprint covers the east yard and part of the north yard, both "
        "of these sit directly beneath the building. That is what triggers the vapour intrusion work.")

    # 5 -------------------------------------------------------------------
    H("5.  Conditions we have set aside")
    for t_, b_ in [
        ("Arsenic",
         f"Arsenic was detected in every soil sample between roughly 5 and 17 mg/kg. The highest "
         f"results are at SB-12, the upgradient reference location, where "
         f"{maxconc('BKG','Arsenic') or 16.6:.1f} mg/kg exceeds the "
         f"{s.SOIL_SL['Arsenic'][2]:g} mg/kg leaching criterion. The ODEQ Brayton Lowland background "
         f"study reports arsenic in native soils from {s.ARSENIC_BACKGROUND[0]:g} to "
         f"{s.ARSENIC_BACKGROUND[1]:g} mg/kg. Every result on this property falls inside that range, "
         f"including the ones at the source areas, and the highest is at the location furthest from "
         f"any of them. This is the parent material, not a release, and ODEQ's guidance says so "
         f"expressly. No action."),
        ("Groundwater metals and the remaining volatiles",
         "Chromium and lead at TW-01 and the trichloroethene, dichloroethene and vinyl chloride "
         "results at TW-02 and TW-03 are all below the applicable GW-2 and GW-3 criteria. They exceed "
         "GW-1, which does not apply here. We would expect a reviewer to ask about them and have "
         "listed them in the attached table for that reason."),
        ("Methylene chloride",
         "Set aside as laboratory blank contamination, as described in section 3."),
    ]:
        p = d.add_paragraph(); p.add_run(f"{t_}. ").bold = True; p.add_run(b_)

    # 6 -------------------------------------------------------------------
    H("6.  Remedial approach")
    d.add_paragraph(
        "We considered three approaches. The first is not achievable, the third is not protective, and "
        "the second is what we recommend.")
    T(["Approach", "Estimated cost", "Assessment"], [
        ["Unrestricted closure: excavate to residential criteria and restore groundwater",
         f"${ALT1:,.0f} plus groundwater remediation",
         "Not achievable at any cost we could defend. Tetrachloroethene persists in soil below the "
         "water table at AOC-2 and AOC-3 and cannot be removed by excavation, and the groundwater "
         "exceedance would remain. The cost shown is for the soil component alone and buys an outcome "
         "the site cannot reach."],
        ["Targeted excavation above the water table, activity and use limitation, vapour intrusion "
         "evaluation and four quarters of monitoring",
         f"${TOT:,.0f}",
         "Recommended. Removes the direct contact exceedances and the great majority of the leaching "
         "mass, manages the residual through the deed restriction, and answers the vapour question "
         "before the slab is designed."],
        ["Activity and use limitation and monitoring only, no excavation",
         f"${ALT3:,.0f}",
         "Not protective. Lead, cadmium, chromium and tetrachloroethene exceed the industrial direct "
         "contact levels in shallow soil at four locations. A use limitation does not manage the "
         "construction worker receptor during the warehouse build, and ODEQ does not permit area "
         "averaging for that receptor."],
    ], [2.1, 1.3, 3.6])
    d.add_paragraph(
        "The excavation is limited to 8 feet below grade at AOC-1 and AOC-2 and 10 feet at AOC-3. "
        "Water is first encountered between 9.9 and 10.8 feet. Excavating into the water table would "
        "require sheeting and a much larger dewatering and treatment effort for a marginal reduction in "
        "residual mass, and the residual is manageable through the use limitation and monitoring.")
    T(["Area", "Footprint", "Interval", "Thickness", "In-situ volume", "Tonnage"],
      [[r["aoc"], f"{r['area']:,} sq ft", f"{r['top']}-{r['bot']} ft", f"{r['thickness']} ft",
        f"{r['cy']:,.0f} cy", f"{r['tons']:,.0f} tons"] for r in vols] +
      [["Total", "", "", "", f"{CY:,.0f} cy", f"{TONS:,.0f} tons"]],
      [0.8, 1.2, 1.1, 1.0, 1.4, 1.4])

    # 7 -------------------------------------------------------------------
    H("7.  Cost estimate")
    d.add_paragraph(
        f"Built from the unit rates in our estimating basis, which carry a stated accuracy of minus "
        f"fifteen to plus thirty percent before contingency.")
    T(["Item", "Quantity", "Amount"],
      [[n, q, f"${a:,.0f}"] for n, q, r_, a in items] +
      [["Subtotal", "", f"${sub:,.0f}"],
       [f"Contingency at {s.CONTINGENCY:.0%}", "", f"${cont:,.0f}"],
       ["Total, recommended approach", "", f"${TOT:,.0f}"],
       ["Total if sub-slab depressurisation proves necessary", "", f"${TOT_SSD:,.0f}"]],
      [4.2, 1.3, 1.5])
    d.add_paragraph(
        f"One line deserves comment. The soil profiles as non-hazardous. Toxicity characteristic "
        f"leaching results for the two highest total lead samples were "
        f"{min(s.TCLP.values()):g} and {max(s.TCLP.values()):g} mg/L against the "
        f"{s.TCLP_LIMIT:g} mg/L regulatory limit, so the material goes to Ridgeline at "
        f"${e.unit('Transport and disposal, non-haz'):,.2f} per ton rather than to Tallmadge at "
        f"${e.unit('Transport and disposal, RCRA'):,.2f}. On {TONS:,.0f} tons that distinction is "
        f"worth ${HAZ_DELTA:,.0f}. An estimate that assumed hazardous disposal on the strength of the "
        f"total lead concentrations alone would be wrong by more than the entire escrow.")

    # 8 -------------------------------------------------------------------
    H("8.  How this sits against the agreement")
    d.add_paragraph(
        f"Section 9.1 caps Seller's contribution at ${s.ESCROW_CAP:,.0f} and puts everything above it "
        f"on Kestrel. The recommended approach exceeds the cap by ${TOT - s.ESCROW_CAP:,.0f}, and by "
        f"${TOT_SSD - s.ESCROW_CAP:,.0f} if vapour mitigation is required. That gap is the number to "
        f"negotiate, either as an increase to the escrow or as a reduction in the purchase price.")
    d.add_paragraph(
        "Section 9.4 is the more awkward provision. Our recommended approach depends on recording an "
        "activity and use limitation, and Kestrel cannot record one without Seller's written consent. "
        "Seller is keeping the adjoining parcel, which gives it a reason to resist a restriction "
        "recorded next door. Consent cannot be unreasonably withheld, but Kestrel should not rely on "
        "that in a transaction with this timetable. We would ask for the consent in writing as a "
        "condition of closing, and Ben should know that the alternative if consent is refused is the "
        f"unrestricted approach in section 6, which is not achievable here at any price. In practical "
        f"terms, refusal of consent is a reason to walk rather than a reason to spend more.")
    d.add_paragraph(
        "Section 9.2 excludes Known Conditions from the indemnity, which takes AOC-4 outside Seller's "
        "cover because the former tank and the 1998 closure file are both described in the Phase I. As "
        "it happens neither boring in the tank basin found anything above criteria, so on present "
        "information that carve-out costs Kestrel nothing. The caution is that the ODEQ closure file "
        "records soil left in place above current criteria, and two borings do not disprove that. If "
        "material turns up during construction it will be Kestrel's, not Seller's. We would allow for "
        "that in the construction budget rather than in this estimate.")

    # 9 -------------------------------------------------------------------
    H("9.  What is still unknown, and the schedule")
    T(["Gap", "Work required", "Duration"], [
        ["Vinyl chloride cannot be screened at the reporting limit achieved",
         "Re-analyse the AOC-2 and AOC-3 archived samples by selected ion monitoring",
         f"{sc['reanalysis']} days"],
        ["Vapour intrusion beneath the planned building is unquantified",
         "Sub-slab and indoor air sampling, two rounds, plus laboratory turnaround",
         f"{sc['vi']} days"],
        ["The plume is not bounded east of TW-02 and TW-03 is biased low",
         "Two additional temporary wells, and re-collect TW-03",
         "Concurrent with the above"],
        ["Residual at the former tank basin is not disproved",
         "Two additional borings in the 1998 excavation footprint",
         "Concurrent with the above"],
        ["Evaluation and reporting", "", f"{s.EVALUATION_AND_REPORTING_DAYS} days"],
    ], [2.4, 3.3, 1.3])
    d.add_paragraph(
        f"The critical path is {sc['critical']} days from today, finishing about "
        f"{sc['finish'].strftime('%B %d, %Y')}. The due diligence period expires "
        f"{s.DD_EXPIRY.strftime('%B %d, %Y')}, which is {sc['available']} days away. We are "
        f"{sc['shortfall']} days short.")
    d.add_paragraph(
        "Section 4.3 allows Kestrel to extend by up to sixty days on written notice with an additional "
        "deposit of $75,000, and does not require Seller's consent. That is the clean answer. The "
        "deposit becomes non-refundable but is credited at closing, so the real cost of the extension "
        "is the risk that Kestrel later walks, against the risk of closing without knowing whether the "
        "building needs a depressurisation system underneath it.")

    # 10 ------------------------------------------------------------------
    H("10.  Recommendation")
    for x in [
        f"Serve notice under Section 4.3 before March 31 and extend the due diligence period. Sixty "
        f"days covers the {sc['critical']}-day critical path with margin.",
        "Commission the vinyl chloride re-analysis, the vapour intrusion round, two step-out wells and "
        "two borings in the former tank basin immediately, without waiting for the extension to be "
        "acknowledged.",
        f"Open the negotiation on the escrow now. The gap is ${TOT - s.ESCROW_CAP:,.0f} on the base "
        f"case and ${TOT_SSD - s.ESCROW_CAP:,.0f} if mitigation is needed; we would ask for the higher "
        f"figure and settle at the lower.",
        "Obtain Seller's written consent to an activity and use limitation as a condition of closing. "
        "Without it the recommended approach does not work and there is no viable substitute.",
        "Budget separately for the possibility of undocumented residual at the former tank basin, "
        "which sits outside the indemnity.",
    ]:
        d.add_paragraph(x, style="List Number")
    d.add_paragraph(
        "We are not recommending that Kestrel walk. The impacts are ordinary for a former plating and "
        "degreasing plant, they are bounded on three sides, and the remedy is conventional. The issue "
        "is that the agreement as drafted allocates a predictable cost overrun to the buyer and gives "
        "the seller a veto over the mechanism that makes the remedy affordable. Both are negotiable, "
        "and both are easier to negotiate before March 31 than after.")
    d.save(OUT)
    print("memo written:", OUT)


if __name__ == "__main__":
    build()
