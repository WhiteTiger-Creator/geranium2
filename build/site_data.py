"""
Canonical dataset for the Fairlead Street Phase II evaluation task.

Inputs, golden solution and rubric all derive from this module, so they cannot
drift apart. Nothing is random; the de-rounding at the bottom is a stable hash.

Units follow laboratory convention: soil VOCs in ug/kg, soil metals in mg/kg,
groundwater in ug/L. Screening levels are published in mg/kg and ug/L.
"""
from datetime import date

SITE = "1480 Fairlead Street"
CITY = "Brayton, Ostrander"
ACRES = 6.2
CLIENT = "Kestrel Industrial Partners LLC"
FIRM = "Marchbank Environmental, Inc."

ASSIGNMENT_DATE = date(2026, 3, 9)
DD_EXPIRY = date(2026, 3, 31)          # due diligence period ends
ESCROW_CAP = 350000                     # PSA environmental escrow cap

# --------------------------------------------------------------- areas ------
# Physical footprints of the site features, from the Phase I and the field work.
AOC = {
    "AOC-1": dict(name="Former electroplating line (interior, Building A)",
                  dims="65 ft x 40 ft", area_sf=2600),
    "AOC-2": dict(name="Former degreaser AST pad (exterior, east yard)",
                  dims="30 ft x 40 ft", area_sf=1200),
    "AOC-3": dict(name="Former floor-drain dry well (exterior, north yard)",
                  dims="20 ft x 20 ft affected footprint around a 6 ft diameter structure",
                  area_sf=400),
    "AOC-4": dict(name="Former 4,000-gallon heating oil UST basin (removed 1998)",
                  dims="18 ft x 24 ft", area_sf=432),
    "BKG":   dict(name="Upgradient / off-source reference location", dims="n/a", area_sf=0),
}

# ------------------------------------------------------------- borings ------
# id, AOC, northing-ish label, total depth, water first encountered, note
BORINGS = [
    ("SB-01", "AOC-1", 16, 11.5, "Interior, north end of former plating line"),
    ("SB-02", "AOC-1", 16, 11.0, "Interior, beneath former rinse tank pit"),
    ("SB-03", "AOC-1", 16, 11.5, "Interior, south end of former plating line"),
    ("SB-04", "AOC-1", 16, 12.0, "Interior, former chemical storage alcove"),
    ("SB-05", "AOC-2", 16, 10.5, "Exterior, north edge of former AST pad"),
    ("SB-06", "AOC-2", 16, 10.5, "Exterior, centre of former AST pad"),
    ("SB-07", "AOC-2", 16, 11.0, "Exterior, south edge of former AST pad"),
    ("SB-08", "AOC-3", 20, 10.0, "Adjacent to former dry well structure"),
    ("SB-09", "AOC-3", 20, 10.0, "3 ft north of former dry well structure"),
    ("SB-10", "AOC-4", 14, 11.0, "Former UST basin, east sidewall"),
    ("SB-11", "AOC-4", 14, 11.0, "Former UST basin, west sidewall"),
    ("SB-12", "BKG",   12, 12.0, "West property boundary, upgradient of all AOCs"),
]

WELLS = [
    ("TW-01", "AOC-1", "Downgradient of former plating line"),
    ("TW-02", "AOC-2", "Downgradient of former AST pad"),
    ("TW-03", "AOC-3", "Adjacent to former dry well"),
    ("TW-04", "BKG",   "Upgradient, west property boundary"),
]

# ------------------------------------------------------------- analytes -----
VOC = ["Tetrachloroethene", "Trichloroethene", "cis-1,2-Dichloroethene",
       "Vinyl chloride", "1,1,1-Trichloroethane", "Methylene chloride"]
MET = ["Arsenic", "Cadmium", "Chromium, total", "Lead", "Nickel"]

# Typical soil reporting limits: VOC in ug/kg, metals in mg/kg
SOIL_RL = {"Tetrachloroethene": 5.0, "Trichloroethene": 5.0, "cis-1,2-Dichloroethene": 5.0,
           "Vinyl chloride": 50.0, "1,1,1-Trichloroethane": 5.0, "Methylene chloride": 10.0,
           "Arsenic": 0.50, "Cadmium": 0.20, "Chromium, total": 1.0, "Lead": 1.0, "Nickel": 2.0}
