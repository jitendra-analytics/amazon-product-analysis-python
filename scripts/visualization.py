"""
Amazon Product Data Visualization (Refactored for 6x4 Charts @ 100 DPI)
Author: Jitendra More
"""

import os
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

# Standard Figure Dimension & Quality Setup
FIG_SIZE = (6, 4)
DPI_VAL = 100

# Create Output Folder
os.makedirs("output/charts", exist_ok=True)

# Helper function to truncate long titles for graphs
def shorten_text(text, max_len=25):
    text = str(text)
    return text[:max_len] + "..." if len(text) > max_len else text

# Helper function to extract main category name
def clean_category(cat_str):
    if pd.isna(cat_str):
        return "Unknown"
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
    df["short_product_name"] = df["product_name"].apply(lambda x: shorten_text(x, 25))
else:
    df["short_product_name"] = df["product_id"]

if "category" in df.columns:
    df["clean_category"] = df["category"].apply(clean_category).apply(lambda x: shorten_text(x, 20))

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
    fig, ax = plt.subplots(figsize=FIG_SIZE, dpi=DPI_VAL)
    ax.text(0.5, 0.55, value, fontsize=24, fontweight="bold", ha="center", va="center", color=color)
    ax.text(0.5, 0.3, title.upper(), fontsize=12, fontweight="bold", ha="center", va="center", color="#555555")
    ax.axis("off")
    plt.tight_layout()
    plt.savefig(f"output/charts/{filename}", dpi=DPI_VAL, bbox_inches="tight")
    plt.close()

# =====================================================
# 05 Rating Distribution
# =====================================================
plt.figure(figsize=FIG_SIZE, dpi=DPI_VAL)
sns.histplot(df["rating"], bins=10, kde=True, color="#2b5c8f", edgecolor="black")
plt.title("Rating Distribution", fontsize=12, fontweight="bold", pad=10)
plt.xlabel("Rating (Out of 5)", fontsize=10)
plt.ylabel("Number of Products", fontsize=10)
plt.tight_layout()
plt.savefig("output/charts/05_rating_distribution.png")
plt.close()

# =====================================================
# 06 Discount Distribution
# =====================================================
plt.figure(figsize=FIG_SIZE, dpi=DPI_VAL)
sns.histplot(df["discount_percentage"], bins=10, kde=True, color="#2ca02c", edgecolor="black")
plt.title("Discount Percentage Distribution", fontsize=12, fontweight="bold", pad=10)
plt.xlabel("Discount (%)", fontsize=10)
plt.ylabel("Number of Products", fontsize=10)
plt.tight_layout()
plt.savefig("output/charts/06_discount_distribution.png")
plt.close()

# =====================================================
# 07 Top 10 Highest Rated Products
# =====================================================
top_rating = df.sort_values(by=["rating", "rating_count"], ascending=[False, False]).head(10)

plt.figure(figsize=FIG_SIZE, dpi=DPI_VAL)
bars = plt.barh(top_rating["short_product_name"], top_rating["rating"], color="#3182bd")
plt.title("Top 10 Highest Rated Products", fontsize=12, fontweight="bold", pad=10)
plt.xlabel("Rating", fontsize=10)
plt.xlim(0, 5)
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("output/charts/07_top_rated_products.png")
plt.close()

# =====================================================
# 08 Top 10 Reviewed Products
# =====================================================
top_review = df.sort_values("rating_count", ascending=False).head(10)

plt.figure(figsize=FIG_SIZE, dpi=DPI_VAL)
plt.barh(top_review["short_product_name"], top_review["rating_count"], color="#e6550d")
plt.title("Top 10 Most Reviewed Products", fontsize=12, fontweight="bold", pad=10)
plt.xlabel("Review Count", fontsize=10)
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("output/charts/08_top_reviewed_products.png")
plt.close()

# =====================================================
# 09 Top 10 Highest Discount Products
# =====================================================
top_discount = df.sort_values("discount_percentage", ascending=False).head(10)

plt.figure(figsize=FIG_SIZE, dpi=DPI_VAL)
plt.barh(top_discount["short_product_name"], top_discount["discount_percentage"], color="#31a354")
plt.title("Top 10 Highest Discount Products", fontsize=12, fontweight="bold", pad=10)
plt.xlabel("Discount (%)", fontsize=10)
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("output/charts/09_top_discount_products.png")
plt.close()

# =====================================================
# 10 Discount vs Rating
# =====================================================
plt.figure(figsize=FIG_SIZE, dpi=DPI_VAL)
sns.scatterplot(data=df, x="discount_percentage", y="rating", alpha=0.7, color="#756bb1", s=40)
plt.title("Discount % vs Product Rating", fontsize=12, fontweight="bold", pad=10)
plt.xlabel("Discount (%)", fontsize=10)
plt.ylabel("Rating", fontsize=10)
plt.tight_layout()
plt.savefig("output/charts/10_discount_vs_rating.png")
plt.close()

# =====================================================
# 11 Top Categories
# =====================================================
cat_col = "clean_category" if "clean_category" in df.columns else "category"
top_category = df[cat_col].value_counts().head(10)

plt.figure(figsize=FIG_SIZE, dpi=DPI_VAL)
plt.barh(top_category.index, top_category.values, color="#6baed6")
plt.title("Top 10 Product Categories", fontsize=12, fontweight="bold", pad=10)
plt.xlabel("Number of Products", fontsize=10)
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("output/charts/11_top_categories.png")
plt.close()

# =====================================================
# 14 Correlation Heatmap
# =====================================================
plt.figure(figsize=FIG_SIZE, dpi=DPI_VAL)
corr = df[["actual_price", "discounted_price", "discount_percentage", "rating", "rating_count"]].corr()

sns.heatmap(
    corr, 
    annot=True, 
    cmap="Blues", 
    linewidths=0.5, 
    fmt=".2f",
    cbar_kws={"shrink": .8},
    annot_kws={"size": 8}
)
plt.title("Correlation Matrix", fontsize=12, fontweight="bold", pad=10)
plt.tight_layout()
plt.savefig("output/charts/14_correlation_heatmap.png")
plt.close()

# =====================================================
# 15 Category Share (Donut Chart)
# =====================================================
plt.figure(figsize=FIG_SIZE, dpi=DPI_VAL)
colors = sns.color_palette("tab10", len(top_category))

wedges, texts, autotexts = plt.pie(
    top_category, 
    labels=top_category.index, 
    autopct="%1.1f%%", 
    startangle=140,
    pctdistance=0.75,
    colors=colors,
    textprops={"fontsize": 7}
)

centre_circle = plt.Circle((0,0), 0.50, fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

plt.title("Top 10 Category Share", fontsize=12, fontweight="bold", pad=10)
plt.tight_layout()
plt.savefig("output/charts/15_category_share.png")
plt.close()

print("\nAll Charts Created Successfully with Size (6, 4) @ 100 DPI!")