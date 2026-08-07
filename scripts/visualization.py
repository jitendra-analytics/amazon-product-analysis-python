"""
visualization.py

Amazon Product Data Visualization
Author: Jitendra More
"""

import os
import textwrap

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# ============================================================
# 1. GLOBAL SETTINGS
# ============================================================

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.edgecolor"] = "#333333"
plt.rcParams["axes.linewidth"] = 0.8
plt.rcParams["axes.titleweight"] = "bold"
plt.rcParams["axes.titlesize"] = 13
plt.rcParams["axes.labelsize"] = 10
plt.rcParams["xtick.labelsize"] = 8
plt.rcParams["ytick.labelsize"] = 8

sns.set_theme(style="whitegrid")


# ============================================================
# 2. PATH SETUP
# ============================================================

DATA_PATH = os.path.join("output", "cleaned_data.csv")
OUTPUT_DIR = os.path.join("output", "charts")

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# 3. LOAD CLEANED DATA
# ============================================================

try:
    df = pd.read_csv(DATA_PATH)

    print("=" * 70)
    print("AMAZON PRODUCT DATA VISUALIZATION")
    print("=" * 70)

    print("\nCleaned Dataset Loaded Successfully")
    print("-" * 70)
    print(f"Rows             : {len(df):,}")
    print(f"Columns          : {len(df.columns)}")
    print(f"Unique Products  : {df['product_id'].nunique():,}")

except FileNotFoundError:
    print("\nERROR: output/cleaned_data.csv not found.")
    print("Run clean_data.py first.")
    raise SystemExit


# ============================================================
# 4. NUMERIC CONVERSION
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
# 5. REMOVE REQUIRED MISSING VALUES
# ============================================================

required_columns = [
    "product_id",
    "product_name",
    "category",
    "rating",
    "rating_count",
    "discount_percentage",
    "actual_price",
    "discounted_price",
]

df = df.dropna(subset=required_columns).copy()


# ============================================================
# 6. PRODUCT-LEVEL DATA
# ============================================================

# One row per product ID.
# This keeps visualization logic consistent with analysis.py.

product_df = (
    df.sort_values(
        by=["product_id", "rating_count"],
        ascending=[True, False]
    )
    .drop_duplicates(subset="product_id")
    .copy()
)


# ============================================================
# 7. HELPER FUNCTIONS
# ============================================================

def shorten_name(text, width=31):
    """
    Shorten long product names without cutting chart layout.
    """
    text = str(text).strip()

    return textwrap.shorten(
        text,
        width=width,
        placeholder="..."
    )


def save_figure(fig, filename):
    """
    Save chart using standard project settings.
    """
    output_path = os.path.join(
        OUTPUT_DIR,
        filename
    )

    fig.savefig(
        output_path,
        dpi=150,
        bbox_inches="tight",
        facecolor="white"
    )

    plt.close(fig)


# ============================================================
# 8. CATEGORY NAME
# ============================================================

product_df["category_name"] = (
    product_df["category"]
    .astype(str)
    .str.split("|")
    .str[-1]
    .str.strip()
)


# ============================================================
# 9. KPI VALUES
# ============================================================

total_products = product_df["product_id"].nunique()

average_rating = product_df["rating"].mean()

average_discount = product_df["discount_percentage"].mean()

total_reviews = product_df["rating_count"].sum()


# ============================================================
# 10. KPI CARD FUNCTION
# ============================================================

def save_kpi_card(
    title,
    value,
    background_color,
    border_color,
    filename
):

    fig, ax = plt.subplots(
        figsize=(4.2, 2.2),
        dpi=150
    )

    fig.patch.set_facecolor("white")

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    card = patches.FancyBboxPatch(
        (0.06, 0.10),
        0.88,
        0.80,
        boxstyle="round,pad=0.04,rounding_size=0.12",
        linewidth=1.5,
        edgecolor=border_color,
        facecolor=background_color,
        transform=ax.transAxes
    )

    ax.add_patch(card)

    ax.text(
        0.50,
        0.62,
        title,
        ha="center",
        va="center",
        fontsize=12,
        fontweight="bold",
        color="#000066",
        transform=ax.transAxes
    )

    ax.text(
        0.50,
        0.36,
        value,
        ha="center",
        va="center",
        fontsize=18,
        fontweight="bold",
        color="#000066",
        transform=ax.transAxes
    )

    save_figure(
        fig,
        filename
    )