GW_RL = {"Tetrachloroethene": 1.0, "Trichloroethene": 1.0, "cis-1,2-Dichloroethene": 1.0,
         "Vinyl chloride": 1.0, "1,1,1-Trichloroethane": 1.0, "Methylene chloride": 2.0,
         "Arsenic": 2.0, "Cadmium": 1.0, "Chromium, total": 5.0, "Lead": 3.0, "Nickel": 10.0}

# ------------------------------------------------- screening levels ---------
# Ostrander DEQ Risk-Based Screening Levels. Soil in mg/kg, groundwater in ug/L.
SOIL_SL = {
    #                       residential DC, industrial DC, soil-to-groundwater
    "Tetrachloroethene":        (24,   110,   0.60),
    "Trichloroethene":          (6.0,  28,    0.30),
    "cis-1,2-Dichloroethene":   (160,  720,   4.0),
    "Vinyl chloride":           (0.60, 2.8,   0.020),
    "1,1,1-Trichloroethane":    (1200, 5400,  12),
    "Methylene chloride":       (53,   240,   0.90),
    "Arsenic":                  (7.0,  30,    15),
    "Cadmium":                  (39,   170,   3.0),
    "Chromium, total":          (180,  800,   100),
    "Lead":                     (400,  800,   200),
    "Nickel":                   (820,  3600,  130),
}
GW_SL = {
    #                       GW-1 potable, GW-2 vapour, GW-3 discharge
    "Tetrachloroethene":        (5.0,   300,    3000),
    "Trichloroethene":          (5.0,   500,    2000),
    "cis-1,2-Dichloroethene":   (70,    4000,   20000),
    "Vinyl chloride":           (2.0,   200,    1000),
    "1,1,1-Trichloroethane":    (200,   9000,   30000),
    "Methylene chloride":       (5.0,   4000,   10000),
    "Arsenic":                  (10,    None,   900),
    "Cadmium":                  (5.0,   None,   150),
    "Chromium, total":          (100,   None,   500),
    "Lead":                     (15,    None,   100),
    "Nickel":                   (100,   None,   1400),
}

ARSENIC_BACKGROUND = (4.0, 22.0)        # regional background range, mg/kg

