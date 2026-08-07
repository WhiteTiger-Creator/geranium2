"""Screening, data qualification and remedial costing -- the golden solution's arithmetic."""
import sys, os
from datetime import timedelta
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import site_data as s

ANALYTES = s.VOC + s.MET

# ---------------------------------------------------------------------------
# 1. APPLICABLE CRITERIA
#    Planned use is warehouse/light industrial and the buyer will accept an
#    activity and use limitation, so industrial direct-contact levels apply.
#    The soil-to-groundwater pathway is not land-use dependent and applies
#    regardless. The aquifer is not a drinking water source, so GW-1 does not
#    apply; GW-2 (vapour) and GW-3 (discharge) do.
# ---------------------------------------------------------------------------
SOIL_DC_INDEX = 1          # 0 = residential, 1 = industrial
GW_APPLICABLE = (1, 2)     # GW-2 and GW-3; GW-1 excluded


def soil_criteria(a):
    res, ind, s2g = s.SOIL_SL[a]
    return (ind if SOIL_DC_INDEX else res), s2g


def gw_criteria(a):
    g1, g2, g3 = s.GW_SL[a]
    vals = [v for i, v in enumerate((g1, g2, g3)) if i in GW_APPLICABLE and v is not None]
    return min(vals) if vals else None


# ---------------------------------------------------------------------------
# 2. DATA QUALIFICATION
# ---------------------------------------------------------------------------
def qualify_soil(sample_id, boring, top, analyte):
    """Returns (value_mgkg, usable, reason). Value None where rejected."""
    val, qual, rl = s.soil_result(sample_id, boring, top, analyte)
    if qual == "U":
        mg = s.to_mgkg(analyte, rl)
        dc, s2g = soil_criteria(analyte)
        if mg > min(dc, s2g):
            return None, False, f"non-detect, but the reporting limit of {mg:g} mg/kg exceeds the criterion"
        return 0.0, True, "non-detect"
    if s.blank_qualified(analyte, val):
        return 0.0, True, (f"detection below {s.BLANK_RULE_FACTOR} times the method blank "
                           f"({s.METHOD_BLANK[analyte]:g} ug/kg); qualified as non-detect")
    return s.to_mgkg(analyte, val), True, ""


def soil_exceedances():
    out = []
    for sid, b, aoc, top, bot in s.soil_samples():
        for a in ANALYTES:
            mg, usable, reason = qualify_soil(sid, b, top, a)
            dc, s2g = soil_criteria(a)
            if not usable:
                out.append(dict(sample=sid, boring=b, aoc=aoc, top=top, analyte=a,
                                value=None, dc=dc, s2g=s2g, kind="indeterminate", note=reason))
                continue
            if mg == 0.0:
                continue
            paths = []
            if mg > dc:
                paths.append("direct contact")
            if mg > s2g:
                paths.append("soil-to-groundwater")
            if not paths:
                continue
            if a == "Arsenic" and mg <= s.ARSENIC_BACKGROUND[1]:
                out.append(dict(sample=sid, boring=b, aoc=aoc, top=top, analyte=a, value=mg,
                                dc=dc, s2g=s2g, kind="background",
                                note=f"within the regional background range of "
                                     f"{s.ARSENIC_BACKGROUND[0]:g} to {s.ARSENIC_BACKGROUND[1]:g} mg/kg"))
                continue
            out.append(dict(sample=sid, boring=b, aoc=aoc, top=top, analyte=a, value=mg,
                            dc=dc, s2g=s2g, kind=" and ".join(paths), note=""))
    return out


def gw_exceedances():
    out = []
    for w, aoc, _ in s.WELLS:
        for a in ANALYTES:
            val, qual, rl = s.gw_result(w, a)
            crit = gw_criteria(a)
            if crit is None or qual.startswith("U"):
                continue
            if val > crit:
                out.append(dict(well=w, aoc=aoc, analyte=a, value=val, crit=crit, qual=qual))
    return out


# ---------------------------------------------------------------------------
# 3. REMEDIAL FOOTPRINT AND COST
# ---------------------------------------------------------------------------
# Excavation is limited to 8 ft below grade in AOC-1 and AOC-2 and 10 ft in
# AOC-3; the water table is first encountered at roughly 10 to 10.5 ft, so
# deeper impact is addressed through the use limitation and monitoring rather
# than removal.
EXCAVATION = {"AOC-1": (2, 8), "AOC-2": (2, 8), "AOC-3": (4, 10)}


def volumes():
    rows = []
    for aoc, (top, bot) in EXCAVATION.items():
        area = s.AOC[aoc]["area_sf"]
        cy = area * (bot - top) / 27.0
        rows.append(dict(aoc=aoc, name=s.AOC[aoc]["name"], area=area, top=top, bot=bot,
                         thickness=bot - top, cy=cy, tons=cy * s.SOIL_DENSITY))
    return rows


