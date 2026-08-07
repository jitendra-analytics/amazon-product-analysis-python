"""
Amazon Product Analysis
Step 3: Exploratory Data Analysis

Author: Jitendra More
"""

import os
import pandas as pd


# ============================================================
# 1. SETTINGS
# ============================================================

DATA_PATH = os.path.join("output", "cleaned_data.csv")
REPORT_DIR = os.path.join("output", "reports")
REPORT_PATH = os.path.join(REPORT_DIR, "analysis_report.txt")

os.makedirs(REPORT_DIR, exist_ok=True)


# ============================================================
# 2. LOAD CLEANED DATASET
# ============================================================

print("=" * 70)
print("AMAZON PRODUCT DATA ANALYSIS")
print("=" * 70)

try:
    df = pd.read_csv(DATA_PATH)

except FileNotFoundError:
    print(f"\nERROR: File not found: {DATA_PATH}")
    print("Run clean_data.py first.")
    raise SystemExit(1)


print("\nCleaned Dataset Loaded Successfully")
print("-" * 70)
print(f"Rows             : {len(df):,}")
print(f"Columns          : {len(df.columns)}")
print(f"Unique Products  : {df['product_id'].nunique():,}")


# ============================================================
# 3. ENSURE NUMERIC COLUMNS
# ============================================================

numeric_columns = [
    "discounted_price",
    "actual_price",
    "discount_percentage",
    "rating",
    "rating_count",
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )


# ============================================================
# 4. REMOVE REQUIRED MISSING VALUES
# ============================================================

df = df.dropna(
    subset=[
        "product_id",
        "product_name",
        "category",
        "discounted_price",
        "actual_price",
        "discount_percentage",
        "rating",
        "rating_count",
    ]
)


# ============================================================
# 5. CREATE PRODUCT-LEVEL DATASET
# ============================================================

# One row per unique product ID.
# If the same product_id occurs more than once,
# keep the row with the highest rating_count.

product_df = (
    df.sort_values(
        by=["product_id", "rating_count"],
        ascending=[True, False]
    )
    .drop_duplicates(
        subset="product_id",
        keep="first"
    )
    .copy()
)


# ============================================================
# 6. CORE KPIs
# ============================================================

total_products = product_df["product_id"].nunique()
average_rating = product_df["rating"].mean()
average_discount = product_df["discount_percentage"].mean()
total_reviews = product_df["rating_count"].sum()
average_actual_price = product_df["actual_price"].mean()
average_discounted_price = product_df["discounted_price"].mean()


print("\n" + "=" * 70)
print("KEY PERFORMANCE INDICATORS")
print("=" * 70)

print(f"Total Products             : {total_products:,}")
print(f"Average Rating             : {average_rating:.2f}")
print(f"Average Discount           : {average_discount:.2f}%")
print(f"Total Reviews              : {total_reviews:,.0f}")
print(f"Average Actual Price       : Rs. {average_actual_price:,.2f}")
print(f"Average Discounted Price   : Rs. {average_discounted_price:,.2f}")


# ============================================================
# 7. HIGHEST RATED PRODUCT
# ============================================================

highest_rated = (
    product_df.sort_values(
        by=["rating", "rating_count"],
        ascending=[False, False]
    )
    .iloc[0]
)

print("\n" + "=" * 70)
print("HIGHEST RATED PRODUCT")
print("=" * 70)

print(f"Product : {highest_rated['product_name']}")
print(f"Rating  : {highest_rated['rating']:.1f}")
print(f"Reviews : {highest_rated['rating_count']:,.0f}")


# ============================================================
# 8. MOST REVIEWED PRODUCT
# ============================================================

most_reviewed = (
    product_df.sort_values(
        by="rating_count",
        ascending=False
    )
    .iloc[0]
)

print("\n" + "=" * 70)
print("MOST REVIEWED PRODUCT")
print("=" * 70)

print(f"Product : {most_reviewed['product_name']}")
print(f"Reviews : {most_reviewed['rating_count']:,.0f}")
print(f"Rating  : {most_reviewed['rating']:.1f}")


# ============================================================
# 9. HIGHEST DISCOUNT PRODUCT
# ============================================================

highest_discount = (
    product_df.sort_values(
        by=["discount_percentage", "rating_count"],
        ascending=[False, False]
    )
    .iloc[0]
)

print("\n" + "=" * 70)
print("HIGHEST DISCOUNT PRODUCT")
print("=" * 70)

