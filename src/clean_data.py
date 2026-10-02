import pandas as pd

INPUT_PATH = "data/raw/packages_dirty.csv"
OUTPUT_PATH = "data/processed/packages_clean.csv"

df = pd.read_csv(INPUT_PATH)

# Remove duplicate package IDs
df = df.drop_duplicates(subset="package_id")

# Standardize provider names
df["provider"] = df["provider"].str.strip().str.title()

# Convert date columns
date_columns = [
    "order_date",
    "ship_date",
    "estimated_delivery_date",
    "actual_delivery_date",
]

for column in date_columns:
    df[column] = pd.to_datetime(df[column], errors="coerce")

# Remove rows with invalid critical values
df = df[df["weight_kg"] > 0]
df = df[df["shipping_cost_usd"] > 0]
df = df[df["delivery_attempts"] > 0]

# Handle missing values
df["destination_province"] = df["destination_province"].fillna("Unknown")

df["weight_kg"] = df["weight_kg"].fillna(
    df["weight_kg"].median()
)

df["shipping_cost_usd"] = df["shipping_cost_usd"].fillna(
    df["shipping_cost_usd"].median()
)

# Remove unrealistic weight outliers
df = df[df["weight_kg"] <= 50]

# Calculate derived metrics
df["delivery_days"] = (
    df["actual_delivery_date"] - df["ship_date"]
).dt.days

df["delay_days"] = (
    df["actual_delivery_date"]
    - df["estimated_delivery_date"]
).dt.days

df["on_time"] = df["delay_days"].le(0).where(
    df["actual_delivery_date"].notna()
)

# Create processed directory and save
import os

os.makedirs("data/processed", exist_ok=True)

df.to_csv(OUTPUT_PATH, index=False)

print(f"Clean dataset created: {OUTPUT_PATH}")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")