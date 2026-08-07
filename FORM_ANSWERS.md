# Submission form - field by field

Task 2. Nothing here contains the project code name.

---

## Section 1

### User Prompt  (2459 / 3000 characters)

```
I run the site assessment group at Marchbank Environmental, a 30-person environmental consulting firm in Brayton. Most of what we do is transaction support: Phase I and Phase II work for buyers who are already under contract and running out of clock.

Kestrel Industrial Partners is buying a 6.2-acre former metal finishing plant on Fairlead Street and intends to demolish the building and put up a distribution warehouse. We finished the Phase II field work in late February and the last of the laboratory data came in on Friday. Their due diligence period expires March 31, so they need our conclusions in time to decide whether to close, renegotiate or walk away. My assignment note is 01_PM_Assignment_Note.docx and it sets out what their acquisitions lead and their outside counsel each need from us.

The analytical data are in 02_Soil_Analytical_Results.xlsx and 03_Groundwater_Analytical_Results.xlsx. Field records, the sample cross-references and the measured dimensions of each site feature are in 04_Field_Records_and_Site_Features.xlsx. Read 05_Laboratory_Case_Narrative.docx before you screen anything against anything, because Calderwood does not validate data and there are items in there that change what some of the results mean.

Screening levels and the agency's application notes are in 06_ODEQ_Screening_Levels.xlsx. Do not simply reach for the most conservative column. Which criteria apply here is a judgment you have to make and defend, and the facts that decide it are in 07_Phase_I_Findings_Summary.docx rather than in the screening table itself.

Build the remedial cost from the unit rates in 08_Remedial_Cost_Basis.xlsx rather than from experience, and read 09_PSA_Environmental_Provisions.docx before you write the recommendation. Two clauses in there constrain what we are able to propose, and one of them our client cannot satisfy on its own.

Give it back as a single memorandum named Fairlead_Phase_II_Evaluation_Memo.docx, written to the client over my signature. It needs to cover which constituents exceed which criteria and where, what the data will and will not support, what the remedy is and what it costs, how that cost sits against the escrow, and what is still unknown. Attach money to the recommendation and put a number of days against anything you say we still need to do. Marisa can follow a screening table but she will not read an appendix, and "a few weeks" is not an answer she can take into a negotiation.
```

### O*NET Occupation

`Environmental Scientists and Specialists, Including Health` - 19-2041.00

### O*NET Tasks (select these four, verbatim)

- Collect, synthesize, analyze, manage, and report environmental data, such as pollution emission measurements, atmospheric monitoring measurements, meteorological or mineralogical information, or soil or water samples.
- Analyze data to determine validity, quality, and scientific significance and to interpret correlations between human activities and environmental effects.
- Review and implement environmental technical standards, guidelines, policies, and formal regulations that meet all appropriate requirements.
- Communicate scientific or technical information to the public, organizations, or internal audiences through oral briefings, written documents, workshops, conferences, training sessions, or public hearings.

### O*NET Skills (from Skills, not Technology Skills)

- Reading Comprehension
- Science
- Critical Thinking
- Mathematics
- Writing

### Input File Uploader

Upload `fairlead_input_files.zip` - 9 files, flat, no subfolders.

### How many input files are tied to your prompt?

**9**

### Are the input files multi-modal?

**No.** All nine are .docx or .xlsx. No images, audio, video, PDF or PPTX.

### Is web search allowed in your prompt?

**No.** Self-contained. Screening levels, background ranges, unit costs and contract terms are all supplied.

### Manual completion time

**8 hours**

---

## Section 2

### Golden Solution File Uploader

Upload `fairlead_golden_solution.zip` - one file, `Fairlead_Phase_II_Evaluation_Memo.docx`.

### What LLM did you use as a starting point?

Answer honestly for your own workflow.

### Rubric - 31 criteria

Max positive reward **89**; negatives total **-25**. Format is 2 of 31 criteria (6%) and 3.4% of reward. 6 negative criteria. Longest 433 chars.

