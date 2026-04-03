import joblib
import pandas as pd

# -----------------------------------------------
# 1. Load Model
# -----------------------------------------------
bundle = joblib.load("model/boq_model_v3.pkl")

model = bundle["model"]
FEATURES = bundle["features"]
TARGETS = bundle["targets"]

print("Model Loaded ✅")


# -----------------------------------------------
# 2. USER INPUT (EDIT HERE 🔥)
# -----------------------------------------------
input_data = {
    "area_sqft": 1200,
    "floors": 2,
    "bedrooms": 3,
    "bathrooms": 2,
    "kitchen": 1,
    "hall": 1,
    "dining": 1,
    "balcony": 2,
    "portico": 1,
    "quality": 1   # 0=budget, 1=standard, 2=premium
}


# -----------------------------------------------
# 3. Convert to DataFrame
# -----------------------------------------------
df = pd.DataFrame([input_data])


# -----------------------------------------------
# 4. Feature Engineering (SAME AS TRAINING)
# -----------------------------------------------
def add_features(df):
    df = df.copy()

    df["total_built_up"] = df["area_sqft"] * df["floors"]

    df["bedrooms_per_floor"] = df["bedrooms"] / df["floors"]
    df["bath_per_bedroom"] = df["bathrooms"] / df["bedrooms"]

    df["area_sq"] = (df["area_sqft"] ** 2) / 1e6

    df["floors_x_bedrooms"] = df["floors"] * df["bedrooms"]
    df["floors_x_bath"] = df["floors"] * df["bathrooms"]

    df["total_rooms"] = (
        df["bedrooms"] +
        df["kitchen"] +
        df["hall"] +
        df["dining"]
    )

    df["rooms_density"] = df["total_rooms"] / df["area_sqft"]

    return df


df = add_features(df)


# -----------------------------------------------
# 5. Align Features
# -----------------------------------------------
for col in FEATURES:
    if col not in df.columns:
        df[col] = 0

df = df[FEATURES]


# -----------------------------------------------
# 6. Predict
# -----------------------------------------------
pred = model.predict(df)[0]


# -----------------------------------------------
# 7. Format Output
# -----------------------------------------------
results = dict(zip(TARGETS, pred))

labor_cost = results["labor_cost"]
materials_cost = (
    results["cement_bags"] * 400 +
    results["steel_kg"] * 70 +
    results["sand_cft"] * 60 +
    results["aggregate_cft"] * 50 +
    results["bricks"] * 9 +
    results["tiles_sqft"] * 80 +
    results["paint_liters"] * 220 +
    results["putty_kg"] * 30 +
    results["wiring_meters"] * 40 +
    results["switches"] * 120 +
    results["lights"] * 250 +
    results["pipes_meters"] * 70 +
    results["bathroom_sets"] * 25000
)
total_cost = labor_cost + materials_cost


# -----------------------------------------------
# 8. Print Output (🔥 CLEAN)
# -----------------------------------------------
print("\n====== 🏗️ BOQ ESTIMATION ======\n")

for k, v in results.items():
    print(f"{k:<20}: {round(v):,}")

print("\n------ 💰 COST SUMMARY ------")
print(f"Material Cost      : ₹{round(materials_cost):,}")
print(f"Labor Cost         : ₹{round(labor_cost):,}")
print(f"Total Cost         : ₹{round(total_cost):,}")

print("\n================================\n")