"""
analysis.py

Amazon Product Data Analysis
Author: Jitendra More
"""

import pandas as pd

DATA_PATH = "output/cleaned_data.csv"

df = pd.read_csv(DATA_PATH)

print("=" * 60)
print("AMAZON PRODUCT DATA ANALYSIS")
print("=" * 60)

# -------------------------
# KPIs
# -------------------------

total_products = df["product_id"].nunique()

avg_rating = df["rating"].mean()

avg_discount = df["discount_percentage"].mean()

total_reviews = df["rating_count"].sum()

print(f"\nTotal Products      : {total_products}")
print(f"Average Rating      : {avg_rating:.2f}")
print(f"Average Discount    : {avg_discount:.2f}%")
print(f"Total Reviews       : {int(total_reviews):,}")

# -------------------------
# Highest Rated Product
# -------------------------

top_rating = df.sort_values("rating", ascending=False).iloc[0]

print("\nHighest Rated Product")
print("-------------------------")
print(top_rating["product_name"])
print("Rating :", top_rating["rating"])

# -------------------------
# Most Reviewed Product
# -------------------------

top_review = df.sort_values("rating_count", ascending=False).iloc[0]

print("\nMost Reviewed Product")
print("-------------------------")
print(top_review["product_name"])
print("Reviews :", int(top_review["rating_count"]))

# -------------------------
# Highest Discount Product
# -------------------------

top_discount = df.sort_values(
    "discount_percentage",
    ascending=False
).iloc[0]

print("\nHighest Discount Product")
print("-------------------------")
print(top_discount["product_name"])
print("Discount :", top_discount["discount_percentage"], "%")

# -------------------------
# Top Categories
# -------------------------

print("\nTop 10 Categories")
print("-------------------------")

print(df["category"].value_counts().head(10))

print("\n" + "=" * 60)
print("ANALYSIS COMPLETED")
print("=" * 60)