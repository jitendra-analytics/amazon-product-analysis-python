# =====================================
# Project : Amazon Product Data Analysis
# Author  : Jitendra More
# File    : 06_visualization.py
# =====================================

import pandas as pd
import matplotlib.pyplot as plt
import os

# =====================================
# Load Cleaned Dataset
# =====================================

df = pd.read_csv("output/cleaned_data.csv")

# =====================================
# Create Output Folder
# =====================================

os.makedirs("output/charts", exist_ok=True)

# =====================================
# KPI Summary
# =====================================

print("=" * 50)
print(" AMAZON PRODUCT DATA ANALYSIS ")
print("=" * 50)

print(f"Total Products      : {df['product_id'].nunique()}")
print(f"Average Rating      : {round(df['rating'].mean(),2)}")
print(f"Average Discount    : {round(df['discount_percentage'].mean(),2)} %")
print(f"Total Reviews       : {int(df['rating_count'].sum()):,}")

# =====================================
# Top 10 Highest Rated Products
# =====================================

top_rated = (
    df[['product_name','rating']]
    .sort_values(by='rating', ascending=False)
    .head(10)
)

plt.figure(figsize=(12,6))
plt.barh(top_rated['product_name'], top_rated['rating'])
plt.title("Top 10 Highest Rated Products")
plt.xlabel("Rating")
plt.ylabel("Product")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("output/charts/top_10_highest_rated_products.png", dpi=300)
plt.close()

# =====================================
# Top 10 Reviewed Products
# =====================================

top_reviewed = (
    df[['product_name','rating_count']]
    .sort_values(by='rating_count', ascending=False)
    .head(10)
)

plt.figure(figsize=(12,6))
plt.barh(top_reviewed['product_name'], top_reviewed['rating_count'])
plt.title("Top 10 Reviewed Products")
plt.xlabel("Review Count")
plt.ylabel("Product")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("output/charts/top_10_reviewed_products.png", dpi=300)
plt.close()

# =====================================
# Top 10 Highest Discount Products
# =====================================

top_discount = (
    df[['product_name','discount_percentage']]
    .sort_values(by='discount_percentage', ascending=False)
    .head(10)
)

plt.figure(figsize=(12,6))
plt.barh(top_discount['product_name'], top_discount['discount_percentage'])
plt.title("Top 10 Highest Discount Products")
plt.xlabel("Discount (%)")
plt.ylabel("Product")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("output/charts/top_10_highest_discount_products.png", dpi=300)
plt.close()

# =====================================
# Discount vs Rating Analysis
# =====================================

plt.figure(figsize=(8,6))
plt.scatter(
    df['discount_percentage'],
    df['rating'],
    alpha=0.6
)

plt.title("Discount vs Rating Analysis")
plt.xlabel("Discount Percentage")
plt.ylabel("Rating")
plt.grid(True)
plt.tight_layout()
plt.savefig("output/charts/discount_vs_rating_analysis.png", dpi=300)
plt.close()

print("\nCharts Created Successfully!")
print("Location : output/charts/")