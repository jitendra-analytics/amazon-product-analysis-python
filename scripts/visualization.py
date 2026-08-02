"""
Amazon Product Data Visualization (Refactored)
Author: Jitendra More
"""

import os
import textwrap
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =====================================================
# Professional Styling Configuration
# =====================================================
sns.set_theme(style="whitegrid")
plt.rcParams["font.sans-serif"] = "DejaVu Sans"
plt.rcParams["axes.edgecolor"] = "#cccccc"
plt.rcParams["axes.linewidth"] = 0.8

# Create Output Folder
os.makedirs("output/charts", exist_ok=True)

# Helper function to truncate long titles for graphs
def shorten_text(text, max_len=40):
    text = str(text)
    return text[:max_len] + "..." if len(text) > max_len else text

# Helper function to extract main category name
def clean_category(cat_str):
    if pd.isna(cat_str):
        return "Unknown"
    # Take the last or first broad category if pipe-separated
    parts = str(cat_str).split("|")
    return parts[-1] if len(parts) > 1 else parts[0]

# =====================================================
# Load Clean Dataset
# =====================================================
DATA_PATH = "output/cleaned_data.csv"

if not os.path.exists(DATA_PATH):
    print(f"Error: {DATA_PATH} file not found!")
    exit()

df = pd.read_csv(DATA_PATH)

# Data Conversions
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

df["rating_count"] = pd.to_numeric(
    df["rating_count"].astype(str).str.replace(",", "", regex=False),
    errors="coerce"
)

df["discount_percentage"] = pd.to_numeric(
    df["discount_percentage"].astype(str).str.replace("%", "", regex=False),
    errors="coerce"
)

df["discounted_price"] = pd.to_numeric(
    df["discounted_price"].astype(str).str.replace("₹", "", regex=False).str.replace(",", "", regex=False),
    errors="coerce"
)

df["actual_price"] = pd.to_numeric(
    df["actual_price"].astype(str).str.replace("₹", "", regex=False).str.replace(",", "", regex=False),
    errors="coerce"
)

df = df.dropna(subset=["rating", "rating_count", "discount_percentage", "discounted_price", "actual_price"])

# Simplify Category & Product Names for clean visual labels
if "product_name" in df.columns:
    df["short_product_name"] = df["product_name"].apply(lambda x: shorten_text(x, 35))
else:
    df["short_product_name"] = df["product_id"]

if "category" in df.columns:
    df["clean_category"] = df["category"].apply(clean_category).apply(lambda x: shorten_text(x, 25))

# =====================================================
# KPI VALUES
# =====================================================
total_products = df["product_id"].nunique() if "product_id" in df.columns else len(df)
average_rating = df["rating"].mean()
average_discount = df["discount_percentage"].mean()
total_reviews = int(df["rating_count"].sum())

print("="*60)
print("AMAZON DATA VISUALIZATION")
print("="*60)
print("Total Products   :", total_products)
print("Average Rating   :", round(average_rating, 2))
print("Average Discount :", round(average_discount, 2), "%")
print("Total Reviews    :", f"{total_reviews:,}")
print("="*60)

# =====================================================
# KPI Cards (01 - 04)
# =====================================================
kpi_data = [
    ("01_total_products.png", "Total Products", f"{total_products:,}", "#1f77b4"),
    ("02_average_rating.png", "Average Rating", f"{average_rating:.2f} ★", "#ff7f0e"),
    ("03_average_discount.png", "Average Discount", f"{average_discount:.2f}%", "#2ca02c"),
    ("04_total_reviews.png", "Total Reviews", f"{total_reviews:,}", "#d62728")
]

for filename, title, value, color in kpi_data:
    fig, ax = plt.subplots(figsize=(5, 2.5))
    ax.text(0.5, 0.55, value, fontsize=28, fontweight="bold", ha="center", va="center", color=color)
    ax.text(0.5, 0.2, title.upper(), fontsize=11, fontweight="bold", ha="center", va="center", color="#555555")
    ax.axis("off")
    plt.tight_layout()
    plt.savefig(f"output/charts/{filename}", dpi=300, bbox_inches="tight")
    plt.close()

# =====================================================
# 05 Rating Distribution
# =====================================================
plt.figure(figsize=(8, 5))
sns.histplot(df["rating"], bins=10, kde=True, color="#2b5c8f", edgecolor="black")
plt.title("Rating Distribution", fontsize=14, fontweight="bold", pad=15)
plt.xlabel("Rating (Out of 5)", fontsize=11)
plt.ylabel("Number of Products", fontsize=11)
plt.tight_layout()
plt.savefig("output/charts/05_rating_distribution.png", dpi=300)
plt.close()

