"""
Amazon Product Data Analysis
Step 1: Load Dataset

Author: Jitendra More
"""

import os
import sys
import pandas as pd


# ============================================================
# 1. PROJECT PATHS
# ============================================================

DATA_PATH = os.path.join("data", "amazon.csv")
OUTPUT_DIR = "output"
CHARTS_DIR = os.path.join(OUTPUT_DIR, "charts")
REPORTS_DIR = os.path.join(OUTPUT_DIR, "reports")


# ============================================================
# 2. CREATE OUTPUT FOLDERS
# ============================================================

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(CHARTS_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)


# ============================================================
# 3. PROJECT HEADER
# ============================================================

print("=" * 70)
print("AMAZON PRODUCT DATA ANALYSIS")
print("STEP 1: LOAD DATASET")
print("=" * 70)


# ============================================================
# 4. CHECK DATASET
# ============================================================

if not os.path.exists(DATA_PATH):
    print(f"\n❌ ERROR: Dataset not found at: {DATA_PATH}")
    print("Please place amazon.csv inside the data folder.")
    sys.exit(1)


# ============================================================
# 5. LOAD DATASET
# ============================================================

try:
    df = pd.read_csv(DATA_PATH)

except Exception as error:
    print("\n❌ ERROR: Unable to load dataset.")
    print("Reason:", error)
    sys.exit(1)


print("\n✅ Dataset Loaded Successfully")
print(f"Location : {DATA_PATH}")


# ============================================================
# 6. DATASET SIZE
# ============================================================

rows, columns = df.shape

print("\n" + "-" * 70)
print("DATASET SIZE")
print("-" * 70)

print(f"Rows    : {rows:,}")
print(f"Columns : {columns}")


# ============================================================
# 7. COLUMN NAMES
# ============================================================

print("\n" + "-" * 70)
print("COLUMN NAMES")
print("-" * 70)

for number, column in enumerate(df.columns, start=1):
    print(f"{number:02}. {column}")


# ============================================================
# 8. FIRST 5 RECORDS
# ============================================================

print("\n" + "-" * 70)
print("FIRST 5 RECORDS")
print("-" * 70)

print(df.head().to_string())


# ============================================================
# 9. LAST 5 RECORDS
# ============================================================

print("\n" + "-" * 70)
print("LAST 5 RECORDS")
print("-" * 70)

print(df.tail().to_string())


# ============================================================
# 10. DATA TYPES
# ============================================================

print("\n" + "-" * 70)
print("DATA TYPES")
print("-" * 70)

print(df.dtypes)


# ============================================================
# 11. MISSING VALUES
# ============================================================

print("\n" + "-" * 70)
print("MISSING VALUES")
print("-" * 70)

missing_values = df.isnull().sum()

print(missing_values)


# ============================================================
# 12. DUPLICATE ROWS
# ============================================================

duplicate_rows = df.duplicated().sum()

print("\n" + "-" * 70)
print("DUPLICATE ROWS")
print("-" * 70)

print(f"Duplicate Rows : {duplicate_rows:,}")


# ============================================================
# 13. UNIQUE PRODUCT IDS
# ============================================================

if "product_id" in df.columns:

    unique_products = df["product_id"].nunique()

    print("\n" + "-" * 70)
    print("UNIQUE PRODUCTS")
    print("-" * 70)

    print(f"Unique Product IDs : {unique_products:,}")

else:
    print("\n⚠️ product_id column not found.")


# ============================================================
# 14. DATASET SUMMARY
# ============================================================

print("\n" + "-" * 70)
print("NUMERIC SUMMARY")
print("-" * 70)

print(df.describe().to_string())


# ============================================================
# 15. FINAL LOAD REPORT
# ============================================================

print("\n" + "=" * 70)
print("LOAD DATA COMPLETED SUCCESSFULLY")
print("=" * 70)

print(f"Total Rows          : {rows:,}")
print(f"Total Columns       : {columns}")
print(f"Duplicate Rows      : {duplicate_rows:,}")

if "product_id" in df.columns:
    print(f"Unique Product IDs  : {unique_products:,}")

print("=" * 70)