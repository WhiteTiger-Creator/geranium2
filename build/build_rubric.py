import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cordell as c
OUT = "/home/azureuser/geranium_tasks/task2_env/RUBRIC.md"
o = c.option_costs(); enc = c.facility_pte_tpy(c.ENCLOSURE_CAPTURE)
C = [
("Rigid",5,f"Computes potential to emit on {c.PTE_DAYS_PER_YEAR} days, being 8,760 hours, and states that the plant's {c.CLIENT_STATED_DAYS} day schedule cannot be credited because Regulation 5.02(b) counts an operating limitation only where it is federally enforceable and no permit condition restricts hours. Using the stated schedule earns nothing."),
("Rigid",4,f"Uses the coating volatile organic compound content less water and exempt compounds of {c.COATING['voc_less_water_lb_gal']:.2f} lb/gal rather than the as-supplied value of {c.COATING['voc_as_supplied_lb_gal']:.2f} lb/gal, consistent with permit condition 3.2. Using the as-supplied value earns nothing."),
("Rigid",5,f"Calculates overall control as the product of capture and destruction, {c.RTO_CAPTURE_AS_DESIGNED:.0%} times {c.RTO_DESTRUCTION:.0%} giving about {c.overall_control(c.RTO_CAPTURE_AS_DESIGNED):.2%}, per Regulation 5.02(d). Crediting the destruction efficiency alone earns nothing."),
("Rigid",4,f"Reports Line 4 potential to emit of about {c.line4_pte_tpy():.2f} tons per year, being the controlled coating stream plus the uncontrolled cleanup solvent. A figure that omits the cleanup solvent or applies control to it earns nothing."),
("Rigid",4,f"Aggregates the August 2025 Line 2 debottleneck of {c.LINE2_DEBOTTLENECK['voc_tpy']:.2f} tons per year with this project under Regulation 5.03(b), notwithstanding that no permit was obtained for it. Treating Line 4 in isolation earns nothing."),
("Rigid",3,f"Reports a project emissions increase of about {c.project_increase_tpy():.2f} tons per year and notes that this is below the {c.SIGNIFICANT_VOC_TPY:.0f} ton significance threshold. Omitting the comparison, or reporting an increase that excludes the Line 2 change, earns nothing."),
("Rigid",5,f"Computes facility potential to emit after the project as about {c.facility_pte_tpy():.2f} tons per year against the {c.MAJOR_VOC_TPY:.0f} ton major source threshold, and concludes the facility becomes a major stationary source. Stopping at the significance test earns nothing."),
("Rigid",5,"States that because the project makes a minor source major, Regulation 5.04(b) requires it to be reviewed as a new major stationary source, that the emissions of the entire project are subject to review, and that netting is not available. Concluding that no review is triggered because the increase is below the significance threshold earns nothing."),
("Rigid",5,f"Excludes the {c.FUGITIVE_VOC_TPY:.2f} tons per year of fugitive emissions from the major source determination, because surface coating manufacture is not a listed category under Regulation 5.02(c), and notes that including them would push the recommended option back over the threshold. Including fugitives earns nothing."),
("Rigid",4,f"Concludes that the {abs(c.LINE1_SHUTDOWN['voc_tpy']):.0f} ton 2022 Line 1 shutdown is not creditable, on the grounds that it was relied upon in full in revision R-23-0412 and that netting is unavailable where a project makes a minor source major. Applying the credit earns nothing."),
("Rigid",3,f"Checks hazardous air pollutants and concludes the facility does not become major, with xylene at about {c.hap_after()['Xylene']:.2f} tons per year against the {c.HAP_SINGLE_TPY:.0f} ton single pollutant threshold and an aggregate below {c.HAP_AGGREGATE_TPY:.0f}. Omitting the hazardous air pollutant check earns nothing."),
("Rigid",2,f"Treats the cleanup solvent as uncontrolled, at about {c.cleanup_voc_tpy():.2f} tons per year, because it is not ducted to the oxidiser under either capture arrangement. Applying control to it earns nothing."),
("Rigid",5,f"Demonstrates that a permanent total enclosure raises overall control to about {c.overall_control(c.ENCLOSURE_CAPTURE):.0%} and brings facility potential to emit to roughly {enc:.2f} tons per year, below the major source threshold at full design throughput. An option analysis that does not compute the resulting facility total earns nothing."),
("Rigid",3,f"Quantifies the throughput cap alternative at roughly {c.capped_throughput_gal_day():.0f} gallons per day, about {c.capped_throughput_gal_day()/c.L4_DESIGN_GAL_DAY:.0%} of the design rate, and identifies that the limit must be federally enforceable to count. Presenting a cap without the resulting throughput earns nothing."),
("Rigid",3,f"Prices the major source route at about ${o['major']:,.0f}, including offsets of {o['offset_tons']:.2f} tons at the {c.OFFSET_RATIO:.2f} to one ratio costing about ${o['offsets']:,.0f}. Omitting offsets, or applying them without the ratio, earns nothing."),
("Rigid",3,f"Prices the enclosure route at about ${o['enclosure']:,.0f} and quantifies the difference against the major source route at roughly ${o['saving']:,.0f}. Comparing the options without a cost difference earns nothing."),
("Rigid",3,f"States the permitting duration for each route, {c.SCHEDULE_MONTHS['major source review'][0]} to {c.SCHEDULE_MONTHS['major source review'][1]} months for major source review against {c.SCHEDULE_MONTHS['minor revision'][0]} to {c.SCHEDULE_MONTHS['minor revision'][1]} for a minor revision, and relates it to the client's second quarter start. Omitting the schedule earns nothing."),
("Subjective",5,"Recommends the permanent total enclosure and supports it on both the threshold arithmetic and the permitting schedule, rather than on capital cost alone. Any recommendation that keeps the facility below the major source threshold at full throughput and is justified against cost and schedule together earns full credit; a recommendation with no supporting comparison earns nothing."),
("Subjective",4,"Corrects the client's stated premise that the project is acceptable because the increase is below forty tons per year, explaining that the significance threshold applies only at a source that is already major. Any explanation that distinguishes the modification test from the new major source test earns full credit."),
("Subjective",3,"Identifies the unpermitted August 2025 Line 2 change as a compliance matter in its own right, contrary to permit condition 7.2, and reaches a position on how it should be resolved. Either recommending it be regularised within this application or addressed separately earns full credit where the reasoning is given."),
("Subjective",2,f"Notes that the margin to the threshold under the recommended option is only a few tons per year and draws a consequence from it, such as verification of the enclosure or caution about future changes. Any handling that quantifies the headroom and states why it matters earns full credit."),
("Format",2,"Delivers a single file named Cordell_NSR_Analysis.xlsx, with that exact name and extension. Any other filename or extension, or a deliverable supplied as chat text rather than a file, earns nothing."),
("Format",2,"Builds the workbook on live formulas resolving back to the design data and the regulation thresholds, so the determination re-computes if a coating property or a control efficiency changes. A workbook of hard-coded results earns nothing."),
("Format",1,"Leads with a sheet carrying the applicability determination, the recommended route and its cost, so the answer is readable without working through the calculation sheets. Burying the determination among the calculations earns nothing."),
("Negative",-5,f"Concludes that major source review is not triggered because the project increase of about {c.project_increase_tpy():.0f} tons per year is below the significance threshold. Apply once wherever that conclusion is stated."),
("Negative",-5,f"Calculates potential to emit on the plant's {c.CLIENT_STATED_DAYS} day operating schedule rather than on 8,760 hours. Apply once wherever the restricted schedule is used."),
("Negative",-4,"Includes fugitive emissions in the major stationary source determination, when surface coating manufacture is not a listed category. Apply once."),
("Negative",-4,"Applies the 2022 Line 1 shutdown as a netting credit against this project. Apply once."),
("Negative",-4,"Credits the oxidiser destruction efficiency without applying capture efficiency, or uses the as-supplied coating volatile organic compound content instead of the less water value. Apply once for either error."),
("Negative",-3,"States a figure in one place that contradicts the same figure elsewhere in the workbook, for example a potential to emit, a cost total or a control efficiency that differs between the summary sheet and the calculation sheets. Apply once."),
]
pos=sum(w for k,w,_ in C if w>0); neg=sum(w for k,w,_ in C if w<0)
fn=sum(1 for k,w,_ in C if k=="Format"); fw=sum(w for k,w,_ in C if k=="Format")
over=[(i,len(t)) for i,(_,_,t) in enumerate(C,1) if len(t)>500]
L=["# Rubric - form-ready criteria","",f"**{len(C)} criteria.** Paste each string into its own Criterion field; the number goes in the Weight field only.","",
   f"Maximum positive reward {pos}. Negative criteria total {neg}.","",
   f"- Format criteria: {fn} of {len(C)} ({fn/len(C):.0%}), under the half limit",
   f"- Format weight: {fw} of {pos} ({fw/pos:.1%}), under the quarter limit",
   f"- Negative criteria: {sum(1 for k,w,_ in C if w<0)}, above the minimum of two",
   f"- Longest criterion: {max(len(t) for _,_,t in C)} characters","","---",""]
for i,(k,w,t) in enumerate(C,1):
    L+=[f"### Criterion {i}  ·  weight `{w}`  ·  _{k}_","",t,"",f"<sub>{len(t)} / 500 characters</sub>",""]
open(OUT,"w").write("\n".join(L)+"\n")
print(f"{len(C)} criteria | +{pos} / {neg} | format {fn} ({fn/len(C):.0%}), {fw/pos:.1%} of reward | longest {max(len(t) for _,_,t in C)} | over 500: {over or 'none'}")
