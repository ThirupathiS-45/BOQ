"""
BOQ Dataset Generator — Based on CPWD DAR/DSR 2023
=====================================================
All material rates, labour wages, and quantity coefficients are derived from:
  - CPWD Delhi Analysis of Rates (DAR) 2023, Vol I & II
  - CPWD Delhi Schedule of Rates (DSR) 2023
  - IS 7272 Labour Output Constants

Key corrections over previous version:
  1. No scale_factor hack — labor is computed as % of total (35-40%)
  2. Quality level affects BOTH quantity coefficients AND unit rates
  3. City-based location factors with real city names
  4. CPWD-validated material quantities per sqft
  5. Bathroom count = bedrooms (realistic for Indian residential)
  6. Tile rates split by quality (budget/standard/premium)
  7. No outlier injection (add_noise is ±8% max)
"""

import random
import pandas as pd

# ─────────────────────────────────────────────
# CPWD DAR 2023 BASIC MATERIAL RATES (excl. GST)
# Source: CPWD DAR 2023 Vol I, Sub-Head 0 Basic Rates
# ─────────────────────────────────────────────
CPWD_RATES = {
    # Cement: OPC 43-grade ₹5156/tonne → ₹257.8/50kg bag
    # Market rate ~₹380–430/bag (includes GST + transport)
    "cement_per_bag": {
        "budget":   (360, 400),   # OPC 43 grade
        "standard": (390, 430),   # OPC 53 grade
        "premium":  (420, 460),   # OPC 53 / PPC premium brand
    },
    # Steel: MS round bar ₹5550/quintal → ₹55.5/kg (CPWD basic)
    # TMT Fe-500D market: ₹62–78/kg
    "steel_per_kg": {
        "budget":   (58, 68),
        "standard": (65, 78),
        "premium":  (72, 88),     # Fe-500D TMT premium brand
    },
    # Coarse sand: ₹1450/cum (CPWD code 0982)
    # Convert to cft: 1 cum = 35.31 cft → ₹41/cft
    "sand_per_cft": {
        "budget":   (35, 50),
        "standard": (45, 65),
        "premium":  (55, 75),     # M-sand or washed river sand
    },
    # Stone aggregate 20mm: ₹1100/cum (CPWD code 0291)
    # Per cft: ₹31/cft
    "aggregate_per_cft": {
        "budget":   (28, 40),
        "standard": (38, 52),
        "premium":  (48, 62),
    },
    # Bricks: ₹4750/1000 nos (CPWD code 1984, class designation 10)
    # ₹4.75/brick basic; market ₹8–14/brick
    "brick_per_nos": {
        "budget":   (7, 10),      # Class 7.5 fly ash bricks
        "standard": (9, 13),      # Class 10 burnt clay
        "premium":  (12, 18),     # Class 12.5 modular or AAC blocks
    },
    # Floor tiles per sqft
    # Budget: ceramic ₹40–80/sqft, Standard: vitrified ₹80–180/sqft
    # Premium: large format/imported ₹180–500/sqft
    "tile_per_sqft": {
        "budget":   (40,  80),
        "standard": (80,  180),
        "premium":  (180, 500),
    },
    # Paint: emulsion paint per litre
    # CPWD DAR: distemper ~₹80/litre, OBD ~₹120/litre
    # Market: economy ₹120–180, premium ₹280–600/litre
    "paint_per_litre": {
        "budget":   (120, 180),
        "standard": (200, 320),
        "premium":  (320, 600),   # Asian Paints Royale / premium brand
    },
    # Putty per kg
    "putty_per_kg": {
        "budget":   (22, 32),
        "standard": (30, 42),
        "premium":  (40, 60),
    },
    # Wiring (PVC conduit + wire) per metre
    # CPWD DSR electrical: point wiring ~₹350–600/point
    # Convert to per-metre: ₹35–80/metre
    "wiring_per_metre": {
        "budget":   (32, 48),
        "standard": (45, 65),
        "premium":  (60, 90),
    },
    # Modular switches per nos
    "switch_per_nos": {
        "budget":   (80,  150),
        "standard": (150, 280),
        "premium":  (280, 600),
    },
    # Light fixtures per nos (basic fitting)
    "light_per_nos": {
        "budget":   (150, 300),
        "standard": (300, 600),
        "premium":  (600, 2000),
    },
    # CPVC/GI pipes per metre
    "pipe_per_metre": {
        "budget":   (55,  90),
        "standard": (80,  130),
        "premium":  (120, 200),
    },
    # Bathroom sets (sanitary fixtures complete)
    # CPWD DSR 2023: Euro WC ₹10250/set (basic vitreous)
    # Budget full set: ₹18k–35k, Standard: ₹35k–80k, Premium: ₹80k–2L
    "bathroom_per_set": {
        "budget":   (18000,  35000),
        "standard": (35000,  80000),
        "premium":  (80000,  200000),
    },
}

