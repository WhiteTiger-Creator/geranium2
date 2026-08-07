import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tracker as t
OUT="/home/azureuser/geranium_tasks/task2_env/RUBRIC.md"
rows=t.build_sample(); med,cut=t.flag_quality(rows); cl=t.cleaned(rows)
w0=t.rake(cl); w=t.trim_and_rerake(cl,w0); n=len(cl)
sp=sum(1 for x in rows if x["_speeder"]); st=sum(1 for x in rows if x["_straight"])
uw,ww=t.umean(cl,'aware'),t.wmean(cl,w,'aware')
u35=sum(1 for x in cl if x["age_band"]=="18-34")/n; o65=sum(1 for x in cl if x["age_band"]=="65+")/n
C=[
("Rigid",4,f"Applies the speeder rule before weighting, using a threshold of one third of the wave median length of interview, which is about {cut:.2f} minutes against a median of {med:.1f}, and removes about {sp} respondents. Weighting an uncleaned file, or setting the threshold by any other rule, earns nothing."),
("Rigid",4,f"Removes about {st} straightliners, defined as an identical response to all eight battery items, counts respondents failing both quality rules once rather than twice, and arrives at a cleaned base of about {n}. A base materially different from that earns nothing."),
("Rigid",5,"Rakes to the three margins in the method note and to those only: age band by gender interlocked, region, and highest educational attainment. Adding a margin, or dropping one, earns nothing."),
("Rigid",5,f"Does not use the syndicated category incidence figure of {t.CATEGORY_INCIDENCE_SYNDICATED:.0%} as a weighting margin, and states why: it is drawn from adults 21 and over on a three month recall window rather than this tracker's universe and twelve month definition, and category use is a measured outcome here rather than a demographic frame. Raking to it earns nothing."),
("Rigid",3,"Treats age by gender as a single interlocked margin of eight cells rather than as two separate margins. Raking to age and gender independently earns nothing."),
("Rigid",4,f"Trims the fitted weights at {t.TRIM_LOW:.2f} and {t.TRIM_HIGH:.2f} and repeats the fit after trimming, rather than trimming and stopping. About nine weights exceed the upper bound before trimming. Trimming without re-fitting, which leaves the margins no longer matching the benchmarks, earns nothing."),
("Rigid",4,f"Reports an effective sample size of about {t.ess(w):.0f}, computed as the square of the sum of the weights over the sum of the squared weights. A figure materially different, or the achieved sample size reported as the effective one, earns nothing."),
("Rigid",3,f"Reports a design effect of about {t.deff(w):.2f}, being the achieved sample size over the effective sample size. Omitting the design effect earns nothing."),
("Rigid",5,f"Reports the margin of error on the effective sample size, giving about {t.moe(w)*100:.2f} percentage points at ninety five percent confidence near a fifty percent proportion, rather than about {1.96*(0.25/n)**0.5*100:.2f} points computed on the achieved sample. Reporting the achieved-base figure earns nothing."),
("Rigid",3,f"Reports unweighted wave 12 awareness of about {uw*100:.1f} per cent, and identifies it as the figure that produced the client's query rather than as the result. Presenting it as the wave 12 result earns nothing."),
("Rigid",5,f"Reports weighted wave 12 awareness of about {ww*100:.1f} per cent. A figure materially different from that, on the method note's scheme, earns nothing."),
("Rigid",5,f"States that the apparent change against wave 11 is about {(uw-0.664)*100:+.1f} points unweighted while the change on the weighted basis is about {(ww-0.664)*100:+.1f} points, and presents the second as the comparable figure. Reporting only one of the two earns nothing."),
("Rigid",4,f"Quantifies the composition problem, with respondents under 35 at about {u35*100:.0f} per cent of the cleaned sample against a benchmark of {sum(v for (a,g),v in t.AGE_GENDER.items() if a=='18-34')*100:.0f} per cent, and those 65 and over at about {o65*100:.0f} per cent against {sum(v for (a,g),v in t.AGE_GENDER.items() if a=='65+')*100:.0f} per cent. Asserting a skew without quantifying it earns nothing."),
("Rigid",4,"Restricts the past twelve month use measure to respondents interviewed on days 3 to 9, because the screener on days 1 and 2 asked about a three month window and does not measure the same thing. Reporting that metric across all field days earns nothing."),
("Rigid",2,"Demonstrates that the weighted sample reproduces each benchmark margin, with the weighted shares matching the population targets on all three margins. Omitting the margin check earns nothing."),
("Rigid",2,"Reports the headline metrics on a base of all adults rather than on category users, consistent with the method note. Rebasing to category users earns nothing."),
("Subjective",5,"Attributes the apparent decline to sample composition arising from the panel supplier substitution, and supports that with the age profile of the achieved sample rather than asserting it. Any explanation that connects the supplier change to the age skew and the age skew to awareness earns full credit; attributing the movement to a change in the market earns nothing."),
("Subjective",4,"Concludes that the brand is flat within the margin of error rather than that it has declined, and expresses that against the corrected figure and the reported precision. Any conclusion that compares the weighted change to the margin of error earns full credit."),
("Subjective",3,"Explains why the syndicated incidence figure was set aside, addressing both the mismatch in universe and recall window and its status as an outcome rather than a frame. Any explanation covering either ground earns full credit; setting it aside silently earns nothing."),
("Subjective",3,"Draws out the precision cost of correcting a wave with two short cells, noting that the effective sample is materially below the achieved sample and that the wave is therefore less precise than usual. Any treatment that connects the shortfalls to the design effect earns full credit."),
("Subjective",3,"Handles the screener change by stating the base used for the affected metric rather than dropping the metric or reporting it without qualification. Either restricting the base or suppressing the metric earns full credit where the reason is stated."),
("Format",2,"Delivers a single file named Wave12_Weighted.xlsx, with that exact name and extension. Any other filename or extension, or a deliverable supplied as chat text rather than a file, earns nothing."),
("Format",2,"Delivers the cleaned respondent file with a weight against every retained row, not summary tables alone, so the client's analyst can reproduce the estimates. Summary output without respondent-level weights earns nothing."),
("Format",1,"Computes the reported estimates and diagnostics as formulas over the weight column rather than typing in results, so the figures recompute if a weight changes. Hard-coded summary figures earn nothing."),
("Negative",-5,"Reports the unweighted awareness figure as the wave 12 result, or places it on the trend line alongside prior waves as a comparable value. Apply once."),
("Negative",-5,"Uses the syndicated category incidence figure as a raking margin. Apply once."),
("Negative",-4,"Reports the margin of error on the achieved sample size rather than the effective sample size, overstating the precision of the wave. Apply once."),
("Negative",-3,"Trims the weights without repeating the fit afterwards, leaving the weighted margins no longer matching the population benchmarks. Apply once."),
("Negative",-3,"Applies the quality removals after weighting rather than before, so the weights are fitted on respondents who are then discarded. Apply once."),
("Negative",-3,"Reports past twelve month use across all field days without addressing the screener wording change on days 1 and 2. Apply once."),
]
pos=sum(x for k,x,_ in C if x>0); neg=sum(x for k,x,_ in C if x<0)
fn=sum(1 for k,x,_ in C if k=="Format"); fw=sum(x for k,x,_ in C if k=="Format")
over=[(i,len(s)) for i,(_,_,s) in enumerate(C,1) if len(s)>500]
L=["# Rubric - form-ready criteria","",f"**{len(C)} criteria.** Paste each string into its own Criterion field; the number goes in the Weight field only.","",
   f"Maximum positive reward {pos}. Negative criteria total {neg}.","",
   f"- Format criteria: {fn} of {len(C)} ({fn/len(C):.0%}), under the half limit",
   f"- Format weight: {fw} of {pos} ({fw/pos:.1%}), under the quarter limit",
   f"- Negative criteria: {sum(1 for k,x,_ in C if x<0)}, above the minimum of two",
   f"- Longest criterion: {max(len(s) for _,_,s in C)} characters","","---",""]
for i,(k,x,s) in enumerate(C,1):
    L+=[f"### Criterion {i}  ·  weight `{x}`  ·  _{k}_","",s,"",f"<sub>{len(s)} / 500 characters</sub>",""]
open(OUT,"w").write("\n".join(L)+"\n")
print(f"{len(C)} criteria | +{pos} / {neg} | format {fn} ({fn/len(C):.0%}), {fw/pos:.1%} | longest {max(len(s) for _,_,s in C)} | over 500: {over or 'none'}")
