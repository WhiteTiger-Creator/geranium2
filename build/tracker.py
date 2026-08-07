"""
Halloway Brand Tracker, wave 12. Data generation and the weighting calculation.

Deterministic throughout: the pseudo-random draws come from a stable FNV hash of
the respondent id, so the dataset and the golden solution cannot diverge.
"""
AGENCY, CLIENT = "Ferndale Insight Group", "Halloway Foods"
WAVE, N_RAW = 12, 1334

# --------------------------------------------------------------- benchmarks
AGE_GENDER = {("18-34","Male"):0.146, ("18-34","Female"):0.142,
              ("35-54","Male"):0.159, ("35-54","Female"):0.163,
              ("55-64","Male"):0.081, ("55-64","Female"):0.087,
              ("65+","Male"):0.096,   ("65+","Female"):0.126}
REGION = {"Northeast":0.171, "Midwest":0.206, "South":0.383, "West":0.240}
EDUCATION = {"High school or less":0.378, "Some college":0.279, "Bachelor's or higher":0.343}

# A syndicated figure supplied in the benchmark file. It is NOT a raking margin:
# different universe (21+) and a different recall window (3 months, not 12).
CATEGORY_INCIDENCE_SYNDICATED = 0.62

# ---------------------------------------------------------------- method ---
TRIM_LOW, TRIM_HIGH, TRIM_CYCLES = 0.30, 3.00, 3
LOI_MEDIAN_FRACTION = 1/3.0
BATTERY_ITEMS = 8
PRIOR_WAVES = {9:0.671, 10:0.668, 11:0.664}

# ----------------------------------------------------------- fieldwork -----
SUPPLIER_DAYS = {"Meridian": (1,3), "Colwyn": (4,9)}
SCREENER_ERROR_DAYS = (1,2)      # narrower recall window in field on days 1 and 2
QUOTA_TARGETS = {"65+":180, "Northeast":216}

# true propensities used to build the sample
AWARE_BY_AGE = {"18-34":0.45, "35-54":0.70, "55-64":0.80, "65+":0.86}
CONSIDER_GIVEN_AWARE = {"18-34":0.41, "35-54":0.47, "55-64":0.50, "65+":0.52}
USED_GIVEN_CONSIDER = 0.58
WAVE12_TRUE_SHIFT = -0.013       # a genuine, small decline


def _h(s):
    h = 2166136261
    for ch in str(s):
        h = ((h ^ ord(ch)) * 16777619) & 0xFFFFFFFF
    return h


def _u(s):
    return (_h(s) % 100000) / 100000.0


def _pick(s, options):
    """options: list of (value, weight)."""
    u = _u(s) * sum(w for _, w in options)
    c = 0.0
    for v, w in options:
        c += w
        if u <= c:
            return v
    return options[-1][0]


