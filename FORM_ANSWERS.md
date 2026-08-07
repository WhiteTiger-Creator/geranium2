# Submission form - field by field

Rebuilt task 2. Nothing here contains the project code name.

---

## Section 1

### User Prompt  (2232 / 3000 characters)

```
We are a twenty-person air quality and environmental engineering practice in Calvert and most of what I do is permitting for coatings, printing and metal finishing plants.

Cordell Specialty Coatings has board approval for a fourth topcoat line and the equipment order goes in at the end of June. Anselm Vieira runs the plant and his request is 01_Client_Request.docx. He has done his own arithmetic, satisfied himself the project is comfortably under the number that matters, and wants that confirmed before he commits capital. Read what he tells us closely, because two of the things he mentions in passing change the answer and he plainly does not think either of them is relevant.

The line design is in 02_Line4_Design_Data.xlsx and the coating and solvent properties are in 03_Coating_Data_Sheets.xlsx. Their current permit is 04_Existing_Permit.docx and the applicability provisions are in 05_Air_Regulation_5.docx. Work from that regulation rather than from what you remember of similar programmes elsewhere, because its definitions are what govern here and one of them is not what you would expect. Thurlow has put up two capture arrangements in 06_Control_Equipment.docx and has declined to recommend either, which is fair because it is a permitting question and not an equipment one. Current facility emissions are in 07_Facility_Emissions.xlsx, pricing is in 08_Cost_Estimates.xlsx, and the agency file is summarised in 09_Permit_History.docx.

What Anselm needs is whether the project triggers major source review, and if it does, what he can do about it, what each route costs and how many months it takes. Work the applicability logic in order and show it: potential to emit, what aggregates with this project, what nets against it if anything, and only then the threshold tests. Several of those steps have a defensible answer and a convenient one and they are not the same.

Give it back as one workbook named Cordell_NSR_Analysis.xlsx, built on live formulas off the design data and the regulation thresholds rather than typed-in results, and lead with a sheet carrying the determination, the recommended route and what it costs. He is an engineer and will follow a calculation, but he will act on the first sheet.
```

### O*NET Occupation

`Environmental Engineers` - 17-2081.00

### O*NET Tasks (select these four, verbatim)

- Provide technical support for environmental remediation or litigation projects, including remediation system design or determination of regulatory applicability.
- Advise industries or government agencies about environmental policies and standards.
- Obtain, update, or maintain plans, permits, or standard operating procedures.
- Design, or supervise the design of, systems, processes, or equipment for control, management, or remediation of water, air, or soil quality.

### O*NET Skills (from Skills, not Technology Skills)

- Mathematics
- Critical Thinking
- Reading Comprehension
- Science
- Writing

### Input File Uploader

Upload `cordell_input_files.zip` - 9 files, flat, no subfolders.

### How many input files are tied to your prompt?

**9**

### Are the input files multi-modal?

**No.** All nine are .docx or .xlsx.

### Is web search allowed in your prompt?

**No.** Self-contained. The regulation, the permit, the emission data and the pricing are all supplied.

### Manual completion time

**8 hours**

---

## Section 2

### Golden Solution File Uploader

Upload `cordell_golden_solution.zip` - one file, `Cordell_NSR_Analysis.xlsx`.

### What LLM did you use as a starting point?

Answer honestly for your own workflow.

### Rubric - 30 criteria

Max positive **85**; negatives **-25**. Format 3 of 30 criteria (10%), 5.9% of reward. 6 negative criteria. Longest 381 chars.