# ============================================================
# 01. TOTAL PRODUCTS
# ============================================================

save_kpi_card(
    "TOTAL PRODUCTS",
    f"{total_products:,}",
    "#E6ECFA",
    "#B0C4DE",
    "01_total_products.png"
)


# ============================================================
# 02. AVERAGE PRODUCT RATING
# ============================================================

save_kpi_card(
    "AVERAGE PRODUCT RATING",
    f"{average_rating:.2f}",
    "#D9EAD3",
    "#B0D8B0",
    "02_average_rating.png"
)


# ============================================================
# 03. AVERAGE DISCOUNT
# ============================================================

save_kpi_card(
    "AVERAGE DISCOUNT",
    f"{average_discount:.2f}%",
    "#FCE5CD",
    "#E6C280",
    "03_average_discount.png"
)


# ============================================================
# 04. TOTAL REVIEWS
# ============================================================

save_kpi_card(
    "TOTAL REVIEWS",
    f"{total_reviews:,.0f}",
    "#F8D7DA",
    "#F5C6CB",
    "04_total_reviews.png"
)


# ============================================================
# 05. RATING DISTRIBUTION
# ============================================================

fig, ax = plt.subplots(
    figsize=(6.2, 4.2),
    dpi=150
)

sns.histplot(
    data=product_df,
    x="rating",
    bins=10,
    kde=True,
    color="steelblue",
    edgecolor="black",
    linewidth=0.8,
    ax=ax
)

ax.set_title(
    "Rating Distribution",
    pad=12
)

ax.set_xlabel(
    "Rating (Out of 5)"
)

ax.set_ylabel(
    "Number of Products"
)

ax.grid(
    axis="both",
    linestyle="--",
    alpha=0.25
)

fig.tight_layout()

save_figure(
    fig,
    "05_rating_distribution.png"
)


# ============================================================
# 06. DISCOUNT DISTRIBUTION
# ============================================================

fig, ax = plt.subplots(
    figsize=(6.2, 4.2),
    dpi=150
)

sns.histplot(
    data=product_df,
    x="discount_percentage",
    bins=10,
    kde=True,
    color="lightgreen",
    edgecolor="black",
    linewidth=0.8,
    ax=ax
)

ax.set_title(
    "Discount Percentage Distribution",
    pad=12
)

ax.set_xlabel(
    "Discount (%)"
)

ax.set_ylabel(
    "Number of Products"
)

ax.grid(
    axis="both",
    linestyle="--",
    alpha=0.25
)

fig.tight_layout()

save_figure(
    fig,
    "06_discount_distribution.png"
)


# ============================================================
# 11. HORIZONTAL BAR CHART FUNCTION
# ============================================================