def unit(name):
    return next(u[2] for u in s.UNIT_COSTS if u[0].startswith(name))


def cost_estimate(include_ssd=False):
    v = volumes()
    cy = sum(r["cy"] for r in v)
    tons = sum(r["tons"] for r in v)
    items = [
        ("Mobilisation and demobilisation", "1 LS", unit("Mobilisation"), unit("Mobilisation")),
        ("Excavation, load and haul preparation", f"{cy:,.0f} CY", unit("Excavation"), cy * unit("Excavation")),
        ("Transport and disposal, non-hazardous industrial soil", f"{tons:,.0f} TON",
         unit("Transport and disposal, non-haz"), tons * unit("Transport and disposal, non-haz")),
        ("Certified clean backfill, supplied and placed", f"{cy:,.0f} CY", unit("Certified"), cy * unit("Certified")),
        ("Confirmation sampling and laboratory analysis", f"{s.CONFIRMATION_SETS} EA",
         unit("Confirmation"), s.CONFIRMATION_SETS * unit("Confirmation")),
        ("Dewatering, treatment and discharge", "1 LS", unit("Dewatering"), unit("Dewatering")),
        ("Engineering oversight, air monitoring and completion report", "1 LS",
         unit("Engineering"), unit("Engineering")),
        ("Activity and use limitation", "1 LS", unit("Activity"), unit("Activity")),
        ("Vapour intrusion evaluation", "1 LS", unit("Vapour"), unit("Vapour")),
        ("Quarterly groundwater monitoring, four wells",
         f"{s.MONITORING_ROUNDS} RND", unit("Quarterly"), s.MONITORING_ROUNDS * unit("Quarterly")),
    ]
    if include_ssd:
        items.append(("Sub-slab depressurisation system, design and installation", "1 LS",
                      unit("Sub-slab"), unit("Sub-slab")))
    sub = sum(i[3] for i in items)
    return items, sub, sub * s.CONTINGENCY, sub * (1 + s.CONTINGENCY)


# ---------------------------------------------------------------------------
# 4. SCHEDULE
# ---------------------------------------------------------------------------
def schedule():
    reanalysis = s.REANALYSIS_BUSINESS_DAYS * 7 // 5
    vi = s.VI_SCHEDULING_DAYS + s.VI_LAB_DAYS
    critical = max(reanalysis, vi) + s.EVALUATION_AND_REPORTING_DAYS
    finish = s.ASSIGNMENT_DATE + timedelta(days=critical)
    available = (s.DD_EXPIRY - s.ASSIGNMENT_DATE).days
    return dict(reanalysis=reanalysis, vi=vi, critical=critical, finish=finish,
                available=available, shortfall=critical - available)


