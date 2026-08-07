"""
Canonical dataset and applicability calculation for the Cordell Line 4 project.

The rules cited are the fictional Calvert Air Regulation 5, supplied to the
candidate in full as an input file, so the exercise is self-contained and does
not depend on any real published regulation.
"""
FACILITY = "Cordell Specialty Coatings"
LOCATION = "Hollis Junction, Calvert"
FIRM = "Wren & Balfour Environmental Engineering"
AGENCY = "Calvert Division of Air Quality"
AREA_CLASS = "Moderate ozone nonattainment"

# ------------------------------------------------- regulatory thresholds ---
MAJOR_VOC_TPY = 100.0            # PTE at or above which a source is major for VOC
SIGNIFICANT_VOC_TPY = 40.0       # significant net emissions increase
HAP_SINGLE_TPY = 10.0
HAP_AGGREGATE_TPY = 25.0
OFFSET_RATIO = 1.15
FUGITIVES_COUNTED = False        # coatings manufacture is not a listed source category

# ------------------------------------------------------ existing facility --
PERMITTED_VOC_CAP_TPY = 82.0     # federally enforceable synthetic minor limit
FUGITIVE_VOC_TPY = 4.20          # wastewater collection and truck loading
EXISTING_HAP_TPY = {"Xylene": 3.10, "Toluene": 1.80}

# ------------------------------------------------------------- Line 4 -----
L4_DESIGN_GAL_DAY = 420.0
PTE_DAYS_PER_YEAR = 365          # 8,760 hours, absent a federally enforceable limit
CLIENT_STATED_DAYS = 250         # one shift, five days, no permit condition

# Coating data sheet reports both bases; the regulation uses less water.
COATING = dict(name="Cordelan 7300 topcoat",
               voc_as_supplied_lb_gal=2.90,      # including water
               voc_less_water_lb_gal=3.80,
               xylene_less_water_lb_gal=0.62)
CLEANUP = dict(name="Cordelan CS-40 wash solvent", gal_per_month=55.0,
               voc_lb_gal=6.90, toluene_lb_gal=1.10)

# ------------------------------------------------------------ controls ----
RTO_DESTRUCTION = 0.98
RTO_CAPTURE_AS_DESIGNED = 0.92          # partial enclosure with side draft hoods
ENCLOSURE_CAPTURE = 1.00                # permanent total enclosure

# ------------------------------------------- contemporaneous activity -----
LINE2_DEBOTTLENECK = dict(when="2025-08", voc_tpy=6.20, xylene_tpy=0.35,
                          permitted=False)
LINE1_SHUTDOWN = dict(when="2022-04", voc_tpy=-14.0,
                      already_relied_upon="2023 permit revision R-23-0412")

# ---------------------------------------------------------------- costs ---
COSTS = {
    "Permanent total enclosure and ductwork, Line 4": 685000.0,
    "Regenerative thermal oxidiser capacity upsizing": 240000.0,
    "Minor permit revision, dispersion modelling and application": 58000.0,
    "Lowest achievable emission rate control upgrade": 1150000.0,
    "Major source permitting, modelling and application": 185000.0,
}
OFFSET_COST_PER_TON = 9400.0
SCHEDULE_MONTHS = {"minor revision": (4, 5), "major source review": (14, 18)}


# =============================================================== maths =====
def tpy(lb_per_year):
    return lb_per_year / 2000.0


def overall_control(capture):
    return capture * RTO_DESTRUCTION


def line4_coating_uncontrolled_tpy():
    return tpy(L4_DESIGN_GAL_DAY * COATING["voc_less_water_lb_gal"] * PTE_DAYS_PER_YEAR)


def line4_xylene_uncontrolled_tpy():
    return tpy(L4_DESIGN_GAL_DAY * COATING["xylene_less_water_lb_gal"] * PTE_DAYS_PER_YEAR)


def cleanup_voc_tpy():
    return tpy(CLEANUP["gal_per_month"] * CLEANUP["voc_lb_gal"] * 12)


def cleanup_toluene_tpy():
    return tpy(CLEANUP["gal_per_month"] * CLEANUP["toluene_lb_gal"] * 12)


def line4_pte_tpy(capture=RTO_CAPTURE_AS_DESIGNED):
    return (line4_coating_uncontrolled_tpy() * (1 - overall_control(capture))
            + cleanup_voc_tpy())


def line4_xylene_tpy(capture=RTO_CAPTURE_AS_DESIGNED):
    return line4_xylene_uncontrolled_tpy() * (1 - overall_control(capture))


def project_increase_tpy(capture=RTO_CAPTURE_AS_DESIGNED):
    """Line 4 aggregated with the unpermitted Line 2 debottleneck."""
    return line4_pte_tpy(capture) + LINE2_DEBOTTLENECK["voc_tpy"]


def facility_pte_tpy(capture=RTO_CAPTURE_AS_DESIGNED, include_fugitives=False):
    t = PERMITTED_VOC_CAP_TPY + project_increase_tpy(capture)
    return t + (FUGITIVE_VOC_TPY if include_fugitives else 0.0)


def is_major(capture=RTO_CAPTURE_AS_DESIGNED, include_fugitives=False):
    return facility_pte_tpy(capture, include_fugitives) >= MAJOR_VOC_TPY


def hap_after(capture=RTO_CAPTURE_AS_DESIGNED):
    x = EXISTING_HAP_TPY["Xylene"] + line4_xylene_tpy(capture) + LINE2_DEBOTTLENECK["xylene_tpy"]
    t = EXISTING_HAP_TPY["Toluene"] + cleanup_toluene_tpy()
    return {"Xylene": x, "Toluene": t, "Aggregate": x + t}


def capped_throughput_gal_day():
    """Throughput limit needed to stay below the major threshold with the RTO as designed."""
    headroom = (MAJOR_VOC_TPY - 0.1) - PERMITTED_VOC_CAP_TPY - LINE2_DEBOTTLENECK["voc_tpy"]
    coating_allowed = headroom - cleanup_voc_tpy()
    uncontrolled = coating_allowed / (1 - overall_control(RTO_CAPTURE_AS_DESIGNED))
    gal_year = uncontrolled * 2000.0 / COATING["voc_less_water_lb_gal"]
    return gal_year / PTE_DAYS_PER_YEAR


def option_costs():
    inc = project_increase_tpy()
    offsets = inc * OFFSET_RATIO * OFFSET_COST_PER_TON
    major = (COSTS["Lowest achievable emission rate control upgrade"]
             + COSTS["Major source permitting, modelling and application"] + offsets)
    enclosure = (COSTS["Permanent total enclosure and ductwork, Line 4"]
                 + COSTS["Regenerative thermal oxidiser capacity upsizing"]
                 + COSTS["Minor permit revision, dispersion modelling and application"])
    return dict(major=major, offsets=offsets, offset_tons=inc * OFFSET_RATIO,
                enclosure=enclosure, saving=major - enclosure)
