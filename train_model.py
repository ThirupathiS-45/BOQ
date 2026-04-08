import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import MinMaxScaler
from xgboost import XGBRegressor
import joblib
import os
import numpy as np

# -----------------------------------------------
# 1. Load Dataset (CPWD V2)
# -----------------------------------------------
DATASET_FILE = "boq_dataset_cpwd_v2.csv"

df = pd.read_csv(DATASET_FILE)
print("Dataset Loaded ✅  Rows:", len(df))


# -----------------------------------------------
# 2. Feature Engineering
# -----------------------------------------------
def add_features(df):
    df = df.copy()

    # Derived
    df["total_built_up"] = df["area_sqft"] * df["floors"]

    # Safe divisions
    df["bedrooms_per_floor"] = df["bedrooms"] / df["floors"].replace(0, 1)
    df["bath_per_bedroom"] = df["bathrooms"] / df["bedrooms"].replace(0, 1)

    # Non-linear (scaled to avoid domination)
    df["area_sq"] = (df["area_sqft"] ** 2) / 1e6

    # Interaction
    df["floors_x_bedrooms"] = df["floors"] * df["bedrooms"]
    df["floors_x_bath"] = df["floors"] * df["bathrooms"]

    # Room composition
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
# 3. Features & Targets (FINAL FIX 🔥)
# -----------------------------------------------
FEATURES = [
    "area_sqft", "floors", "bedrooms", "bathrooms",
    "kitchen", "hall", "dining", "balcony", "portico",
    "total_built_up",
    "bedrooms_per_floor", "bath_per_bedroom",
    "area_sq",
    "floors_x_bedrooms", "floors_x_bath",
    "total_rooms", "rooms_density",
    "quality"
]

TARGETS = [
    "cement_bags", "steel_kg", "sand_cft", "aggregate_cft", "bricks",
    "tiles_sqft", "paint_liters", "putty_kg",
    "wiring_meters", "switches", "lights",
    "pipes_meters", "bathroom_sets",
    "labor_cost"
]

X = df[FEATURES]
y = df[TARGETS]

# Scale targets to [0, 1] to prevent negative predictions
print("\n🔧 Scaling targets for numerical stability...")
target_scalers = {}
y_scaled = y.copy()

for col in TARGETS:
    scaler = MinMaxScaler(feature_range=(0, 1))
    y_scaled[col] = scaler.fit_transform(y[[col]])
    target_scalers[col] = scaler
    print(f"   {col}: min={y[col].min():.0f}, max={y[col].max():.0f}")

y = y_scaled


# -----------------------------------------------
# 4. Train-Test Split
# -----------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Train: {len(X_train):,}   Test: {len(X_test):,}")


# -----------------------------------------------
# 5. MODEL
# -----------------------------------------------
xgb = XGBRegressor(
    n_estimators=300,
    learning_rate=0.1,
    max_depth=6,
    subsample=0.9,
    colsample_bytree=0.9,
    min_child_weight=1,
    gamma=0.0,
    reg_alpha=0.5,
    reg_lambda=1.0,
    tree_method="hist",
    objective="reg:squarederror",
    random_state=42,
    n_jobs=-1,
    base_score=0.5,  # For scaled targets
)

model = MultiOutputRegressor(xgb, n_jobs=1)


# -----------------------------------------------
# 6. Train
# -----------------------------------------------
print("\nTraining started 🚀...\n")

model.fit(X_train, y_train)

print("\nTraining completed ✅")


# -----------------------------------------------
# 7. Evaluate
# -----------------------------------------------
y_pred = model.predict(X_test)

# Inverse scale predictions and targets
y_test_unscaled = y_test.copy()
y_pred_unscaled = y_pred.copy()

for i, col in enumerate(TARGETS):
    scaler = target_scalers[col]
    # Clip predictions to [0, 1] range before inverse transform
    y_pred_unscaled[:, i] = np.clip(y_pred[:, i], 0, 1)
    y_test_unscaled.iloc[:, i] = scaler.inverse_transform(y_test.iloc[:, i].values.reshape(-1, 1)).ravel()
    y_pred_unscaled[:, i] = scaler.inverse_transform(y_pred_unscaled[:, i].reshape(-1, 1)).ravel()

print("\n── Per-target performance ──────────────────────────")
print(f"{'Target':<20} {'MAE':>14} {'R²':>8}")
print("-" * 46)

for i, col in enumerate(TARGETS):
    mae = mean_absolute_error(y_test_unscaled.iloc[:, i], y_pred_unscaled[:, i])
    r2 = r2_score(y_test_unscaled.iloc[:, i], y_pred_unscaled[:, i])
    print(f"{col:<20} {mae:>14,.1f} {r2:>8.4f}")

overall_mae = mean_absolute_error(y_test_unscaled, y_pred_unscaled)
print(f"\nOverall MAE: {overall_mae:,.2f}")


# -----------------------------------------------
# 8. Save Model
# -----------------------------------------------
os.makedirs("model", exist_ok=True)

joblib.dump(
    {
        "model": model,
        "features": FEATURES,
        "targets": TARGETS,
        "target_scalers": target_scalers,  # Save scalers for inference
    },
    "model/boq_model_v3.pkl"
)

print("\nModel saved successfully ✅ → model/boq_model_v3.pkl")