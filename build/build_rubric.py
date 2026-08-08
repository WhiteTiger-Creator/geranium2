import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cutover as c
OUT="/home/azureuser/geranium_tasks/task2_env/RUBRIC.md"
s=c.solve(); wv=c.waves(s)
LAST=max(v['live'] for v in s.values()); FLOAT=c.LAST_WEEK-LAST
BL=sorted(w for w in c.BLACKOUT if w<=c.LAST_WEEK)
CORLATE=c.LAST_WEEK-c.SITE['COR']['weeks']-c.VALIDATION_WEEKS
NDEP=sum(1 for x in c.SITE.values() if 'BRD' in x['deps'])
C=[
("Rigid",5,f"Places Bridgnorth in the first wave, on the ground that it owns material master and {NDEP} of the fourteen sites cannot start until it completes. Any plan that schedules Bridgnorth after another dependent site earns nothing."),
("Rigid",4,"Schedules all three master data owners, Bridgnorth, Halesworth and Kinloss, in the first wave so that the dependency chain is released as early as possible. Scheduling a master data owner behind a site that consumes its domain earns nothing."),
("Rigid",5,f"Schedules Cork early rather than late, recognising that its {c.VALIDATION_WEEKS} week validation period runs after the technical cutover and that it must therefore begin by about programme week {CORLATE} to be live before support ends. Placing Cork in the final waves because it is the smallest site earns nothing."),
("Rigid",5,f"Starts Sarnia in programme week {c.SITE['SAR']['shutdown'][0]} and Mobile in programme week {c.SITE['MOB']['shutdown'][0]}, being their annual shutdown windows, and treats those weeks as fixed points around which the rest of the plan is built. Starting either site in any other week earns nothing."),
("Rigid",5,f"Places no cutover in a financial blackout week and allows none to run through one. A blackout is the week containing a quarter end and the week before it, and the first three weeks of January; on the programme calendar those are weeks {', '.join(str(w) for w in BL)}. A plan in which any site's cutover spans one of them earns nothing."),
("Rigid",5,f"Keeps the number of sites in cutover in any programme week at or below {c.TEAMS}, the number of deployment teams. A plan requiring a fourth concurrent team in any week earns nothing."),
("Rigid",5,f"Brings every site live on or before programme week {c.LAST_WEEK}, the week in which legacy support ends, treating Cork's live date as the end of validation rather than the end of its technical cutover. A plan in which any site goes live later earns nothing."),
("Rigid",4,"Respects every master data dependency listed in the site profile, so that no site begins its cutover before each of the sites it depends on has completed. A plan violating any single dependency earns nothing."),
("Rigid",4,f"Uses the cutover durations given in the site profile without altering them, so that the fourteen sites consume {sum(x['weeks'] for x in c.SITE.values())} team weeks in total. Shortening a duration to make the plan fit earns nothing."),
("Rigid",3,f"States the programme week of the last go-live and the float remaining to the support deadline, with both figures consistent with the schedule presented. On a plan that satisfies every constraint the last go-live falls at or before programme week {c.LAST_WEEK}. A plan that does not say how much room is left earns nothing."),
("Rigid",3,"Assigns each site to a named deployment team and shows the loading week by week, so that the concurrency constraint can be seen rather than asserted. A plan giving dates without team assignment earns nothing."),
("Rigid",3,f"Does not schedule Charleston in the first wave despite it being the largest site at {c.SITE['CHA']['users']} users, because it depends on both Bridgnorth and Halesworth. A size-ordered plan that leads with Charleston earns nothing."),
("Rigid",2,"Converts programme week numbers to calendar dates using the stated start of programme week 1, so the plan can be read against the client's calendar. A plan expressed only in week numbers earns nothing."),
("Rigid",2,"Treats validation at Cork as not occupying a deployment team, so the team is released at the end of the technical cutover rather than at go-live. Holding a team through validation earns nothing."),
("Subjective",3,"Explains the sequence as driven by which sites have the least freedom to move rather than by site size, user count or business importance. Any rationale that makes constraint severity the ordering principle earns full credit; a plan presented without a stated rationale earns nothing."),
("Subjective",2,"Identifies the fixed points the rest of the plan is built around: the master data owners, the two sites limited to a shutdown window, and the regulated site. Naming all three categories earns full credit; naming only some of them earns nothing."),
("Subjective",4,"Identifies which sites carry programme risk and why, recognising that a slip on Bridgnorth moves the eleven sites that depend on it and that a slip causing Sarnia or Mobile to miss its shutdown window moves that site by a full year. Any risk treatment that distinguishes the sites with no recovery from those with float earns full credit."),
("Subjective",3,"Addresses the two failed internal attempts described in the brief, showing why a size-ordered sequence and an evenly spread sequence each break. Any explanation that names the specific constraint each approach violates earns full credit."),
("Subjective",3,"Shows each constraint as satisfied by the plan rather than stating that it has been met, so the steering committee can verify the plan rather than trust it. Any presentation that tests the constraints against the schedule itself earns full credit."),
("Subjective",3,"Locates where the float sits in the programme and observes which sites it does and does not protect, noting that float at the end of the programme does not help the shutdown sites or the regulated site. Any treatment that connects the float to specific sites earns full credit."),
("Format",2,"Delivers a single file named Cutover_Plan.xlsx, with that exact name and extension. Any other filename or extension, or a deliverable supplied as chat text rather than a file, earns nothing."),
("Format",2,"Presents the plan as a schedule that can be read directly, with one row per site carrying wave, team, start week and calendar date, rather than as narrative describing what the sequence should be. A prose description without a schedule earns nothing."),
("Format",1,"Shows team loading across the programme weeks so that concurrency and the blackout periods are visible. A plan without a time-phased view earns nothing."),
("Negative",-5,"Produces a plan in which any site begins its cutover before a site it depends on for master data has completed. Apply once."),
("Negative",-5,"Produces a plan in which more than three sites are in cutover in any programme week. Apply once."),
("Negative",-5,"Starts Sarnia or Mobile outside its stated shutdown window. Apply once for either."),
("Negative",-4,"Places Cork in the final waves, so that its validation period runs past the end of legacy support. Apply once."),
("Negative",-4,"Schedules any cutover to start in or run through a financial blackout week, being a week containing a quarter end, the week immediately before one, or one of the first three weeks of January. Apply once."),
("Negative",-3,"Treats Cork as live at the end of its technical cutover rather than at the end of validation, understating the date by which it must start. Apply once."),
("Negative",-3,"Alters a cutover duration, adds a fourth deployment team, or moves a shutdown window in order to make the plan fit, when the brief states that none of these is available. Apply once."),
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
print(f"{len(C)} criteria | +{pos} / {neg} | format {fn} ({fn/len(C):.0%}), {fw/pos:.1%} | longest {max(len(t) for _,_,t in C)} | over 500: {over or 'none'}")
