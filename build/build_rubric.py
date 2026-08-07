"""Generate RUBRIC.md: form-ready criteria, each self-contained and under 500 characters."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import site_data as s
import evaluate as e

OUT = "/home/azureuser/geranium_tasks/task2_env/RUBRIC.md"

ex = e.soil_exceedances()
real = [x for x in ex if x["kind"] not in ("background", "indeterminate")]
gwex = e.gw_exceedances()
V = e.volumes()
CY = sum(r["cy"] for r in V)
TONS = sum(r["tons"] for r in V)
items, sub, cont, TOT = e.cost_estimate()
_, _, _, TOT2 = e.cost_estimate(include_ssd=True)
sc = e.schedule()
HAZ = TONS * (e.unit("Transport and disposal, RCRA") - e.unit("Transport and disposal, non-haz"))
mc = [s.soil_result(sid, b, top, "Methylene chloride")[0]
      for sid, b, aoc, top, bot in s.soil_samples()
      if not s.soil_result(sid, b, top, "Methylene chloride")[1]]
LEAD_RPD = s.rpd(s.SOIL_HITS[(s.FIELD_DUP[0], s.FIELD_DUP[1])]["Lead"], s.FIELD_DUP[3]["Lead"])
PCE_MAX_GW = max(g["value"] for g in gwex)

C = [
("Rigid", 4, f"Applies the industrial and commercial soil direct contact criteria rather than the residential column, and grounds that on the M-2 zoning, the planned distribution warehouse use and the client's acceptance of an activity and use limitation. Applying residential criteria throughout, or switching columns without stating a basis, earns nothing."),
("Rigid", 3, "Applies the soil to groundwater criteria to every area irrespective of land use classification, and identifies the leaching pathway rather than direct contact as the driver of most of the remedial footprint. Screening soil against direct contact criteria only earns nothing."),
("Rigid", 5, "Excludes the GW-1 potable supply criteria and screens groundwater against GW-2, on the basis that the surficial aquifer is mapped Class II-B, the property is on municipal water and no private supply wells were found within one mile. Screening groundwater against GW-1 earns nothing."),
("Rigid", 4, "Converts the laboratory's soil volatile results from ug/kg to mg/kg before comparing them to the screening table, which publishes soil criteria in mg/kg. Comparing ug/kg results directly against mg/kg criteria, which inflates every volatile result by a factor of one thousand, earns nothing."),
("Rigid", 4, f"Qualifies the methylene chloride soil detections as not detected because each falls below five times the {s.METHOD_BLANK['Methylene chloride']:g} ug/kg method blank result, and therefore excludes methylene chloride from the constituents of concern. Carrying the detections forward as site impact earns nothing."),
("Rigid", 5, f"Identifies that vinyl chloride was reported not detected at a soil reporting limit of {s.SOIL_RL['Vinyl chloride']:g} ug/kg, equal to {s.SOIL_RL['Vinyl chloride']/1000:g} mg/kg, which is above the {s.SOIL_SL['Vinyl chloride'][2]:g} mg/kg leaching criterion, so the results do not demonstrate compliance and re-analysis at a lower limit is required. Concluding that vinyl chloride is absent earns nothing."),
("Rigid", 3, "Identifies that the TW-03 volatile aliquot was analysed beyond the holding time, that its detected results are estimated and biased low, and that TW-03 therefore cannot be used to bound the extent of the plume even though its exceedance stands. Ignoring the holding time exceedance earns nothing."),
("Rigid", 2, f"Reports the relative percent difference between field duplicate FD-01 and its parent for lead as approximately {LEAD_RPD:.0f} percent, above the thirty percent limit, and attributes it to fill heterogeneity rather than laboratory performance. Treating the duplicate pair as acceptable, or as evidence of a laboratory problem, earns nothing."),
("Rigid", 3, f"Sets arsenic aside as naturally occurring because every result falls within the {s.ARSENIC_BACKGROUND[0]:g} to {s.ARSENIC_BACKGROUND[1]:g} mg/kg regional background range, noting that the highest concentration is at the upgradient reference boring. Carrying arsenic forward as a constituent of concern requiring remediation earns nothing."),
("Rigid", 3, "Reports that the soil exceedances are confined to AOC-1, AOC-2 and AOC-3, and that neither boring in the AOC-4 former tank basin exceeded an applicable criterion. Reporting exceedances in all four areas, or omitting the AOC-4 finding, earns nothing."),
("Rigid", 4, f"Reports that tetrachloroethene is the only groundwater constituent exceeding an applicable criterion, at TW-02 and TW-03, against the GW-2 value of {s.GW_SL['Tetrachloroethene'][1]:g} ug/L, with a maximum of about {PCE_MAX_GW:,.0f} ug/L. Listing metals or other volatiles as groundwater exceedances earns nothing."),
("Rigid", 4, f"Uses the non-hazardous disposal rate because both toxicity characteristic leaching results for lead, {min(s.TCLP.values()):g} and {max(s.TCLP.values()):g} mg/L, are below the {s.TCLP_LIMIT:g} mg/L regulatory limit. Applying the hazardous rate on the strength of total lead concentrations, an error worth roughly ${HAZ:,.0f}, earns nothing."),
("Rigid", 4, f"Estimates an in-situ excavation volume of roughly {CY:,.0f} cubic yards and about {TONS:,.0f} tons, built from the measured feature footprints and the depth intervals that exceed criteria, and limits the excavation to above the water table. A volume derived without reference to the measured footprints or the exceedance depths earns nothing."),
("Rigid", 5, f"Produces a remedial cost estimate of approximately ${TOT:,.0f} including the twenty percent contingency, built line by line from the unit rates in the estimating basis. An estimate that does not use those unit rates, or that omits the contingency, earns nothing."),
("Rigid", 4, f"States that the recommended remedy exceeds the ${s.ESCROW_CAP:,.0f} environmental escrow by roughly ${TOT - s.ESCROW_CAP:,.0f}, and that under Section 9.1 the excess falls on the buyer. Reporting a cost without comparing it to the escrow cap earns nothing."),
("Rigid", 4, f"Quantifies the schedule as approximately {sc['critical']} days of critical path against the {sc['available']} days remaining in the due diligence period, a shortfall of about {sc['shortfall']} days. Stating that more time is needed without quantifying it in days earns nothing."),
("Rigid", 3, "Identifies Section 4.3 as the mechanism to resolve the schedule, noting the sixty day maximum, the $75,000 additional deposit credited at closing, and that seller consent is not required. Recommending renegotiation of the closing date without reference to the extension right earns nothing."),
("Rigid", 3, f"Reports the contingent cost of about ${TOT2:,.0f} should the vapour intrusion evaluation show that a sub-slab depressurisation system is required, and presents it separately from the base estimate. Folding the mitigation cost into the base estimate, or omitting it, earns nothing."),
("Subjective", 5, "Recommends a risk-based approach built on targeted excavation, an activity and use limitation, vapour intrusion evaluation and monitoring, and rejects unrestricted closure on the grounds that residual impact below the water table and the groundwater exceedance make it unachievable rather than merely expensive. A recommendation supported by that feasibility reasoning earns full credit whatever the precise excavation limits chosen."),
("Subjective", 4, "Identifies that Section 9.4 makes the activity and use limitation subject to seller consent, that seller is retaining the adjoining parcel and so has a reason to resist, and that the recommended remedy therefore is not within the buyer's unilateral control. Any handling that names the dependency and states what happens if consent is refused earns full credit."),
("Subjective", 3, "Reaches a supported position on the Known Conditions carve-out in Section 9.2, recognising that the former tank and its agency closure file are described in the Phase I so AOC-4 sits outside the indemnity, while noting that the two borings there found no exceedance. Either concluding the carve-out has no present cost or treating it as a budgeted construction risk earns full credit if the reasoning is given."),
("Subjective", 4, "Concludes that a vapour intrusion evaluation is required, reasoning from the GW-2 exceedance beneath the planned warehouse footprint rather than from a general precaution, and places it before slab design in the sequence. Any conclusion that connects the groundwater result to the planned building and to the design schedule earns full credit."),
("Subjective", 3, "Sets out the remaining data gaps with a duration attached to each, covering at least the vinyl chloride re-analysis and the vapour intrusion round. The specific gaps chosen may vary, but each must carry a stated number of days and the durations must roll up to the critical path figure used elsewhere in the deliverable."),
("Format", 2, "Delivers a single file named Fairlead_Phase_II_Evaluation_Memo.docx, with that exact name and extension. Any other filename or extension, or a deliverable supplied as chat text rather than a file, earns nothing."),
("Format", 1, "Presents the work as a memorandum addressed to the client that carries the conclusions, the screening results and the recommendation in the body, so it can be read without reference to an appendix or a separate data package. A bare data dump or an unstructured narrative earns nothing."),
("Negative", -5, "Screens groundwater against the GW-1 potable supply criteria, which produces around ten additional apparent exceedances across all three downgradient wells and points toward aquifer restoration that is neither required nor useful at this property. Apply once wherever GW-1 is used as the compliance standard."),
("Negative", -5, "Compares soil volatile results reported in ug/kg directly against screening criteria published in mg/kg, overstating every volatile concentration by a factor of one thousand. Apply once wherever the unconverted comparison appears."),
("Negative", -4, "Carries the methylene chloride detections forward as site impact and includes them in the constituents of concern or the remedial footprint, when they are attributable to the laboratory method blank. Apply once."),
("Negative", -4, f"Applies the RCRA hazardous disposal rate of ${e.unit('Transport and disposal, RCRA'):,.2f} per ton when the toxicity characteristic leaching results demonstrate the soil is non-hazardous. Apply once wherever hazardous disposal is assumed in the cost estimate."),
("Negative", -4, "Concludes that vinyl chloride is absent or not a concern on the strength of non-detect results, without recognising that the reporting limit achieved is above the applicable criterion. Apply once."),
("Negative", -3, "States a figure in one section that contradicts the same figure elsewhere in the deliverable, for example an excavation volume, a cost total or a number of days that differs between the summary and the supporting tables. Apply once."),
]

pos = sum(w for k, w, _ in C if w > 0)
neg = sum(w for k, w, _ in C if w < 0)
fn = sum(1 for k, w, _ in C if k == "Format")
fw = sum(w for k, w, _ in C if k == "Format")
over = [(i, len(t)) for i, (_, _, t) in enumerate(C, 1) if len(t) > 500]

L = ["# Rubric - form-ready criteria", "",
     f"**{len(C)} criteria.** Paste each string into its own Criterion field; the number goes in the "
     f"Weight field only.", "",
     f"Maximum positive reward {pos}. Negative criteria total {neg}.", "",
     f"- Format criteria: {fn} of {len(C)} ({fn/len(C):.0%}), under the half limit",
     f"- Format weight: {fw} of {pos} ({fw/pos:.1%}), under the quarter limit",
     f"- Negative criteria: {sum(1 for k,w,_ in C if w<0)}, above the minimum of two",
     f"- Longest criterion: {max(len(t) for _,_,t in C)} characters", "", "---", ""]
for i, (kind, w, text) in enumerate(C, 1):
    L += [f"### Criterion {i}  ·  weight `{w}`  ·  _{kind}_", "", text, "",
          f"<sub>{len(text)} / 500 characters</sub>", ""]
open(OUT, "w").write("\n".join(L) + "\n")
print(f"{len(C)} criteria | +{pos} / {neg} | format {fn} crit ({fn/len(C):.0%}), {fw/pos:.1%} of reward "
      f"| longest {max(len(t) for _,_,t in C)} | over 500: {over or 'none'}")