print(f"Product          : {highest_discount['product_name']}")
print(f"Discount         : {highest_discount['discount_percentage']:.0f}%")
print(f"Actual Price     : Rs. {highest_discount['actual_price']:,.2f}")
print(f"Discounted Price : Rs. {highest_discount['discounted_price']:,.2f}")


# ============================================================
# 10. TOP 10 HIGHEST RATED PRODUCTS
# ============================================================

top_rated = (
    product_df.sort_values(
        by=["rating", "rating_count"],
        ascending=[False, False]
    )
    .drop_duplicates(
        subset="product_name",
        keep="first"
    )
    .head(10)
    .copy()
)

print("\n" + "=" * 70)
print("TOP 10 HIGHEST RATED PRODUCTS")
print("=" * 70)

print(
    top_rated[
        [
            "product_name",
            "rating",
            "rating_count"
        ]
    ].to_string(index=False)
)


# ============================================================
# 11. TOP 10 MOST REVIEWED PRODUCTS
# ============================================================

top_reviewed = (
    product_df.sort_values(
        by="rating_count",
        ascending=False
    )
    .drop_duplicates(
        subset="product_name",
        keep="first"
    )
    .head(10)
    .copy()
)

print("\n" + "=" * 70)
print("TOP 10 MOST REVIEWED PRODUCTS")
print("=" * 70)

print(
    top_reviewed[
        [
            "product_name",
            "rating_count",
            "rating"
        ]
    ].to_string(index=False)
)


# ============================================================
# 12. TOP 10 HIGHEST DISCOUNT PRODUCTS
# ============================================================

top_discount = (
    product_df.sort_values(
        by=["discount_percentage", "rating_count"],
        ascending=[False, False]
    )
    .drop_duplicates(
        subset="product_name",
        keep="first"
    )
    .head(10)
    .copy()
)

print("\n" + "=" * 70)
print("TOP 10 HIGHEST DISCOUNT PRODUCTS")
print("=" * 70)

print(
    top_discount[
        [
            "product_name",
            "discount_percentage",
            "actual_price",
            "discounted_price"
        ]
    ].to_string(index=False)
)


# ============================================================
# 13. CATEGORY CLEANING
# ============================================================

product_df["category_name"] = (
    product_df["category"]
    .astype(str)
    .str.split("|")
    .str[-1]
    .str.strip()
)


# ============================================================
# 14. TOP 10 PRODUCT CATEGORIES
# ============================================================

top_categories = (
    product_df["category_name"]
    .value_counts()
    .head(10)
)

print("\n" + "=" * 70)
print("TOP 10 PRODUCT CATEGORIES")
print("=" * 70)

print(top_categories.to_string())


# ============================================================
# 15. RATING ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("RATING ANALYSIS")
print("=" * 70)

minimum_rating = product_df["rating"].min()
maximum_rating = product_df["rating"].max()
median_rating = product_df["rating"].median()

high_rated_products = (
    product_df["rating"] >= 4.5
).sum()

print(f"Minimum Rating              : {minimum_rating:.2f}")
print(f"Maximum Rating              : {maximum_rating:.2f}")
print(f"Average Rating              : {average_rating:.2f}")
print(f"Median Rating               : {median_rating:.2f}")
print(f"Products Rated 4.5 or Above : {high_rated_products:,}")


# ============================================================
# 16. DISCOUNT ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("DISCOUNT ANALYSIS")
print("=" * 70)

minimum_discount = product_df["discount_percentage"].min()
maximum_discount = product_df["discount_percentage"].max()

high_discount_products = (
    product_df["discount_percentage"] >= 70
).sum()

print(f"Minimum Discount             : {minimum_discount:.2f}%")
print(f"Maximum Discount             : {maximum_discount:.2f}%")
print(f"Average Discount             : {average_discount:.2f}%")
print(f"Products with 70%+ Discount  : {high_discount_products:,}")


# ============================================================
# 17. PRICE ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("PRICE ANALYSIS")
print("=" * 70)

lowest_actual_price = product_df["actual_price"].min()
highest_actual_price = product_df["actual_price"].max()

print(f"Lowest Actual Price       : Rs. {lowest_actual_price:,.2f}")
print(f"Highest Actual Price      : Rs. {highest_actual_price:,.2f}")
print(f"Average Actual Price      : Rs. {average_actual_price:,.2f}")
print(f"Average Discounted Price  : Rs. {average_discounted_price:,.2f}")


