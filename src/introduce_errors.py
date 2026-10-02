import pandas as pd
import numpy as np

INPUT_PATH = "data/raw/packages.csv"
OUTPUT_PATH = "data/raw/packages_dirty.csv"

rng = np.random.default_rng(42)

df = pd.read_csv(INPUT_PATH)

# Missing values
for column in ["weight_kg", "shipping_cost_usd", "destination_province"]:
    indexes = rng.choice(len(df), size=20, replace=False)
    df.loc[indexes, column] = None

# Duplicate package IDs
duplicate_indexes = rng.choice(
    np.arange(100, len(df)),
    size=20,
    replace=False
)

for index in duplicate_indexes:
    df.loc[index, "package_id"] = df.loc[index - 1, "package_id"]

# Invalid weights
indexes = rng.choice(len(df), size=15, replace=False)
df.loc[indexes, "weight_kg"] = -5

# Invalid shipping costs
indexes = rng.choice(len(df), size=15, replace=False)
df.loc[indexes, "shipping_cost_usd"] = 0

# Invalid delivery attempts
indexes = rng.choice(len(df), size=15, replace=False)
df.loc[indexes, "delivery_attempts"] = 0

# Inconsistent dates
indexes = rng.choice(len(df), size=15, replace=False)
df.loc[indexes, "actual_delivery_date"] = df.loc[indexes, "ship_date"]

# Inconsistent provider names
indexes = rng.choice(len(df), size=30, replace=False)

df.loc[indexes[:15], "provider"] = "amazon "
df.loc[indexes[15:], "provider"] = "temu"

# Weight outliers
indexes = rng.choice(len(df), size=10, replace=False)
df.loc[indexes, "weight_kg"] = 150

df.to_csv(OUTPUT_PATH, index=False)

print(f"Dirty dataset created: {OUTPUT_PATH}")