# ─────────────────────────────────────────────
# CPWD-BASED LABOUR RATES (DAR 2023, April 2023)
# Mason (avg): ₹857/day, Beldar/Coolie: ₹736/day, Bhisti: ₹816/day
# Market rates for private residential are 20–40% higher
# Labour = 35–40% of total project cost (IS standard)
# ─────────────────────────────────────────────
LABOUR_PCT = {
    "budget":   (0.32, 0.38),
    "standard": (0.34, 0.40),
    "premium":  (0.36, 0.42),
}

# ─────────────────────────────────────────────
# QUALITY-WISE RATE PER SQFT (built-up area)
# Based on CPWD Plinth Area Rates + market analysis 2024
# ─────────────────────────────────────────────
RATE_PER_SQFT = {
    "budget":   (1400, 1800),
    "standard": (1800, 2500),
    "premium":  (2600, 4200),
}

# ─────────────────────────────────────────────
# CITY-BASED LOCATION FACTORS (real market data)
# Base = Delhi (CPWD reference city = 1.0)
# ─────────────────────────────────────────────
CITY_FACTORS = {
    "Mumbai":    1.55,
    "Delhi":     1.00,
    "Bangalore": 1.20,
    "Chennai":   1.10,
    "Hyderabad": 1.05,
    "Pune":      1.15,
    "Kolkata":   0.95,
    "Ahmedabad": 0.90,
    "Tier2":     0.85,   # Jaipur, Lucknow, Nagpur etc.
    "Tier3":     0.75,   # Smaller cities
    "Rural":     0.65,
}

# ─────────────────────────────────────────────
# QUANTITY COEFFICIENTS PER SQFT (CPWD thumb rules)
# Source: CPWD DAR + IS 7272 material consumption norms
# ─────────────────────────────────────────────
# Civil quantities per sqft of total built-up area
CIVIL_COEFF = {
    # Cement bags per sqft (includes RCC, masonry, plaster, flooring)
    "cement": {
        "budget":   (0.38, 0.44),
        "standard": (0.40, 0.46),
        "premium":  (0.42, 0.50),
    },
    # Steel kg per sqft (Fe-500D TMT)
    # CPWD: ~4–4.5 kg/sqft for standard residential RCC
    "steel": {
        "budget":   (3.5,  4.2),
        "standard": (4.0,  4.8),
        "premium":  (4.5,  5.5),
    },
    # Sand cft per sqft
    "sand": {
        "budget":   (1.6, 2.2),
        "standard": (1.8, 2.4),
        "premium":  (2.0, 2.6),
    },
    # Aggregate cft per sqft
    "aggregate": {
        "budget":   (1.8, 2.4),
        "standard": (2.0, 2.6),
        "premium":  (2.2, 2.8),
    },
    # Bricks per sqft (includes all masonry)
    # CPWD: ~8–10 bricks/sqft for half-brick walls
    "bricks": {
        "budget":   (8,  10),
        "standard": (9,  11),
        "premium":  (10, 13),
    },
}

# Finishing quantities per sqft of built-up area
FINISH_COEFF = {
    # Tiles sqft: ~90–100% of built-up (floor area only)
    "tiles": {
        "budget":   (0.88, 0.95),
        "standard": (0.90, 0.97),
        "premium":  (0.92, 1.00),
    },
    # Paint litres per sqft (walls + ceiling, 2 coats)
    # ~0.14–0.18 litre/sqft
    "paint": {
        "budget":   (0.12, 0.16),
        "standard": (0.14, 0.18),
        "premium":  (0.16, 0.22),
    },
    # Putty kg per sqft
    "putty": {
        "budget":   (0.18, 0.24),
        "standard": (0.20, 0.26),
        "premium":  (0.22, 0.30),
    },
}