# ============================================================
# 18. CORRELATION ANALYSIS
# ============================================================

correlation_columns = [
    "actual_price",
    "discounted_price",
    "discount_percentage",
    "rating",
    "rating_count",
]

correlation_matrix = product_df[
    correlation_columns
].corr()

print("\n" + "=" * 70)
print("CORRELATION MATRIX")
print("=" * 70)

print(
    correlation_matrix
    .round(2)
    .to_string()
)


# ============================================================
# 19. BUSINESS INSIGHTS
# ============================================================

print("\n" + "=" * 70)
print("BUSINESS INSIGHTS")
print("=" * 70)

most_common_category = top_categories.index[0]

print(
    f"1. The dataset contains "
    f"{total_products:,} unique products."
)

print(
    f"2. The average product rating is "
    f"{average_rating:.2f} out of 5."
)

print(
    f"3. The average discount offered is "
    f"{average_discount:.2f}%."
)

print(
    f"4. Products in the dataset received approximately "
    f"{total_reviews:,.0f} reviews."
)

print(
    f"5. {high_rated_products:,} products have ratings "
    f"of 4.5 or higher."
)

print(
    f"6. {high_discount_products:,} products offer "
    f"discounts of 70% or more."
)

print(
    f"7. The most common product category is "
    f"'{most_common_category}'."
)


# ============================================================
# 20. SAVE ANALYSIS REPORT
# ============================================================