def build_sample():
    rows = []
    for i in range(1, N_RAW + 1):
        rid = f"R{i:05d}"
        day = _pick(rid + "day", [(d, 1.0) for d in range(1, 4)] + [(d, 1.55) for d in range(4, 10)])
        supplier = "Meridian" if day <= 3 else "Colwyn"
        # Colwyn skews young and urban; Meridian is closer to balanced
        if supplier == "Colwyn":
            age_band = _pick(rid+"age", [("18-34",0.55),("35-54",0.28),("55-64",0.11),("65+",0.06)])
            urban = _pick(rid+"urb", [("Urban",0.52),("Suburban",0.36),("Rural",0.12)])
        else:
            age_band = _pick(rid+"age", [("18-34",0.27),("35-54",0.33),("55-64",0.19),("65+",0.21)])
            urban = _pick(rid+"urb", [("Urban",0.34),("Suburban",0.46),("Rural",0.20)])
        gender = _pick(rid+"gen", [("Male",0.47),("Female",0.53)])
        region = _pick(rid+"reg", [("Northeast",0.135),("Midwest",0.205),("South",0.395),("West",0.265)])
        edu = _pick(rid+"edu", [("High school or less",0.30),("Some college",0.28),("Bachelor's or higher",0.42)])
        # length of interview, minutes
        base_loi = 7.4 + (_u(rid+"loi") - 0.5) * 5.2
        speeder = _u(rid+"sp") < 0.047
        loi = round(1.6 + _u(rid+"loi2")*1.1, 1) if speeder else round(max(4.2, base_loi), 1)
        # battery, 1 to 5
        straight = _u(rid+"st") < 0.036
        if straight:
            v = 1 + _h(rid+"stv") % 5
            battery = [v]*BATTERY_ITEMS
        else:
            battery = [1 + _h(rid+f"b{k}") % 5 for k in range(BATTERY_ITEMS)]
        p_aw = min(0.97, max(0.02, AWARE_BY_AGE[age_band] + WAVE12_TRUE_SHIFT))
        aware = 1 if _u(rid+"aw") < p_aw else 0
        consider = 1 if (aware and _u(rid+"co") < CONSIDER_GIVEN_AWARE[age_band]) else 0
        used = 1 if (consider and _u(rid+"us") < USED_GIVEN_CONSIDER) else 0
        rows.append(dict(respondent_id=rid, field_day=day, supplier=supplier,
                         screener_version=("v1_3month" if day <= SCREENER_ERROR_DAYS[1] else "v2_12month"),
                         loi_minutes=loi, age_band=age_band, gender=gender, region=region,
                         education=edu, urbanicity=urban, aware=aware, consider=consider,
                         used_12m=used, **{f"b{k+1}": battery[k] for k in range(BATTERY_ITEMS)}))
    return rows


# --------------------------------------------------------- quality rules ---
def median(xs):
    s = sorted(xs); n = len(s)
    return s[n//2] if n % 2 else (s[n//2-1]+s[n//2])/2


def flag_quality(rows):
    med = median([r["loi_minutes"] for r in rows])
    cut = med * LOI_MEDIAN_FRACTION
    for r in rows:
        r["_speeder"] = r["loi_minutes"] < cut
        b = [r[f"b{k+1}"] for k in range(BATTERY_ITEMS)]
        r["_straight"] = len(set(b)) == 1
    return med, cut


def cleaned(rows):
    return [r for r in rows if not r["_speeder"] and not r["_straight"]]


# ------------------------------------------------------------- raking ------
MARGINS = [("age_gender", AGE_GENDER), ("region", REGION), ("education", EDUCATION)]


def key(r, name):
    if name == "age_gender":
        return (r["age_band"], r["gender"])
    return r["region"] if name == "region" else r["education"]


def rake(rows, iterations=60, w=None):
    n = len(rows)
    w = w[:] if w else [1.0]*n
    for _ in range(iterations):
        for name, target in MARGINS:
            tot = sum(w)
            cur = {}
            for r, wi in zip(rows, w):
                cur[key(r, name)] = cur.get(key(r, name), 0.0) + wi
            for i, r in enumerate(rows):
                k = key(r, name)
                if cur.get(k):
                    w[i] *= (target[k]*tot)/cur[k]
    m = sum(w)/n
    return [x/m for x in w]          # normalise to mean 1


def trim_and_rerake(rows, w):
    for _ in range(TRIM_CYCLES):
        capped = [min(max(x, TRIM_LOW), TRIM_HIGH) for x in w]
        if capped == w:
            break
        w = rake(rows, 40, capped)
    return w


def ess(w):
    return sum(w)**2 / sum(x*x for x in w)


def deff(w):
    return len(w)/ess(w)


def moe(w, p=0.5):
    return 1.96 * (p*(1-p)/ess(w))**0.5


def wmean(rows, w, field):
    return sum(r[field]*wi for r, wi in zip(rows, w))/sum(w)


def umean(rows, field):
    return sum(r[field] for r in rows)/len(rows)