if __name__ == "__main__":
    print("=" * 100)
    print("APPLICABLE CRITERIA")
    print("=" * 100)
    print("  Soil direct contact  : industrial (planned warehouse use, AUL accepted)")
    print("  Soil leaching        : soil-to-groundwater, applies regardless of land use")
    print("  Groundwater          : GW-2 and GW-3; GW-1 excluded, aquifer is not a drinking water source")

    print("\n" + "=" * 100)
    print("SOIL SCREENING")
    print("=" * 100)
    ex = soil_exceedances()
    real = [e for e in ex if e["kind"] not in ("background", "indeterminate")]
    print(f"{'Sample':14} {'AOC':7} {'Analyte':26} {'Result':>10} {'DC':>8} {'S2GW':>8}  Pathway")
    for e in sorted(real, key=lambda x: (x["aoc"], x["sample"], x["analyte"])):
        print(f"{e['sample']:14} {e['aoc']:7} {e['analyte']:26} {e['value']:10.3g} "
              f"{e['dc']:8g} {e['s2g']:8g}  {e['kind']}")
    print(f"\n  exceedances: {len(real)}  |  distinct analytes: "
          f"{sorted({e['analyte'] for e in real})}")
    print(f"  AOCs affected: {sorted({e['aoc'] for e in real})}")

    print("\n  SET ASIDE:")
    for e in ex:
        if e["kind"] == "background":
            print(f"    {e['sample']:12} {e['analyte']:20} {e['value']:8.3g} mg/kg  {e['note']}")
    for e in ex:
        if e["kind"] == "indeterminate":
            print(f"    {e['sample']:12} {e['analyte']:20} {'':8}  {e['note']}")

    print("\n  BLANK-QUALIFIED DETECTIONS (methylene chloride):")
    for sid, b, aoc, top, bot in s.soil_samples():
        v, q, rl = s.soil_result(sid, b, top, "Methylene chloride")
        if not q and s.blank_qualified("Methylene chloride", v):
            print(f"    {sid:12} {v:8g} ug/kg  <  {s.BLANK_RULE_FACTOR}x blank "
                  f"({s.BLANK_RULE_FACTOR*s.METHOD_BLANK['Methylene chloride']:g} ug/kg)"
                  f"  -- would otherwise exceed the {s.SOIL_SL['Methylene chloride'][2]*1000:g} ug/kg leaching value")

    b, top, sid, vals = s.FIELD_DUP
    print(f"\n  FIELD DUPLICATE {sid} vs {b} ({top}-{top+2} ft):")
    for a, dv in vals.items():
        pv = s.SOIL_HITS[(b, top)].get(a)
        if pv:
            r = s.rpd(pv, dv)
            print(f"    {a:20} parent {pv:8g}  dup {dv:8g}  RPD {r:5.1f}%"
                  f"{'   EXCEEDS ' + str(s.DUP_RPD_LIMIT) + '%' if r > s.DUP_RPD_LIMIT else ''}")

    print("\n" + "=" * 100)
    print("GROUNDWATER SCREENING")
    print("=" * 100)
    for e in gw_exceedances():
        print(f"  {e['well']:7} {e['analyte']:26} {e['value']:9g} ug/L  >  {e['crit']:g} ug/L"
              f"  {'(estimated, holding time)' if e['qual'] else ''}")
    print(f"\n  If GW-1 had been applied in error, these would also appear:")
    for w, aoc, _ in s.WELLS:
        for a in ANALYTES:
            val, q, rl = s.gw_result(w, a)
            if q.startswith("U"):
                continue
            g1 = s.GW_SL[a][0]
            if val > g1 and val <= (gw_criteria(a) or 1e9):
                print(f"    {w:7} {a:26} {val:9g} ug/L  >  GW-1 {g1:g} ug/L  but below the applicable criterion")

    print("\n" + "=" * 100)
    print("TCLP")
    print("=" * 100)
    for (b, top), v in s.TCLP.items():
        print(f"  {b} {top}-{top+2} ft: lead {v:g} mg/L  vs  RCRA limit {s.TCLP_LIMIT:g} mg/L"
              f"  ->  {'HAZARDOUS' if v >= s.TCLP_LIMIT else 'non-hazardous, disposal at the lower rate'}")

    print("\n" + "=" * 100)
    print("REMEDIAL FOOTPRINT AND COST")
    print("=" * 100)
    for r in volumes():
        print(f"  {r['aoc']}  {r['area']:5,} sf x {r['thickness']} ft ({r['top']}-{r['bot']} ft bgs)"
              f"  = {r['cy']:8,.1f} CY  = {r['tons']:8,.1f} tons")
    v = volumes()
    print(f"  {'TOTAL':7} {'':5}                             "
          f"  = {sum(r['cy'] for r in v):8,.1f} CY  = {sum(r['tons'] for r in v):8,.1f} tons")
    items, sub, cont, tot = cost_estimate()
    print()
    for name, qty, rate, amt in items:
        print(f"    {name:60} {qty:>12} {amt:12,.0f}")
    print(f"    {'Subtotal':60} {'':>12} {sub:12,.0f}")
    print(f"    {'Contingency at 20%':60} {'':>12} {cont:12,.0f}")
    print(f"    {'TOTAL, recommended remedy':60} {'':>12} {tot:12,.0f}")
    _, sub2, _, tot2 = cost_estimate(include_ssd=True)
    print(f"    {'TOTAL if vapour mitigation proves necessary':60} {'':>12} {tot2:12,.0f}")
    print(f"\n  PSA environmental escrow cap: {s.ESCROW_CAP:,.0f}")
    print(f"  Shortfall against the cap    : {tot - s.ESCROW_CAP:,.0f}"
          f"  ({tot/s.ESCROW_CAP - 1:.0%} over)")
    print(f"  Shortfall with mitigation    : {tot2 - s.ESCROW_CAP:,.0f}")

    print("\n" + "=" * 100)
    print("SCHEDULE")
    print("=" * 100)
    sc = schedule()
    print(f"  Vinyl chloride re-analysis at a lower reporting limit : {sc['reanalysis']} calendar days")
    print(f"  Vapour intrusion sampling and laboratory turnaround   : {sc['vi']} calendar days")
    print(f"  Evaluation and reporting                             : {s.EVALUATION_AND_REPORTING_DAYS} days")
    print(f"  Critical path from {s.ASSIGNMENT_DATE}                      : {sc['critical']} days, "
          f"finishing {sc['finish']}")
    print(f"  Due diligence period available                       : {sc['available']} days, "
          f"expiring {s.DD_EXPIRY}")
    print(f"  SHORTFALL                                            : {sc['shortfall']} days")
