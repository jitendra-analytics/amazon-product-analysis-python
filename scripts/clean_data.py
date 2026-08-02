"""
Amazon Product Analysis
Step 2 : Data Cleaning

Author : Jitendra More
"""

import os
import pandas as pd

print("=" * 60)
print(" AMAZON PRODUCT DATA CLEANING ")
print("=" * 60)

# =====================================
# Create Output Folder
# =====================================

os.makedirs("output", exist_ok=True)

# =====================================
# Load Dataset
# =====================================

DATA_PATH = "data/amazon.csv"

try:
    df = pd.read_csv(DATA_PATH)
    print("\n✅ Dataset Loaded Successfully")

except FileNotFoundError:
    print("\n❌ Dataset not found.")
    exit()

# =====================================
# Original Shape
# =====================================

print("\nOriginal Shape :", df.shape)

# =====================================
# Remove Duplicate Rows
# =====================================

duplicate_rows = df.duplicated().sum()

print("Duplicate Rows :", duplicate_rows)

df = df.drop_duplicates()

# =====================================
# Clean Rating
# =====================================

df["rating"] = pd.to_numeric(
    df["rating"],
    errors="coerce"
)

# =====================================
# Clean Rating Count
# =====================================

df["rating_count"] = (
    df["rating_count"]
    .astype(str)
    .str.replace(",", "", regex=False)
)

df["rating_count"] = pd.to_numeric(
    df["rating_count"],
    errors="coerce"
)

# =====================================
# Clean Discount Percentage
# =====================================

df["discount_percentage"] = (
    df["discount_percentage"]
    .astype(str)
    .str.replace("%", "", regex=False)
)

df["discount_percentage"] = pd.to_numeric(
    df["discount_percentage"],
    errors="coerce"
)

# =====================================
# Clean Discounted Price
# =====================================

df["discounted_price"] = (
    df["discounted_price"]
    .astype(str)
    .str.replace("₹", "", regex=False)
    .str.replace(",", "", regex=False)
)

df["discounted_price"] = pd.to_numeric(
    df["discounted_price"],
    errors="coerce"
)

# =====================================
# Clean Actual Price
# =====================================

df["actual_price"] = (
    df["actual_price"]
    .astype(str)
    .str.replace("₹", "", regex=False)
    .str.replace(",", "", regex=False)
)

df["actual_price"] = pd.to_numeric(
    df["actual_price"],
    errors="coerce"
)

# =====================================
# Missing Values
# =====================================

print("\nMissing Values")
print(df.isnull().sum())

# =====================================
# Remove Missing Values
# =====================================

required_columns = [
    "product_id",
    "product_name",
    "category",
    "rating",
    "rating_count",
    "discount_percentage",
    "discounted_price",
    "actual_price"
]

df = df.dropna(subset=required_columns)

# =====================================
# Remove Duplicate Product IDs
# =====================================

df = df.drop_duplicates(subset="product_id")

# =====================================
# Reset Index
# =====================================

df.reset_index(drop=True, inplace=True)

# =====================================
# Save Clean Dataset
# =====================================

OUTPUT_PATH = "output/cleaned_data.csv"

df.to_csv(
    OUTPUT_PATH,
    index=False
)

# =====================================
# Final Report
# =====================================

print("\nFinal Shape :", df.shape)

print("\nTotal Products :", df["product_id"].nunique())

print("\nClean Dataset Saved Successfully")

print("Location :", OUTPUT_PATH)

print("\n" + "=" * 60)
print(" DATA CLEANING COMPLETED ")
print("=" * 60)