# ---------------------------------------------------- soil detections -------
# (boring, depth_top) -> {analyte: value}. VOC in ug/kg, metals in mg/kg.
# Everything not listed is non-detect at the reporting limit.
SOIL_HITS = {
    ("SB-01", 2):  {"Lead": 318, "Chromium, total": 244, "Nickel": 96, "Arsenic": 9.4,
                    "Methylene chloride": 1180},
    ("SB-01", 6):  {"Lead": 505, "Chromium, total": 1120, "Cadmium": 61, "Nickel": 140,
                    "Arsenic": 8.1},
    ("SB-01", 10): {"Lead": 44, "Chromium, total": 38, "Arsenic": 6.2},
    ("SB-02", 2):  {"Lead": 1420, "Cadmium": 212, "Chromium, total": 690, "Nickel": 305,
                    "Arsenic": 11.8, "Methylene chloride": 940},
    ("SB-02", 6):  {"Lead": 866, "Cadmium": 118, "Chromium, total": 402, "Nickel": 188,
                    "Arsenic": 9.0},
    ("SB-02", 10): {"Lead": 61, "Chromium, total": 45, "Arsenic": 7.4},
    ("SB-03", 2):  {"Lead": 274, "Chromium, total": 196, "Arsenic": 8.8},
    ("SB-03", 6):  {"Lead": 913, "Chromium, total": 358, "Cadmium": 74, "Arsenic": 10.2},
    ("SB-03", 10): {"Lead": 38, "Chromium, total": 29, "Arsenic": 5.9},
    ("SB-04", 2):  {"Lead": 149, "Chromium, total": 88, "Arsenic": 7.7,
                    "Methylene chloride": 2100},
    ("SB-04", 6):  {"Lead": 96, "Chromium, total": 61, "Arsenic": 6.8},
    ("SB-05", 2):  {"Tetrachloroethene": 41000, "Trichloroethene": 3100,
                    "cis-1,2-Dichloroethene": 2400, "Arsenic": 6.1, "Lead": 32},
    ("SB-05", 6):  {"Tetrachloroethene": 12000, "Trichloroethene": 980, "Arsenic": 5.4},
    ("SB-05", 10): {"Tetrachloroethene": 410, "Arsenic": 5.0},
    ("SB-06", 2):  {"Tetrachloroethene": 168000, "Trichloroethene": 4200,
                    "cis-1,2-Dichloroethene": 12000, "Arsenic": 6.6, "Lead": 40,
                    "Methylene chloride": 1650},
    ("SB-06", 6):  {"Tetrachloroethene": 74000, "Trichloroethene": 2900,
                    "cis-1,2-Dichloroethene": 5100, "Arsenic": 5.8},
    ("SB-06", 10): {"Tetrachloroethene": 690, "Trichloroethene": 110, "Arsenic": 5.2},
    ("SB-07", 2):  {"Tetrachloroethene": 22000, "Trichloroethene": 1400, "Arsenic": 6.0},
    ("SB-07", 6):  {"Tetrachloroethene": 8600, "Arsenic": 5.6},
    ("SB-08", 4):  {"Tetrachloroethene": 3400, "Trichloroethene": 620,
                    "cis-1,2-Dichloroethene": 890, "Lead": 212, "Arsenic": 7.1},
    ("SB-08", 10): {"Tetrachloroethene": 1900, "Trichloroethene": 340, "Arsenic": 6.4},
    ("SB-09", 4):  {"Tetrachloroethene": 2600, "Trichloroethene": 410, "Lead": 168,
                    "Arsenic": 6.9, "Methylene chloride": 1020},
    ("SB-09", 10): {"Tetrachloroethene": 1100, "Arsenic": 6.0},
    ("SB-10", 4):  {"1,1,1-Trichloroethane": 640, "Lead": 88, "Arsenic": 7.2},
    ("SB-10", 8):  {"Lead": 52, "Arsenic": 6.5},
    ("SB-11", 4):  {"Lead": 71, "Arsenic": 6.8},
    ("SB-12", 2):  {"Arsenic": 16.4, "Lead": 28, "Chromium, total": 22},
    ("SB-12", 6):  {"Arsenic": 14.9, "Lead": 19, "Chromium, total": 18},
}

# Field duplicate: SB-03 (6 ft) collected as blind duplicate FD-01.
FIELD_DUP = ("SB-03", 6, "FD-01", {"Lead": 372, "Chromium, total": 331, "Cadmium": 69,
                                   "Arsenic": 9.6})

# TCLP performed on the two highest total-lead soil samples.
TCLP = {("SB-02", 2): 3.1, ("SB-03", 6): 1.8}      # mg/L, RCRA limit is 5.0
TCLP_LIMIT = 5.0

# ------------------------------------------------ groundwater results -------
GW_HITS = {
    "TW-01": {"Tetrachloroethene": 84, "Trichloroethene": 31, "cis-1,2-Dichloroethene": 62,
              "Lead": 41, "Chromium, total": 118, "Arsenic": 7.4},
    "TW-02": {"Tetrachloroethene": 1240, "Trichloroethene": 186, "cis-1,2-Dichloroethene": 340,
              "Vinyl chloride": 14, "Arsenic": 6.1},
    "TW-03": {"Tetrachloroethene": 470, "Trichloroethene": 96, "cis-1,2-Dichloroethene": 210,
              "Vinyl chloride": 6.2, "Arsenic": 5.8},
    "TW-04": {"Arsenic": 5.2},
}
# TW-03 VOC aliquot analysed 3 days beyond the 14-day holding time.
HOLDING_TIME_ISSUE = "TW-03"

# ------------------------------------------------------- laboratory QC ------
METHOD_BLANK = {"Methylene chloride": 620}        # ug/kg, soil VOC method blank
BLANK_RULE_FACTOR = 5                              # common laboratory contaminant
DUP_RPD_LIMIT = 30                                 # percent, for soil

