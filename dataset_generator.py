import random
import pandas as pd

def generate_boq():
    area = random.randint(800, 3000)
    floors = random.randint(1, 3)
    bedrooms = random.randint(2, 5)
    bathrooms = random.randint(1, min(bedrooms, 3))

    # -------------------------------
    # ROOM TYPES
    # -------------------------------
    kitchen = 1
    hall = 1
    dining = 1 if bedrooms >= 3 else 0
    balcony = floors
    portico = 1 if random.random() > 0.5 else 0

    total_rooms = bedrooms + hall + kitchen + dining
    total_built_up = area * floors

    # -------------------------------
    # NEW FEATURES (🔥)
    # -------------------------------
    building_type = random.choice(["residential", "villa", "apartment"])
    foundation_type = random.choice(["normal", "deep", "pile"])
    location_factor = random.uniform(0.9, 1.3)

    # -------------------------------
    # QUALITY
    # -------------------------------
    quality = random.choice(["budget", "standard", "premium"])

    if quality == "budget":
        rate_per_sqft = random.uniform(1400, 1800)
    elif quality == "standard":
        rate_per_sqft = random.uniform(1800, 2500)
    else:
        rate_per_sqft = random.uniform(2500, 4000)

    expected_total_cost = total_built_up * rate_per_sqft * location_factor

    # -------------------------------
    # CIVIL (with noise 🔥)
    # -------------------------------
    cement     = total_built_up * random.uniform(0.35, 0.45)
    steel      = total_built_up * random.uniform(3.5, 5.5)
    sand       = total_built_up * random.uniform(1.5, 2.5)
    aggregate  = total_built_up * random.uniform(2.0, 3.0)
    bricks     = total_built_up * random.uniform(8, 12)

    # Add randomness (real-world variation)
    def add_noise(x):
        if random.random() < 0.1:
            return x * random.uniform(0.7, 1.3)
        return x * random.uniform(0.9, 1.1)

    cement = round(add_noise(cement))
    steel = round(add_noise(steel))
    sand = round(add_noise(sand))
    aggregate = round(add_noise(aggregate))
    bricks = round(add_noise(bricks))

    # -------------------------------
    # FINISHING
    # -------------------------------
    tiles = round(add_noise(total_built_up * random.uniform(0.85, 1.0)))
    paint = round(add_noise(total_built_up * random.uniform(0.12, 0.18)))
    putty = round(add_noise(total_built_up * random.uniform(0.20, 0.30)))

    # -------------------------------
    # ELECTRICAL
    # -------------------------------
    wiring = round(add_noise(total_built_up * random.uniform(0.6, 0.9)))
    switches = total_rooms * floors * random.randint(6, 10)
    lights = total_rooms * floors * random.randint(4, 6)

    # -------------------------------
    # PLUMBING
    # -------------------------------
    pipes = round(add_noise(bathrooms * random.uniform(70, 110) + area * 0.1))
    bathroom_sets = bathrooms

    # -------------------------------
    # MATERIAL COST
    # -------------------------------
    material_cost = (
        cement * random.uniform(370, 430) +
        steel * random.uniform(62, 78) +
        sand * random.uniform(40, 70) +
        aggregate * random.uniform(38, 55) +
        bricks * random.uniform(7, 11) +
        tiles * random.uniform(55, 120) +
        paint * random.uniform(180, 280) +
        putty * random.uniform(25, 40) +
        wiring * random.uniform(30, 50) +
        switches * random.uniform(80, 200) +
        lights * random.uniform(150, 400) +
        pipes * random.uniform(50, 90) +
        bathroom_sets * random.uniform(18000, 35000)
    )

    # -------------------------------
    # LABOUR
    # -------------------------------
    labor_cost = total_built_up * random.uniform(300, 600)

    # -------------------------------
    # SCALE
    # -------------------------------
    current_total = material_cost + labor_cost
    scale_factor = expected_total_cost / current_total

    material_cost *= scale_factor
    labor_cost *= scale_factor

    total_cost = material_cost + labor_cost

    return [
        area, floors, bedrooms, bathrooms,
        kitchen, hall, dining, balcony, portico,
        building_type, foundation_type, location_factor,
        total_built_up, quality,
        cement, steel, sand, aggregate, bricks,
        tiles, paint, putty,
        wiring, switches, lights,
        pipes, bathroom_sets,
        round(labor_cost), round(total_cost)
    ]


# -------------------------------
# COLUMNS
# -------------------------------
columns = [
    "area_sqft", "floors", "bedrooms", "bathrooms",
    "kitchen", "hall", "dining", "balcony", "portico",
    "building_type", "foundation_type", "location_factor",
    "total_built_up", "quality",
    "cement_bags", "steel_kg", "sand_cft", "aggregate_cft", "bricks",
    "tiles_sqft", "paint_liters", "putty_kg",
    "wiring_meters", "switches", "lights",
    "pipes_meters", "bathroom_sets",
    "labor_cost", "total_cost"
]

data = [generate_boq() for _ in range(100000)]
df = pd.DataFrame(data, columns=columns)

# Encode categorical
df["quality"] = df["quality"].map({"budget": 0, "standard": 1, "premium": 2})
df = pd.get_dummies(df, columns=["building_type", "foundation_type"])

df.to_csv("boq_dataset_v3.csv", index=False)

print("Dataset V3 generated successfully ✅")