| # | Weight | Criterion |
|---|---|---|
| 1 | `4` | Applies the industrial and commercial soil direct contact criteria rather than the residential column, and grounds that on the M-2 zoning, the planned distribution warehouse use and the client's acceptance of an activity and use limitation. Applying residential criteria throughout, or switching columns without stating a basis, earns nothing. |
| 2 | `3` | Applies the soil to groundwater criteria to every area irrespective of land use classification, and identifies the leaching pathway rather than direct contact as the driver of most of the remedial footprint. Screening soil against direct contact criteria only earns nothing. |
| 3 | `5` | Excludes the GW-1 potable supply criteria and screens groundwater against GW-2, on the basis that the surficial aquifer is mapped Class II-B, the property is on municipal water and no private supply wells were found within one mile. Screening groundwater against GW-1 earns nothing. |
| 4 | `4` | Converts the laboratory's soil volatile results from ug/kg to mg/kg before comparing them to the screening table, which publishes soil criteria in mg/kg. Comparing ug/kg results directly against mg/kg criteria, which inflates every volatile result by a factor of one thousand, earns nothing. |
| 5 | `4` | Qualifies the methylene chloride soil detections as not detected because each falls below five times the 620 ug/kg method blank result, and therefore excludes methylene chloride from the constituents of concern. Carrying the detections forward as site impact earns nothing. |
| 6 | `5` | Identifies that vinyl chloride was reported not detected at a soil reporting limit of 50 ug/kg, equal to 0.05 mg/kg, which is above the 0.02 mg/kg leaching criterion, so the results do not demonstrate compliance and re-analysis at a lower limit is required. Concluding that vinyl chloride is absent earns nothing. |
| 7 | `3` | Identifies that the TW-03 volatile aliquot was analysed beyond the holding time, that its detected results are estimated and biased low, and that TW-03 therefore cannot be used to bound the extent of the plume even though its exceedance stands. Ignoring the holding time exceedance earns nothing. |
| 8 | `2` | Reports the relative percent difference between field duplicate FD-01 and its parent for lead as approximately 78 percent, above the thirty percent limit, and attributes it to fill heterogeneity rather than laboratory performance. Treating the duplicate pair as acceptable, or as evidence of a laboratory problem, earns nothing. |
| 9 | `3` | Sets arsenic aside as naturally occurring because every result falls within the 4 to 22 mg/kg regional background range, noting that the highest concentration is at the upgradient reference boring. Carrying arsenic forward as a constituent of concern requiring remediation earns nothing. |
| 10 | `3` | Reports that the soil exceedances are confined to AOC-1, AOC-2 and AOC-3, and that neither boring in the AOC-4 former tank basin exceeded an applicable criterion. Reporting exceedances in all four areas, or omitting the AOC-4 finding, earns nothing. |
| 11 | `4` | Reports that tetrachloroethene is the only groundwater constituent exceeding an applicable criterion, at TW-02 and TW-03, against the GW-2 value of 300 ug/L, with a maximum of about 1,230 ug/L. Listing metals or other volatiles as groundwater exceedances earns nothing. |
| 12 | `4` | Uses the non-hazardous disposal rate because both toxicity characteristic leaching results for lead, 1.8 and 3.1 mg/L, are below the 5 mg/L regulatory limit. Applying the hazardous rate on the strength of total lead concentrations, an error worth roughly $334,950, earns nothing. |
| 13 | `4` | Estimates an in-situ excavation volume of roughly 933 cubic yards and about 1,353 tons, built from the measured feature footprints and the depth intervals that exceed criteria, and limits the excavation to above the water table. A volume derived without reference to the measured footprints or the exceedance depths earns nothing. |
| 14 | `5` | Produces a remedial cost estimate of approximately $403,820 including the twenty percent contingency, built line by line from the unit rates in the estimating basis. An estimate that does not use those unit rates, or that omits the contingency, earns nothing. |
| 15 | `4` | States that the recommended remedy exceeds the $350,000 environmental escrow by roughly $53,820, and that under Section 9.1 the excess falls on the buyer. Reporting a cost without comparing it to the escrow cap earns nothing. |
| 16 | `4` | Quantifies the schedule as approximately 34 days of critical path against the 22 days remaining in the due diligence period, a shortfall of about 12 days. Stating that more time is needed without quantifying it in days earns nothing. |
| 17 | `3` | Identifies Section 4.3 as the mechanism to resolve the schedule, noting the sixty day maximum, the $75,000 additional deposit credited at closing, and that seller consent is not required. Recommending renegotiation of the closing date without reference to the extension right earns nothing. |
| 18 | `3` | Reports the contingent cost of about $477,020 should the vapour intrusion evaluation show that a sub-slab depressurisation system is required, and presents it separately from the base estimate. Folding the mitigation cost into the base estimate, or omitting it, earns nothing. |
| 19 | `5` | Recommends a risk-based approach built on targeted excavation, an activity and use limitation, vapour intrusion evaluation and monitoring, and rejects unrestricted closure on the grounds that residual impact below the water table and the groundwater exceedance make it unachievable rather than merely expensive. A recommendation supported by that feasibility reasoning earns full credit whatever the precise excavation limits chosen. |
| 20 | `4` | Identifies that Section 9.4 makes the activity and use limitation subject to seller consent, that seller is retaining the adjoining parcel and so has a reason to resist, and that the recommended remedy therefore is not within the buyer's unilateral control. Any handling that names the dependency and states what happens if consent is refused earns full credit. |
| 21 | `3` | Reaches a supported position on the Known Conditions carve-out in Section 9.2, recognising that the former tank and its agency closure file are described in the Phase I so AOC-4 sits outside the indemnity, while noting that the two borings there found no exceedance. Either concluding the carve-out has no present cost or treating it as a budgeted construction risk earns full credit if the reasoning is given. |
| 22 | `4` | Concludes that a vapour intrusion evaluation is required, reasoning from the GW-2 exceedance beneath the planned warehouse footprint rather than from a general precaution, and places it before slab design in the sequence. Any conclusion that connects the groundwater result to the planned building and to the design schedule earns full credit. |
| 23 | `3` | Sets out the remaining data gaps with a duration attached to each, covering at least the vinyl chloride re-analysis and the vapour intrusion round. The specific gaps chosen may vary, but each must carry a stated number of days and the durations must roll up to the critical path figure used elsewhere in the deliverable. |
| 24 | `2` | Delivers a single file named Fairlead_Phase_II_Evaluation_Memo.docx, with that exact name and extension. Any other filename or extension, or a deliverable supplied as chat text rather than a file, earns nothing. |
| 25 | `1` | Presents the work as a memorandum addressed to the client that carries the conclusions, the screening results and the recommendation in the body, so it can be read without reference to an appendix or a separate data package. A bare data dump or an unstructured narrative earns nothing. |
| 26 | `-5` | Screens groundwater against the GW-1 potable supply criteria, which produces around ten additional apparent exceedances across all three downgradient wells and points toward aquifer restoration that is neither required nor useful at this property. Apply once wherever GW-1 is used as the compliance standard. |
| 27 | `-5` | Compares soil volatile results reported in ug/kg directly against screening criteria published in mg/kg, overstating every volatile concentration by a factor of one thousand. Apply once wherever the unconverted comparison appears. |
| 28 | `-4` | Carries the methylene chloride detections forward as site impact and includes them in the constituents of concern or the remedial footprint, when they are attributable to the laboratory method blank. Apply once. |
| 29 | `-4` | Applies the RCRA hazardous disposal rate of $310.00 per ton when the toxicity characteristic leaching results demonstrate the soil is non-hazardous. Apply once wherever hazardous disposal is assumed in the cost estimate. |
| 30 | `-4` | Concludes that vinyl chloride is absent or not a concern on the strength of non-detect results, without recognising that the reporting limit achieved is above the applicable criterion. Apply once. |
| 31 | `-3` | States a figure in one section that contradicts the same figure elsewhere in the deliverable, for example an excavation volume, a cost total or a number of days that differs between the summary and the supporting tables. Apply once. |

---

## Section 3

### How long did this submission take?

Your own clock, in minutes.