# Electrical quantities
ELEC_COEFF = {
    # Wiring metres per sqft
    "wiring": {
        "budget":   (0.55, 0.70),
        "standard": (0.65, 0.80),
        "premium":  (0.75, 1.00),
    },
    # Switches per room per floor: 6–10 nos
    "switches_per_room": {
        "budget":   (5, 7),
        "standard": (6, 9),
        "premium":  (8, 12),
    },
    # Lights per room per floor
    "lights_per_room": {
        "budget":   (3, 5),
        "standard": (4, 6),
        "premium":  (5, 8),
    },
}


def add_noise(x, pct=0.08):
    """Realistic ±8% noise, no outliers"""
    return x * random.uniform(1 - pct, 1 + pct)


def get_rate(rate_dict, quality):
    lo, hi = rate_dict[quality]
    return random.uniform(lo, hi)


def generate_boq():
    # ── Project parameters ──
    area        = random.randint(600, 3000)      # plot/carpet area sqft
    floors      = random.randint(1, 3)
    bedrooms    = random.randint(2, 5)
    # CPWD/real-world: bathrooms = bedrooms for residential
    bathrooms   = bedrooms if random.random() > 0.3 else max(1, bedrooms - 1)
    kitchen     = 1
    hall        = 1
    dining      = 1 if bedrooms >= 3 else 0
    balcony     = floors
    portico     = 1 if random.random() > 0.5 else 0
    total_rooms = bedrooms + hall + kitchen + dining

    building_type   = random.choice(["residential", "villa", "apartment"])
    foundation_type = random.choice(["normal", "deep", "pile"])
    quality         = random.choice(["budget", "standard", "premium"])

    city            = random.choice(list(CITY_FACTORS.keys()))
    location_factor = CITY_FACTORS[city] * random.uniform(0.96, 1.04)  # ±4% local variation

    total_built_up  = area * floors   # sqft

    # ── Civil quantities (CPWD coefficients) ──
    cement    = total_built_up * get_rate(CIVIL_COEFF["cement"],    quality)
    steel     = total_built_up * get_rate(CIVIL_COEFF["steel"],     quality)
    sand      = total_built_up * get_rate(CIVIL_COEFF["sand"],      quality)
    aggregate = total_built_up * get_rate(CIVIL_COEFF["aggregate"], quality)
    bricks    = total_built_up * get_rate(CIVIL_COEFF["bricks"],    quality)

    cement    = round(add_noise(cement))
    steel     = round(add_noise(steel))
    sand      = round(add_noise(sand))
    aggregate = round(add_noise(aggregate))
    bricks    = round(add_noise(bricks))

    # ── Finishing quantities ──
    tiles = round(add_noise(total_built_up * get_rate(FINISH_COEFF["tiles"], quality)))
    paint = round(add_noise(total_built_up * get_rate(FINISH_COEFF["paint"], quality)))
    putty = round(add_noise(total_built_up * get_rate(FINISH_COEFF["putty"], quality)))

    # ── Electrical quantities ──
    wiring   = round(add_noise(total_built_up * get_rate(ELEC_COEFF["wiring"], quality)))
    switches = total_rooms * floors * random.randint(*ELEC_COEFF["switches_per_room"][quality])
    lights   = total_rooms * floors * random.randint(*ELEC_COEFF["lights_per_room"][quality])

    # ── Plumbing quantities ──
    # Pipes: ~70–110 metres per bathroom + 0.08 sqft factor for distribution
    pipes         = round(add_noise(bathrooms * random.uniform(70, 110) + area * 0.08))
    bathroom_sets = bathrooms

    # ── Material cost (CPWD-based unit rates, quality-differentiated) ──
    material_cost = (
        cement        * get_rate(CPWD_RATES["cement_per_bag"],     quality) +
        steel         * get_rate(CPWD_RATES["steel_per_kg"],       quality) +
        sand          * get_rate(CPWD_RATES["sand_per_cft"],       quality) +
        aggregate     * get_rate(CPWD_RATES["aggregate_per_cft"],  quality) +
        bricks        * get_rate(CPWD_RATES["brick_per_nos"],      quality) +
        tiles         * get_rate(CPWD_RATES["tile_per_sqft"],      quality) +
        paint         * get_rate(CPWD_RATES["paint_per_litre"],    quality) +
        putty         * get_rate(CPWD_RATES["putty_per_kg"],       quality) +
        wiring        * get_rate(CPWD_RATES["wiring_per_metre"],   quality) +
        switches      * get_rate(CPWD_RATES["switch_per_nos"],     quality) +
        lights        * get_rate(CPWD_RATES["light_per_nos"],      quality) +
        pipes         * get_rate(CPWD_RATES["pipe_per_metre"],     quality) +
        bathroom_sets * get_rate(CPWD_RATES["bathroom_per_set"],   quality)
    )

    # Apply location factor to material cost
    material_cost *= location_factor

    # ── Labour cost (35–40% of total — CPWD/IS norm, NOT a flat per-sqft) ──
    # labour_pct = labour / (material + labour)
    # => labour = material_cost * labour_pct / (1 - labour_pct)
    labour_pct  = random.uniform(*LABOUR_PCT[quality])
    labour_cost = material_cost * (labour_pct / (1 - labour_pct))
    labour_cost *= location_factor   # city-adjust labour too

    total_cost  = material_cost + labour_cost

    # ── Sanity check: align with CPWD Plinth Area Rate band ──
    # If computed total deviates >30% from expected sqft band, clip gently
    lo_rate, hi_rate = RATE_PER_SQFT[quality]
    expected_lo = total_built_up * lo_rate * location_factor
    expected_hi = total_built_up * hi_rate * location_factor
    if total_cost < expected_lo * 0.80:
        total_cost = expected_lo * random.uniform(0.85, 1.0)
        material_cost = total_cost * (1 - labour_pct)
        labour_cost   = total_cost * labour_pct
    elif total_cost > expected_hi * 1.20:
        total_cost = expected_hi * random.uniform(1.0, 1.15)
        material_cost = total_cost * (1 - labour_pct)
        labour_cost   = total_cost * labour_pct

    quality_encoded = {"budget": 0, "standard": 1, "premium": 2}[quality]

    return [
        area, floors, bedrooms, bathrooms,
        kitchen, hall, dining, balcony, portico,
        building_type, foundation_type,
        city, round(location_factor, 3),
        total_built_up, quality_encoded,
        cement, steel, sand, aggregate, bricks,
        tiles, paint, putty,
        wiring, switches, lights,
        pipes, bathroom_sets,
        round(material_cost),
        round(labour_cost),
        round(total_cost),
    ]