# ------------------------------------------------------ remedial costs ------
UNIT_COSTS = [
    ("Mobilisation and demobilisation", "lump sum", 28500, "LS"),
    ("Excavation, load and haul preparation", "per cubic yard in-situ", 18.75, "CY"),
    ("Transport and disposal, non-hazardous industrial soil", "per ton", 62.50, "TON"),
    ("Transport and disposal, RCRA hazardous soil", "per ton", 310.00, "TON"),
    ("Certified clean backfill, supplied and placed", "per cubic yard", 34.00, "CY"),
    ("Confirmation sampling and laboratory analysis", "per sample set", 1150, "EA"),
    ("Dewatering, treatment and discharge", "lump sum", 22000, "LS"),
    ("Engineering oversight, air monitoring and completion report", "lump sum", 46500, "LS"),
    ("Activity and use limitation: drafting, agency review and recording", "lump sum", 12800, "LS"),
    ("Vapour intrusion evaluation: sub-slab and indoor air, two rounds", "lump sum", 38400, "LS"),
    ("Quarterly groundwater monitoring, four wells", "per round", 9600, "RND"),
    ("Sub-slab depressurisation system, design and installation", "lump sum", 61000, "LS"),
]
SOIL_DENSITY = 1.45          # tons per in-situ cubic yard
CONFIRMATION_SETS = 14
MONITORING_ROUNDS = 4
CONTINGENCY = 0.20

# Laboratory turnaround and scheduling, from the case narrative and the cost basis
REANALYSIS_BUSINESS_DAYS = 10
VI_SCHEDULING_DAYS = 14
VI_LAB_DAYS = 10
EVALUATION_AND_REPORTING_DAYS = 10


# =====================================================  de-rounding =========
def _fnv(s):
    h = 2166136261
    for ch in s:
        h = ((h ^ ord(ch)) * 16777619) & 0xFFFFFFFF
    return h


def _jitter(val, key, pct):
    """Deterministic +/- pct variation, to laboratory-realistic precision."""
    f = 1 + ((_fnv(key) % 2001) - 1000) / 1000 * pct
    v = val * f
    if v >= 1000:
        return round(v, -1)
    if v >= 100:
        return round(v)
    if v >= 10:
        return round(v, 1)
    return round(v, 2)


for _k, _hits in SOIL_HITS.items():
    for _a in list(_hits):
        _hits[_a] = _jitter(_hits[_a], f"{_k[0]}{_k[1]}{_a}", 0.06)
for _w, _hits in GW_HITS.items():
    for _a in list(_hits):
        _hits[_a] = _jitter(_hits[_a], f"{_w}{_a}", 0.05)
for _a in list(FIELD_DUP[3]):
    FIELD_DUP[3][_a] = _jitter(FIELD_DUP[3][_a], f"FD01{_a}", 0.04)


# =====================================================  derivations =========
def soil_samples():
    """(sample_id, boring, aoc, top, bottom) for every soil sample, duplicate last."""
    out = []
    for (b, top) in sorted(SOIL_HITS, key=lambda x: (x[0], x[1])):
        aoc = next(x[1] for x in BORINGS if x[0] == b)
        out.append((f"{b}-{top:02d}{top+2:02d}", b, aoc, top, top + 2))
    b, top, sid, _ = FIELD_DUP
    aoc = next(x[1] for x in BORINGS if x[0] == b)
    out.append((sid, b, aoc, top, top + 2))
    return out


def soil_result(sample_id, boring, top, analyte):
    """(value, qualifier, reporting_limit) as the laboratory reported it."""
    rl = SOIL_RL[analyte]
    hits = FIELD_DUP[3] if sample_id == FIELD_DUP[2] else SOIL_HITS.get((boring, top), {})
    if analyte in hits:
        return hits[analyte], "", rl
    return rl, "U", rl


def gw_result(well, analyte):
    rl = GW_RL[analyte]
    hits = GW_HITS.get(well, {})
    if analyte in hits:
        q = "J" if well == HOLDING_TIME_ISSUE and analyte in VOC else ""
        return hits[analyte], q, rl
    q = "UJ" if well == HOLDING_TIME_ISSUE and analyte in VOC else "U"
    return rl, q, rl


def to_mgkg(analyte, value):
    """Laboratory reports soil VOCs in ug/kg; screening levels are mg/kg."""
    return value / 1000.0 if analyte in VOC else value


def blank_qualified(analyte, value_ugkg):
    """True where a detection is attributable to the laboratory method blank."""
    if analyte not in METHOD_BLANK:
        return False
    return value_ugkg < BLANK_RULE_FACTOR * METHOD_BLANK[analyte]


def rpd(a, b):
    return abs(a - b) / ((a + b) / 2) * 100
