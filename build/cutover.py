"""
Sequencing data and solver for the Verwood ERP cutover plan.

The problem is a constrained scheduling problem: 14 sites, 3 deployment teams,
hard predecessor relationships from master-data ownership, fixed plant shutdown
windows, financial blackout weeks, a validation period at the regulated site,
and a legacy support expiry that the last cutover must precede.
"""
from datetime import date, timedelta

CLIENT, INTEGRATOR = "Verwood Specialty Chemicals", "Ostley Rowan Consulting"
PROGRAMME_START = date(2026, 9, 7)      # Monday of programme week 1
LEGACY_SUPPORT_ENDS = date(2027, 6, 30)
TEAMS = 3
VALIDATION_WEEKS = 12                    # regulated site, after technical cutover

# week index 1 == week commencing PROGRAMME_START
def wk(d):
    return (d - PROGRAMME_START).days // 7 + 1

def monday(w):
    return PROGRAMME_START + timedelta(weeks=w - 1)

LAST_WEEK = wk(LEGACY_SUPPORT_ENDS)

# ---------------------------------------------------------------- sites ----
# code, name, country, users, master role, depends on, cutover weeks, shutdown window, gmp
SITES = [
 ("BRD","Bridgnorth","United Kingdom",  610,"Material master", [], 5, None, False),
 ("HAL","Halesworth","United Kingdom",  240,"Customer master", [], 4, None, False),
 ("KIN","Kinloss","United Kingdom",     180,"Vendor master",   [], 4, None, False),
 ("ANT","Antwerp","Belgium",            520,None,["BRD","KIN"], 5, None, False),
 ("ROT","Rotterdam","Netherlands",      460,None,["BRD","KIN"], 4, None, False),
 ("LYO","Lyon","France",                310,None,["BRD"],       4, None, False),
 ("TUR","Turin","Italy",                290,None,["BRD"],       4, None, False),
 ("VAL","Valencia","Spain",             205,None,["BRD"],       3, None, False),
 ("GDA","Gdansk","Poland",              340,None,["BRD","HAL"], 4, None, False),
 ("CHA","Charleston","United States",   580,None,["BRD","HAL"], 5, None, False),
 ("MOB","Mobile","United States",       395,None,["BRD","HAL"], 4, (33, 34), False),
 ("SAR","Sarnia","Canada",              260,None,["BRD","HAL"], 4, (24, 25), False),
 ("PEN","Penang","Malaysia",            215,None,["BRD"],       3, None, False),
 ("COR","Cork","Ireland",               150,None,["BRD","KIN"], 3, None, True),
]

# ------------------------------------------------------- blackout weeks ----
# No cutover may start or run through a financial blackout. Two weeks either
# side of each quarter end, and the whole of January for the annual close.
def blackout_weeks():
    out = set()
    for y in (2026, 2027, 2028):
        for m, d in ((3,31),(6,30),(9,30),(12,31)):
            qe = date(y, m, d)
            for off in (-1,0):
                w = wk(qe) + off
                if 1 <= w <= LAST_WEEK + 20:
                    out.add(w)
        for day in (5, 12, 19):
            w = wk(date(y, 1, day))
            if 1 <= w <= LAST_WEEK + 20:
                out.add(w)
    return out

BLACKOUT = blackout_weeks()

# Plant shutdown windows are expressed above as programme week numbers and are
# the only weeks in which those two sites may begin a cutover.

SITE = {s[0]: dict(code=s[0], name=s[1], country=s[2], users=s[3], master=s[4],
                   deps=s[5], weeks=s[6], shutdown=s[7], gmp=s[8]) for s in SITES}


def free(w, n):
    """True if the n-week span starting at week w avoids every blackout week."""
    return all((w + i) not in BLACKOUT for i in range(n))


def priority_order():
    """Constrained sites first. Master-data owners unblock everything else; the
    regulated site and the two shutdown-window sites have the least freedom."""
    masters = [c for c in SITE if SITE[c]["master"]]
    masters.sort(key=lambda c: -sum(1 for x in SITE.values() if c in x["deps"]))
    constrained = [c for c in SITE if not SITE[c]["master"] and (SITE[c]["gmp"] or SITE[c]["shutdown"])]
    constrained.sort(key=lambda c: (SITE[c]["shutdown"][0] if SITE[c]["shutdown"]
                                    else LAST_WEEK - SITE[c]["weeks"] - VALIDATION_WEEKS))
    rest = [c for c in SITE if c not in masters and c not in constrained]
    rest.sort(key=lambda c: -SITE[c]["users"])
    return masters + constrained + rest


def earliest_start(code, ready, from_week):
    s = SITE[code]
    if s["shutdown"]:
        w = s["shutdown"][0]
        if w < max(ready, from_week) or not free(w, s["weeks"]):
            return None
        return w
    w = max(ready, from_week)
    while w + s["weeks"] - 1 <= LAST_WEEK + 30:
        if free(w, s["weeks"]):
            return w
        w += 1
    return None


def solve():
    sched, done = {}, {}
    team_free = [1] * TEAMS
    for code in priority_order():
        s = SITE[code]
        ready = max([1] + [done[d] for d in s["deps"]])
        best = None
        for ti in range(TEAMS):
            w = earliest_start(code, ready, team_free[ti])
            if w is None:
                continue
            if best is None or w < best[1]:
                best = (ti, w)
        if best is None:
            raise RuntimeError(f"no feasible slot for {code}")
        ti, w = best
        fin = w + s["weeks"]
        sched[code] = dict(team=ti + 1, start=w, end=fin - 1,
                           live=fin + (VALIDATION_WEEKS if s["gmp"] else 0))
        done[code] = fin
        team_free[ti] = fin
    return sched


def check(sched):
    """Return a list of constraint violations; empty means feasible."""
    bad = []
    for c, r in sched.items():
        s = SITE[c]
        for d in s["deps"]:
            if sched[d]["end"] >= r["start"]:
                bad.append(f"{c} starts before its master {d} completes")
        if s["shutdown"] and r["start"] != s["shutdown"][0]:
            bad.append(f"{c} must start in its shutdown window week {s['shutdown'][0]}")
        for i in range(s["weeks"]):
            if (r["start"] + i) in BLACKOUT:
                bad.append(f"{c} runs through blackout week {r['start']+i}")
        if r["live"] > LAST_WEEK:
            bad.append(f"{c} goes live in week {r['live']} after support ends in week {LAST_WEEK}")
    for w in range(1, LAST_WEEK + 1):
        busy = sum(1 for r in sched.values() if r["start"] <= w <= r["end"])
        if busy > TEAMS:
            bad.append(f"week {w} needs {busy} teams")
    return bad


def waves(sched):
    """Group into waves by start week for reporting."""
    order = sorted(sched, key=lambda c: (sched[c]["start"], c))
    wv, cur, last = {}, 1, None
    for c in order:
        st = sched[c]["start"]
        if last is not None and st > last + 1:
            cur += 1
        wv[c] = cur
        last = max(last or st, st)
    return wv
