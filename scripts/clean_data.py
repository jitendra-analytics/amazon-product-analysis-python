"""
Amazon Product Analysis
Step 2: Data Cleaning

Author: Jitendra More
"""

import os
import pandas as pd


# ============================================================
# 1. SETTINGS
# ============================================================

DATA_PATH = os.path.join("data", "amazon.csv")
OUTPUT_PATH = os.path.join("output", "cleaned_data.csv")

os.makedirs("output", exist_ok=True)


# ============================================================
# 2. START MESSAGE
# ============================================================

print("=" * 65)
print("AMAZON PRODUCT DATA CLEANING")
print("=" * 65)


# ============================================================
# 3. LOAD RAW DATASET
# ============================================================

try:
    df = pd.read_csv(DATA_PATH)

except FileNotFoundError:
    print(f"\nERROR: Dataset not found at: {DATA_PATH}")
    print("Please check that amazon.csv exists inside the data folder.")
    raise SystemExit(1)

except Exception as error:
    print(f"\nERROR while loading dataset: {error}")
    raise SystemExit(1)


print("\nDataset Loaded Successfully")
print("-" * 65)


# ============================================================
# 4. STORE ORIGINAL DATASET INFORMATION
# ============================================================

# Store these values BEFORE any cleaning.
# This fixes the incorrect Original Rows count.

original_rows = len(df)
original_columns = len(df.columns)

print(f"Original Rows       : {original_rows:,}")
print(f"Original Columns    : {original_columns}")


# ============================================================
# 5. STANDARDIZE COLUMN NAMES
# ============================================================

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_", regex=False)
)

print("\nColumn Names Standardized")


# ============================================================
# 6. CHECK REQUIRED COLUMNS
# ============================================================

required_dataset_columns = [
    "product_id",
    "product_name",
    "category",
    "discounted_price",
    "actual_price",
    "discount_percentage",
    "rating",
    "rating_count",
]

missing_columns = [
    column
    for column in required_dataset_columns
    if column not in df.columns
]

if missing_columns:
    print("\nERROR: Required columns are missing:")
    
    for column in missing_columns:
        print(f"- {column}")

    raise SystemExit(1)


# ============================================================
# 7. EXACT DUPLICATE ROW CHECK
# ============================================================

duplicate_rows = df.duplicated().sum()

print("\nDuplicate Check")
print("-" * 65)
print(f"Exact Duplicate Rows : {duplicate_rows:,}")

if duplicate_rows > 0:
    df = df.drop_duplicates().copy()


# ============================================================
# 8. CLEAN TEXT COLUMNS
# ============================================================

text_columns = [
    "product_id",
    "product_name",
    "category",
    "about_product",
    "user_id",
    "user_name",
    "review_id",
    "review_title",
    "review_content",
    "img_link",
    "product_link",
]

for column in text_columns:

    if column in df.columns:

        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
        )


# ============================================================
# 9. CLEAN DISCOUNTED PRICE
# ============================================================

df["discounted_price"] = (
    df["discounted_price"]
    .astype(str)
    .str.replace("₹", "", regex=False)
    .str.replace(",", "", regex=False)
    .str.strip()
)

df["discounted_price"] = pd.to_numeric(
    df["discounted_price"],
    errors="coerce"
)


# ============================================================
# 10. CLEAN ACTUAL PRICE
# ============================================================

df["actual_price"] = (
    df["actual_price"]
    .astype(str)
    .str.replace("₹", "", regex=False)
    .str.replace(",", "", regex=False)
    .str.strip()
)

df["actual_price"] = pd.to_numeric(
    df["actual_price"],
    errors="coerce"
)


# ============================================================
# 11. CLEAN DISCOUNT PERCENTAGE
# ============================================================

df["discount_percentage"] = (
    df["discount_percentage"]
    .astype(str)
    .str.replace("%", "", regex=False)
    .str.strip()
)

df["discount_percentage"] = pd.to_numeric(
    df["discount_percentage"],
    errors="coerce"
)


# ============================================================
# 12. CLEAN RATING
# ============================================================

df["rating"] = (
    df["rating"]
    .astype(str)
    .str.strip()
)

df["rating"] = pd.to_numeric(
    df["rating"],
    errors="coerce"
)


# ============================================================
# 13. CLEAN RATING COUNT
# ============================================================

df["rating_count"] = (
    df["rating_count"]
    .astype(str)
    .str.replace(",", "", regex=False)
    .str.strip()
)

df["rating_count"] = pd.to_numeric(
    df["rating_count"],
    errors="coerce"
)


# ============================================================
# 14. INVALID VALUE CHECK
# ============================================================

# Rating must be between 0 and 5.

df.loc[
    (df["rating"] < 0)
    | (df["rating"] > 5),
    "rating"
] = pd.NA


# Discount percentage must be between 0 and 100.

df.loc[
    (df["discount_percentage"] < 0)
    | (df["discount_percentage"] > 100),
    "discount_percentage"
] = pd.NA