def save_product_bar_chart(
    data,
    x_column,
    title,
    xlabel,
    color,
    filename,
    value_type="normal"
):

    chart_data = data.copy()

    # Reverse only for display.
    # Highest product will appear at the top.
    display_data = chart_data.iloc[::-1].copy()

    display_data["display_name"] = (
        display_data["product_name"]
        .apply(lambda x: shorten_name(x, 32))
    )

    fig, ax = plt.subplots(
        figsize=(8.2, 5.2),
        dpi=150
    )

    y_position = np.arange(
        len(display_data)
    )

    bars = ax.barh(
        y_position,
        display_data[x_column],
        height=0.62,
        color=color,
        edgecolor="black",
        linewidth=0.8
    )

    ax.set_yticks(
        y_position
    )

    ax.set_yticklabels(
        display_data["display_name"],
        fontsize=7.5
    )

    ax.set_title(
        title,
        fontsize=13,
        fontweight="bold",
        pad=12
    )

    ax.set_xlabel(
        xlabel,
        fontsize=9
    )

    ax.set_ylabel(
        "Product Name",
        fontsize=9
    )

    ax.grid(
        axis="x",
        linestyle="--",
        alpha=0.25
    )

    ax.set_axisbelow(True)

    max_value = display_data[x_column].max()

    # --------------------------------------------------------
    # VALUE LABELS
    # --------------------------------------------------------

    for bar, value in zip(
        bars,
        display_data[x_column]
    ):

        if value_type == "count":
            label = f"{int(value):,}"

        elif value_type == "percentage":
            label = f"{value:.0f}%"

        else:
            label = f"{value:.1f}"

        ax.text(
            bar.get_width() + (max_value * 0.008),
            bar.get_y() + (bar.get_height() / 2),
            label,
            va="center",
            ha="left",
            fontsize=7.5,
            fontweight="bold"
        )

    # Extra right space for labels.
    ax.set_xlim(
        0,
        max_value * 1.14
    )

    # Product names remain inside image.
    fig.subplots_adjust(
        left=0.36,
        right=0.94,
        top=0.88,
        bottom=0.12
    )

    save_figure(
        fig,
        filename
    )


# ============================================================
# 07. TOP 10 HIGHEST RATED PRODUCTS
# ============================================================

top_rated = (
    product_df
    .sort_values(
        by=[
            "rating",
            "rating_count"
        ],
        ascending=[
            False,
            False
        ]
    )
    .drop_duplicates(
        subset="product_name"
    )
    .head(10)
    .copy()
)

save_product_bar_chart(
    top_rated,
    "rating",
    "Top 10 Highest Rated Products",
    "Rating",
    "forestgreen",
    "07_top_10_rated_products.png",
    value_type="normal"
)


# ============================================================
# 08. TOP 10 MOST REVIEWED PRODUCTS
# ============================================================

top_reviewed = (
    product_df
    .sort_values(
        by=[
            "rating_count",
            "rating"
        ],
        ascending=[
            False,
            False
        ]
    )
    .drop_duplicates(
        subset="product_name"
    )
    .head(10)
    .copy()
)

save_product_bar_chart(
    top_reviewed,
    "rating_count",
    "Top 10 Most Reviewed Products",
    "Number of Reviews",
    "steelblue",
    "08_top_10_reviewed_products.png",
    value_type="count"
)


# ============================================================
# 09. TOP 10 HIGHEST DISCOUNT PRODUCTS
# ============================================================

top_discount = (
    product_df
    .sort_values(
        by=[
            "discount_percentage",
            "rating_count"
        ],
        ascending=[
            False,
            False
        ]
    )
    .drop_duplicates(
        subset="product_name"
    )
    .head(10)
    .copy()
)

save_product_bar_chart(
    top_discount,
    "discount_percentage",
    "Top 10 Highest Discount Products",
    "Discount (%)",
    "orange",
    "09_top_10_discount_products.png",
    value_type="percentage"
)


# ============================================================
# 10. DISCOUNT VS PRODUCT RATING
# ============================================================

fig, ax = plt.subplots(
    figsize=(7, 4.3),
    dpi=150
)

ax.scatter(
    product_df["discount_percentage"],
    product_df["rating"],
    color="purple",
    alpha=0.55,
    s=28
)

ax.set_title(
    "Discount Percentage vs Product Rating",
    fontsize=13,
    fontweight="bold",
    pad=12
)

ax.set_xlabel(
    "Discount (%)"
)

ax.set_ylabel(
    "Rating (0 to 5)"
)

ax.grid(
    True,
    linestyle="--",
    alpha=0.25
)

fig.tight_layout()

save_figure(
    fig,
    "10_discount_vs_rating.png"
)


# ============================================================
# 11. TOP 10 PRODUCT CATEGORIES
# ============================================================

top_categories = (
    product_df["category_name"]
    .value_counts()
    .head(10)
)

fig, ax = plt.subplots(
    figsize=(7, 4.6),
    dpi=150
)