with open(
    REPORT_PATH,
    "w",
    encoding="utf-8"
) as report:

    report.write(
        "AMAZON PRODUCT DATA ANALYSIS REPORT\n"
    )

    report.write("=" * 70 + "\n\n")

    # KPI SECTION
    report.write("KEY PERFORMANCE INDICATORS\n")
    report.write("-" * 70 + "\n")

    report.write(
        f"Total Products           : {total_products:,}\n"
    )

    report.write(
        f"Average Rating           : {average_rating:.2f}\n"
    )

    report.write(
        f"Average Discount         : {average_discount:.2f}%\n"
    )

    report.write(
        f"Total Reviews            : {total_reviews:,.0f}\n"
    )

    report.write(
        f"Average Actual Price     : "
        f"Rs. {average_actual_price:,.2f}\n"
    )

    report.write(
        f"Average Discounted Price : "
        f"Rs. {average_discounted_price:,.2f}\n"
    )

    # HIGHEST RATED
    report.write("\n")
    report.write("HIGHEST RATED PRODUCT\n")
    report.write("-" * 70 + "\n")

    report.write(
        f"{highest_rated['product_name']}\n"
    )

    report.write(
        f"Rating: {highest_rated['rating']:.1f}\n"
    )

    report.write(
        f"Reviews: {highest_rated['rating_count']:,.0f}\n"
    )

    # MOST REVIEWED
    report.write("\n")
    report.write("MOST REVIEWED PRODUCT\n")
    report.write("-" * 70 + "\n")

    report.write(
        f"{most_reviewed['product_name']}\n"
    )

    report.write(
        f"Reviews: {most_reviewed['rating_count']:,.0f}\n"
    )

    report.write(
        f"Rating: {most_reviewed['rating']:.1f}\n"
    )

    # HIGHEST DISCOUNT
    report.write("\n")
    report.write("HIGHEST DISCOUNT PRODUCT\n")
    report.write("-" * 70 + "\n")

    report.write(
        f"{highest_discount['product_name']}\n"
    )

    report.write(
        f"Discount: "
        f"{highest_discount['discount_percentage']:.0f}%\n"
    )

    report.write(
        f"Actual Price: "
        f"Rs. {highest_discount['actual_price']:,.2f}\n"
    )

    report.write(
        f"Discounted Price: "
        f"Rs. {highest_discount['discounted_price']:,.2f}\n"
    )

    # TOP 10 RATED
    report.write("\n")
    report.write("TOP 10 HIGHEST RATED PRODUCTS\n")
    report.write("-" * 70 + "\n")

    report.write(
        top_rated[
            [
                "product_name",
                "rating",
                "rating_count"
            ]
        ].to_string(index=False)
    )

    # TOP 10 REVIEWED
    report.write("\n\n")
    report.write("TOP 10 MOST REVIEWED PRODUCTS\n")
    report.write("-" * 70 + "\n")

    report.write(
        top_reviewed[
            [
                "product_name",
                "rating_count",
                "rating"
            ]
        ].to_string(index=False)
    )

    # TOP 10 DISCOUNT
    report.write("\n\n")
    report.write("TOP 10 HIGHEST DISCOUNT PRODUCTS\n")
    report.write("-" * 70 + "\n")

    report.write(
        top_discount[
            [
                "product_name",
                "discount_percentage",
                "actual_price",
                "discounted_price"
            ]
        ].to_string(index=False)
    )

    # CATEGORIES
    report.write("\n\n")
    report.write("TOP 10 PRODUCT CATEGORIES\n")
    report.write("-" * 70 + "\n")

    report.write(
        top_categories.to_string()
    )

    # RATING ANALYSIS
    report.write("\n\n")
    report.write("RATING ANALYSIS\n")
    report.write("-" * 70 + "\n")

    report.write(
        f"Minimum Rating: {minimum_rating:.2f}\n"
    )

    report.write(
        f"Maximum Rating: {maximum_rating:.2f}\n"
    )

    report.write(
        f"Average Rating: {average_rating:.2f}\n"
    )

    report.write(
        f"Median Rating: {median_rating:.2f}\n"
    )

    report.write(
        f"Products Rated 4.5 or Above: "
        f"{high_rated_products:,}\n"
    )

    # DISCOUNT ANALYSIS
    report.write("\n")
    report.write("DISCOUNT ANALYSIS\n")
    report.write("-" * 70 + "\n")

    report.write(
        f"Minimum Discount: {minimum_discount:.2f}%\n"
    )

    report.write(
        f"Maximum Discount: {maximum_discount:.2f}%\n"
    )

    report.write(
        f"Average Discount: {average_discount:.2f}%\n"
    )

    report.write(
        f"Products with 70%+ Discount: "
        f"{high_discount_products:,}\n"
    )

    # PRICE ANALYSIS
    report.write("\n")
    report.write("PRICE ANALYSIS\n")
    report.write("-" * 70 + "\n")

    report.write(
        f"Lowest Actual Price: "
        f"Rs. {lowest_actual_price:,.2f}\n"
    )

    report.write(
        f"Highest Actual Price: "
        f"Rs. {highest_actual_price:,.2f}\n"
    )

    report.write(
        f"Average Actual Price: "
        f"Rs. {average_actual_price:,.2f}\n"
    )

    report.write(
        f"Average Discounted Price: "
        f"Rs. {average_discounted_price:,.2f}\n"
    )

    # CORRELATION MATRIX
    report.write("\n")
    report.write("CORRELATION MATRIX\n")
    report.write("-" * 70 + "\n")

    report.write(
        correlation_matrix
        .round(2)
        .to_string()
    )

    # BUSINESS INSIGHTS
    report.write("\n\n")
    report.write("BUSINESS INSIGHTS\n")
    report.write("-" * 70 + "\n")

    report.write(
        f"1. The dataset contains "
        f"{total_products:,} unique products.\n"
    )

    report.write(
        f"2. The average product rating is "
        f"{average_rating:.2f} out of 5.\n"
    )

    report.write(
        f"3. The average discount offered is "
        f"{average_discount:.2f}%.\n"
    )

    report.write(
        f"4. Products received approximately "
        f"{total_reviews:,.0f} reviews.\n"
    )

    report.write(
        f"5. {high_rated_products:,} products have "
        f"ratings of 4.5 or higher.\n"
    )

    report.write(
        f"6. {high_discount_products:,} products offer "
        f"discounts of 70% or more.\n"
    )

    report.write(
        f"7. The most common product category is "
        f"'{most_common_category}'.\n"
    )


# ============================================================
# 21. FINAL VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("FINAL VALIDATION")
print("=" * 70)

print(f"Product-level Rows         : {len(product_df):,}")
print(f"Unique Product IDs         : {product_df['product_id'].nunique():,}")
print(f"Top Rated Rows             : {len(top_rated)}")
print(f"Top Reviewed Rows          : {len(top_reviewed)}")
print(f"Top Discount Rows          : {len(top_discount)}")

print(
    "Duplicate Names in Top Rated    :",
    top_rated["product_name"].duplicated().sum()
)

print(
    "Duplicate Names in Top Reviewed :",
    top_reviewed["product_name"].duplicated().sum()
)

print(
    "Duplicate Names in Top Discount :",
    top_discount["product_name"].duplicated().sum()
)


# ============================================================
# 22. FINAL MESSAGE
# ============================================================

print("\n" + "=" * 70)
print("ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 70)

print(f"\nAnalysis Report Saved : {REPORT_PATH}")