| # | Weight | Criterion |
|---|---|---|
| 1 | `5` | Computes potential to emit on 365 days, being 8,760 hours, and states that the plant's 250 day schedule cannot be credited because Regulation 5.02(b) counts an operating limitation only where it is federally enforceable and no permit condition restricts hours. Using the stated schedule earns nothing. |
| 2 | `4` | Uses the coating volatile organic compound content less water and exempt compounds of 3.80 lb/gal rather than the as-supplied value of 2.90 lb/gal, consistent with permit condition 3.2. Using the as-supplied value earns nothing. |
| 3 | `5` | Calculates overall control as the product of capture and destruction, 92% times 98% giving about 90.16%, per Regulation 5.02(d). Crediting the destruction efficiency alone earns nothing. |
| 4 | `4` | Reports Line 4 potential to emit of about 30.94 tons per year, being the controlled coating stream plus the uncontrolled cleanup solvent. A figure that omits the cleanup solvent or applies control to it earns nothing. |
| 5 | `4` | Aggregates the August 2025 Line 2 debottleneck of 6.20 tons per year with this project under Regulation 5.03(b), notwithstanding that no permit was obtained for it. Treating Line 4 in isolation earns nothing. |
| 6 | `3` | Reports a project emissions increase of about 37.14 tons per year and notes that this is below the 40 ton significance threshold. Omitting the comparison, or reporting an increase that excludes the Line 2 change, earns nothing. |
| 7 | `5` | Computes facility potential to emit after the project as about 119.14 tons per year against the 100 ton major source threshold, and concludes the facility becomes a major stationary source. Stopping at the significance test earns nothing. |
| 8 | `5` | States that because the project makes a minor source major, Regulation 5.04(b) requires it to be reviewed as a new major stationary source, that the emissions of the entire project are subject to review, and that netting is not available. Concluding that no review is triggered because the increase is below the significance threshold earns nothing. |
| 9 | `5` | Excludes the 4.20 tons per year of fugitive emissions from the major source determination, because surface coating manufacture is not a listed category under Regulation 5.02(c), and notes that including them would push the recommended option back over the threshold. Including fugitives earns nothing. |
| 10 | `4` | Concludes that the 14 ton 2022 Line 1 shutdown is not creditable, on the grounds that it was relied upon in full in revision R-23-0412 and that netting is unavailable where a project makes a minor source major. Applying the credit earns nothing. |
| 11 | `3` | Checks hazardous air pollutants and concludes the facility does not become major, with xylene at about 8.13 tons per year against the 10 ton single pollutant threshold and an aggregate below 25. Omitting the hazardous air pollutant check earns nothing. |
| 12 | `2` | Treats the cleanup solvent as uncontrolled, at about 2.28 tons per year, because it is not ducted to the oxidiser under either capture arrangement. Applying control to it earns nothing. |
| 13 | `5` | Demonstrates that a permanent total enclosure raises overall control to about 98% and brings facility potential to emit to roughly 96.30 tons per year, below the major source threshold at full design throughput. An option analysis that does not compute the resulting facility total earns nothing. |
| 14 | `3` | Quantifies the throughput cap alternative at roughly 138 gallons per day, about 33% of the design rate, and identifies that the limit must be federally enforceable to count. Presenting a cap without the resulting throughput earns nothing. |
| 15 | `3` | Prices the major source route at about $1,736,461, including offsets of 42.71 tons at the 1.15 to one ratio costing about $401,461. Omitting offsets, or applying them without the ratio, earns nothing. |
| 16 | `3` | Prices the enclosure route at about $983,000 and quantifies the difference against the major source route at roughly $753,461. Comparing the options without a cost difference earns nothing. |
| 17 | `3` | States the permitting duration for each route, 14 to 18 months for major source review against 4 to 5 for a minor revision, and relates it to the client's second quarter start. Omitting the schedule earns nothing. |
| 18 | `5` | Recommends the permanent total enclosure and supports it on both the threshold arithmetic and the permitting schedule, rather than on capital cost alone. Any recommendation that keeps the facility below the major source threshold at full throughput and is justified against cost and schedule together earns full credit; a recommendation with no supporting comparison earns nothing. |
| 19 | `4` | Corrects the client's stated premise that the project is acceptable because the increase is below forty tons per year, explaining that the significance threshold applies only at a source that is already major. Any explanation that distinguishes the modification test from the new major source test earns full credit. |
| 20 | `3` | Identifies the unpermitted August 2025 Line 2 change as a compliance matter in its own right, contrary to permit condition 7.2, and reaches a position on how it should be resolved. Either recommending it be regularised within this application or addressed separately earns full credit where the reasoning is given. |
| 21 | `2` | Notes that the margin to the threshold under the recommended option is only a few tons per year and draws a consequence from it, such as verification of the enclosure or caution about future changes. Any handling that quantifies the headroom and states why it matters earns full credit. |
| 22 | `2` | Delivers a single file named Cordell_NSR_Analysis.xlsx, with that exact name and extension. Any other filename or extension, or a deliverable supplied as chat text rather than a file, earns nothing. |
| 23 | `2` | Builds the workbook on live formulas resolving back to the design data and the regulation thresholds, so the determination re-computes if a coating property or a control efficiency changes. A workbook of hard-coded results earns nothing. |
| 24 | `1` | Leads with a sheet carrying the applicability determination, the recommended route and its cost, so the answer is readable without working through the calculation sheets. Burying the determination among the calculations earns nothing. |
| 25 | `-5` | Concludes that major source review is not triggered because the project increase of about 37 tons per year is below the significance threshold. Apply once wherever that conclusion is stated. |
| 26 | `-5` | Calculates potential to emit on the plant's 250 day operating schedule rather than on 8,760 hours. Apply once wherever the restricted schedule is used. |
| 27 | `-4` | Includes fugitive emissions in the major stationary source determination, when surface coating manufacture is not a listed category. Apply once. |
| 28 | `-4` | Applies the 2022 Line 1 shutdown as a netting credit against this project. Apply once. |
| 29 | `-4` | Credits the oxidiser destruction efficiency without applying capture efficiency, or uses the as-supplied coating volatile organic compound content instead of the less water value. Apply once for either error. |
| 30 | `-3` | States a figure in one place that contradicts the same figure elsewhere in the workbook, for example a potential to emit, a cost total or a control efficiency that differs between the summary sheet and the calculation sheets. Apply once. |

---

## Section 3

Your own clock, in minutes.