# ─────────────────────────────────────────────
# COLUMNS
# ─────────────────────────────────────────────
columns = [
    "area_sqft", "floors", "bedrooms", "bathrooms",
    "kitchen", "hall", "dining", "balcony", "portico",
    "building_type", "foundation_type",
    "city", "location_factor",
    "total_built_up", "quality",          # quality: 0=budget,1=standard,2=premium
    "cement_bags", "steel_kg", "sand_cft", "aggregate_cft", "bricks",
    "tiles_sqft", "paint_liters", "putty_kg",
    "wiring_meters", "switches", "lights",
    "pipes_meters", "bathroom_sets",
    "material_cost",
    "labor_cost",
    "total_cost",
]

if __name__ == "__main__":
    import time
    print("Generating 100,000 rows based on CPWD DAR/DSR 2023...")
    t0 = time.time()

    data = [generate_boq() for _ in range(100_000)]
    df   = pd.DataFrame(data, columns=columns)

    # One-hot encode categoricals
    df = pd.get_dummies(df, columns=["building_type", "foundation_type", "city"])

    df.to_csv("boq_dataset_cpwd_v2.csv", index=False)

    elapsed = time.time() - t0
    print(f"Done in {elapsed:.1f}s  →  boq_dataset_cpwd_v2.csv")
    print(f"Shape: {df.shape}")
    print("\nSample stats:")
    print(df[["total_built_up","material_cost","labor_cost","total_cost"]].describe().to_string())

    # Quick sanity: labor % distribution
    df["labor_pct"] = df["labor_cost"] / df["total_cost"] * 100
    print(f"\nLabour % — mean: {df['labor_pct'].mean():.1f}%  "
          f"min: {df['labor_pct'].min():.1f}%  "
          f"max: {df['labor_pct'].max():.1f}%")