category_display = top_categories.iloc[::-1]

bars = ax.barh(
    category_display.index,
    category_display.values,
    color="skyblue",
    edgecolor="black",
    linewidth=0.8
)

ax.set_title(
    "Top 10 Product Categories",
    fontsize=13,
    fontweight="bold",
    pad=12
)

ax.set_xlabel(
    "Number of Products"
)

ax.set_ylabel(
    "Category"
)

ax.grid(
    axis="x",
    linestyle="--",
    alpha=0.25
)

ax.set_axisbelow(True)

max_category = category_display.max()

for bar, value in zip(
    bars,
    category_display.values
):

    ax.text(
        bar.get_width() + max_category * 0.01,
        bar.get_y() + bar.get_height() / 2,
        f"{int(value)}",
        va="center",
        fontsize=8,
        fontweight="bold"
    )

ax.set_xlim(
    0,
    max_category * 1.12
)

fig.tight_layout()

save_figure(
    fig,
    "11_top_10_categories.png"
)


# ============================================================
# 14. CORRELATION HEATMAP
# ============================================================

correlation_columns = [
    "actual_price",
    "discounted_price",
    "discount_percentage",
    "rating",
    "rating_count"
]

correlation = (
    product_df[correlation_columns]
    .corr()
)

fig, ax = plt.subplots(
    figsize=(7, 5),
    dpi=150
)

sns.heatmap(
    correlation,
    annot=True,
    fmt=".2f",
    cmap="Blues",
    linewidths=0.5,
    cbar=True,
    ax=ax
)

ax.set_title(
    "Correlation Matrix",
    fontsize=13,
    fontweight="bold",
    pad=12
)

ax.tick_params(
    axis="x",
    rotation=90,
    labelsize=8
)

ax.tick_params(
    axis="y",
    rotation=0,
    labelsize=8
)

fig.tight_layout()

save_figure(
    fig,
    "14_correlation_heatmap.png"
)


# ============================================================
# 15. TOP 10 CATEGORY SHARE
# ============================================================

fig, ax = plt.subplots(
    figsize=(7, 5.5),
    dpi=150
)

ax.pie(
    top_categories.values,
    labels=top_categories.index,
    autopct="%1.1f%%",
    startangle=140,
    pctdistance=0.78,
    labeldistance=1.08,
    wedgeprops={
        "width": 0.45,
        "edgecolor": "white",
        "linewidth": 1
    },
    textprops={
        "fontsize": 7
    }
)

ax.set_title(
    "Top 10 Category Share",
    fontsize=13,
    fontweight="bold",
    pad=15
)

fig.tight_layout()

save_figure(
    fig,
    "15_category_share.png"
)


# ============================================================
# 16. FINAL VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("VISUALIZATION VALIDATION")
print("=" * 70)

print(f"Product-level Rows              : {len(product_df):,}")
print(f"Unique Product IDs              : {product_df['product_id'].nunique():,}")

print(f"Top Rated Rows                  : {len(top_rated)}")
print(f"Top Reviewed Rows               : {len(top_reviewed)}")
print(f"Top Discount Rows               : {len(top_discount)}")

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
# 17. FINAL MESSAGE
# ============================================================

chart_files = [
    "01_total_products.png",
    "02_average_rating.png",
    "03_average_discount.png",
    "04_total_reviews.png",
    "05_rating_distribution.png",
    "06_discount_distribution.png",
    "07_top_10_rated_products.png",
    "08_top_10_reviewed_products.png",
    "09_top_10_discount_products.png",
    "10_discount_vs_rating.png",
    "11_top_10_categories.png",
    "14_correlation_heatmap.png",
    "15_category_share.png",
]

print("\n" + "=" * 70)
print("ALL 13 CHARTS CREATED SUCCESSFULLY")
print("=" * 70)

for chart in chart_files:
    print(chart)

print("\nCharts Saved:")
print(OUTPUT_DIR)

print("\n" + "=" * 70)
print("VISUALIZATION COMPLETED SUCCESSFULLY")
print("=" * 70)