# =====================================================
# 06 Discount Distribution
# =====================================================
plt.figure(figsize=(8, 5))
sns.histplot(df["discount_percentage"], bins=10, kde=True, color="#2ca02c", edgecolor="black")
plt.title("Discount Percentage Distribution", fontsize=14, fontweight="bold", pad=15)
plt.xlabel("Discount (%)", fontsize=11)
plt.ylabel("Number of Products", fontsize=11)
plt.tight_layout()
plt.savefig("output/charts/06_discount_distribution.png", dpi=300)
plt.close()

print("\nPart 1 (KPIs & Distributions) Completed Successfully")

# =====================================================
# 07 Top 10 Highest Rated Products
# =====================================================
top_rating = df.sort_values(by=["rating", "rating_count"], ascending=[False, False]).head(10)

plt.figure(figsize=(10, 6))
bars = plt.barh(top_rating["short_product_name"], top_rating["rating"], color="#3182bd", edgecolor="none")
plt.title("Top 10 Highest Rated Products", fontsize=14, fontweight="bold", pad=15)
plt.xlabel("Rating", fontsize=11)
plt.xlim(0, 5)
plt.gca().invert_yaxis()

# Add values on bars
for bar in bars:
    plt.text(bar.get_width() - 0.3, bar.get_y() + bar.get_height()/2, f"{bar.get_width():.1f}", 
             va="center", color="white", fontweight="bold")

plt.tight_layout()
plt.savefig("output/charts/07_top_rated_products.png", dpi=300)
plt.close()

# =====================================================
# 08 Top 10 Reviewed Products
# =====================================================
top_review = df.sort_values("rating_count", ascending=False).head(10)

plt.figure(figsize=(10, 6))
plt.barh(top_review["short_product_name"], top_review["rating_count"], color="#e6550d")
plt.title("Top 10 Most Reviewed Products", fontsize=14, fontweight="bold", pad=15)
plt.xlabel("Review Count", fontsize=11)
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("output/charts/08_top_reviewed_products.png", dpi=300)
plt.close()

# =====================================================
# 09 Top 10 Highest Discount Products
# =====================================================
top_discount = df.sort_values("discount_percentage", ascending=False).head(10)

plt.figure(figsize=(10, 6))
plt.barh(top_discount["short_product_name"], top_discount["discount_percentage"], color="#31a354")
plt.title("Top 10 Highest Discount Products", fontsize=14, fontweight="bold", pad=15)
plt.xlabel("Discount (%)", fontsize=11)
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("output/charts/09_top_discount_products.png", dpi=300)
plt.close()

# =====================================================
# 10 Discount vs Rating
# =====================================================
plt.figure(figsize=(8, 6))
sns.scatterplot(
    data=df, 
    x="discount_percentage", 
    y="rating", 
    alpha=0.6, 
    color="#756bb1",
    s=50
)
plt.title("Discount Percentage vs Product Rating", fontsize=14, fontweight="bold", pad=15)
plt.xlabel("Discount (%)", fontsize=11)
plt.ylabel("Rating", fontsize=11)
plt.tight_layout()
plt.savefig("output/charts/10_discount_vs_rating.png", dpi=300)
plt.close()

# =====================================================
# 11 Top Categories
# =====================================================
cat_col = "clean_category" if "clean_category" in df.columns else "category"
top_category = df[cat_col].value_counts().head(10)

plt.figure(figsize=(10, 6))
plt.barh(top_category.index, top_category.values, color="#6baed6")
plt.title("Top 10 Product Categories", fontsize=14, fontweight="bold", pad=15)
plt.xlabel("Number of Products", fontsize=11)
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("output/charts/11_top_categories.png", dpi=300)
plt.close()

print("\nPart 2 (Top Products & Relationships) Completed Successfully")

# =====================================================
# 14 Correlation Heatmap
# =====================================================
plt.figure(figsize=(8, 6))
corr = df[["actual_price", "discounted_price", "discount_percentage", "rating", "rating_count"]].corr()

sns.heatmap(
    corr, 
    annot=True, 
    cmap="Blues", 
    linewidths=1, 
    fmt=".2f",
    cbar_kws={"shrink": .8}
)
plt.title("Correlation Matrix", fontsize=14, fontweight="bold", pad=15)
plt.tight_layout()
plt.savefig("output/charts/14_correlation_heatmap.png", dpi=300)
plt.close()

# =====================================================
# 15 Category Share (Donut Chart for better readability)
# =====================================================
plt.figure(figsize=(8, 8))
colors = sns.color_palette("tab10", len(top_category))

wedges, texts, autotexts = plt.pie(
    top_category, 
    labels=top_category.index, 
    autopct="%1.1f%%", 
    startangle=140,
    pctdistance=0.75,
    colors=colors,
    textprops={"fontsize": 9}
)

# Draw a circle in center to make it a Donut Chart
centre_circle = plt.Circle((0,0), 0.50, fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

plt.title("Top 10 Category Share", fontsize=14, fontweight="bold", pad=15)
plt.tight_layout()
plt.savefig("output/charts/15_category_share.png", dpi=300)
plt.close()

print("\nAll 15 Charts Created Successfully!")