# Actual price cannot be negative.

df.loc[
    df["actual_price"] < 0,
    "actual_price"
] = pd.NA


# Discounted price cannot be negative.

df.loc[
    df["discounted_price"] < 0,
    "discounted_price"
] = pd.NA


# Review count cannot be negative.

df.loc[
    df["rating_count"] < 0,
    "rating_count"
] = pd.NA


# ============================================================
# 15. MISSING VALUE REPORT
# ============================================================

print("\nMissing Values After Conversion")
print("-" * 65)

missing_values = df.isnull().sum()

missing_report = (
    missing_values[
        missing_values > 0
    ]
    .sort_values(ascending=False)
)

if len(missing_report) > 0:
    print(missing_report)

else:
    print("No Missing Values Found")


# ============================================================
# 16. REMOVE ROWS WITH MISSING ESSENTIAL VALUES
# ============================================================

required_analysis_columns = [
    "product_id",
    "product_name",
    "category",
    "discounted_price",
    "actual_price",
    "discount_percentage",
    "rating",
    "rating_count",
]

rows_before_missing_removal = len(df)

df = df.dropna(
    subset=required_analysis_columns
).copy()

rows_after_missing_removal = len(df)

rows_removed_missing = (
    rows_before_missing_removal
    - rows_after_missing_removal
)


# ============================================================
# 17. PRODUCT ID ANALYSIS
# ============================================================

# IMPORTANT:
# We are NOT deleting repeated product IDs.
#
# The same product_id may appear in multiple legitimate records.
# Product-level analysis should use product_id.nunique().

duplicate_product_rows = df.duplicated(
    subset=["product_id"],
    keep=False
).sum()

unique_product_ids = df["product_id"].nunique()


print("\nProduct ID Check")
print("-" * 65)

print(
    f"Rows with repeated Product IDs : "
    f"{duplicate_product_rows:,}"
)

print(
    f"Unique Product IDs             : "
    f"{unique_product_ids:,}"
)


# ============================================================
# 18. RESET INDEX
# ============================================================

df.reset_index(
    drop=True,
    inplace=True
)


# ============================================================
# 19. FINAL DUPLICATE CHECK
# ============================================================

remaining_duplicates = df.duplicated().sum()


# ============================================================
# 20. SAVE CLEANED DATASET
# ============================================================

try:

    df.to_csv(
        OUTPUT_PATH,
        index=False
    )

except Exception as error:

    print(
        f"\nERROR while saving cleaned dataset: "
        f"{error}"
    )

    raise SystemExit(1)


# ============================================================
# 21. FINAL DATA TYPES
# ============================================================

numeric_columns = [
    "discounted_price",
    "actual_price",
    "discount_percentage",
    "rating",
    "rating_count",
]


# ============================================================
# 22. CLEANING SUMMARY
# ============================================================

print("\n" + "=" * 65)
print("CLEANING SUMMARY")
print("=" * 65)

print(
    f"Original Rows               : "
    f"{original_rows:,}"
)

print(
    f"Original Columns            : "
    f"{original_columns}"
)

print(
    f"Exact Duplicates Removed    : "
    f"{duplicate_rows:,}"
)

print(
    f"Rows Removed (Missing)      : "
    f"{rows_removed_missing:,}"
)

print(
    f"Final Rows                  : "
    f"{len(df):,}"
)

print(
    f"Final Columns               : "
    f"{len(df.columns)}"
)

print(
    f"Unique Product IDs          : "
    f"{df['product_id'].nunique():,}"
)

print(
    f"Remaining Exact Duplicates  : "
    f"{remaining_duplicates:,}"
)


# ============================================================
# 23. NUMERIC DATA TYPES
# ============================================================

print("\nNumeric Data Types")
print("-" * 65)

print(
    df[numeric_columns].dtypes
)


# ============================================================
# 24. FINAL VALIDATION
# ============================================================

print("\nFinal Validation")
print("-" * 65)

print(
    f"Minimum Rating              : "
    f"{df['rating'].min():.1f}"
)

print(
    f"Maximum Rating              : "
    f"{df['rating'].max():.1f}"
)

print(
    f"Minimum Discount            : "
    f"{df['discount_percentage'].min():.1f}%"
)

print(
    f"Maximum Discount            : "
    f"{df['discount_percentage'].max():.1f}%"
)

print(
    f"Minimum Actual Price        : "
    f"Rs. {df['actual_price'].min():,.2f}"
)

print(
    f"Maximum Actual Price        : "
    f"Rs. {df['actual_price'].max():,.2f}"
)


# ============================================================
# 25. OUTPUT LOCATION
# ============================================================

print("\nClean Dataset Saved:")
print(OUTPUT_PATH)


# ============================================================
# 26. COMPLETED
# ============================================================

print("\n" + "=" * 65)
print("DATA CLEANING COMPLETED SUCCESSFULLY")
print("=" * 65)