import os
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Global matplotlib settings for clean rendering
plt.rcParams["font.sans-serif"] = "DejaVu Sans"
plt.rcParams["axes.edgecolor"] = "#333333"
plt.rcParams["axes.linewidth"] = 0.8

# Path Setup
csv_path = os.path.join("output", "cleaned_data.csv")
if not os.path.exists(csv_path):
    csv_path = "cleaned_data.csv"

df = pd.read_csv(csv_path)

# Data Cleaning & Conversion
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
df["rating_count"] = pd.to_numeric(
    df["rating_count"].astype(str).str.replace(",", "", regex=False),
    errors="coerce",
)
df["discount_percentage"] = pd.to_numeric(
    df["discount_percentage"].astype(str).str.replace("%", "", regex=False),
    errors="coerce",
)
df = df.dropna(subset=["rating", "rating_count", "discount_percentage"])


def shorten(text, length=45):
    return (
        str(text)[:length] + "..." if len(str(text)) > length else str(text)
    )


df["short_name"] = df["product_name"].apply(lambda x: shorten(x, 45))

output_dir = os.path.join("output", "charts")
os.makedirs(output_dir, exist_ok=True)


# --- 1. KPI CARDS (01 to 04) ---
def save_kpi_card(
    title, value, bg_color, border_color, output_filename, figsize=(4, 2)
):
    fig, ax = plt.subplots(figsize=figsize, dpi=150)
    ax.axis("off")

    rect = patches.FancyBboxPatch(
        (0.05, 0.05),
        0.9,
        0.9,
        boxstyle="round,pad=0.08,rounding_size=0.15",
        linewidth=1.5,
        edgecolor=border_color,
        facecolor=bg_color,
        transform=ax.transAxes,
        clip_on=False,
    )
    ax.add_patch(rect)

    ax.text(
        0.5,
        0.62,
        title,
        fontsize=13,
        fontweight="bold",
        ha="center",
        va="center",
        color="#000066",
        transform=ax.transAxes,
    )
    ax.text(
        0.5,
        0.32,
        value,
        fontsize=18,
        fontweight="bold",
        ha="center",
        va="center",
        color="#000066",
        transform=ax.transAxes,
    )

    plt.savefig(
        os.path.join(output_dir, output_filename),
        bbox_inches="tight",
        transparent=True,
    )
    plt.close()


save_kpi_card(
    "TOTAL PRODUCTS",
    f"{len(df)}",
    "#E6ECFA",
    "#B0C4DE",
    "01_total_products.png",
)
save_kpi_card(
    "AVERAGE PRODUCT RATING",
    f"{df['rating'].mean():.2f} ★",
    "#D9EAD3",
    "#B0D8B0",
    "02_average_rating.png",
)
save_kpi_card(
    "AVERAGE DISCOUNT",
    f"{df['discount_percentage'].mean():.1f} %",
    "#FCE5CD",
    "#E6C280",
    "03_average_discount.png",
)
save_kpi_card(
    "TOTAL REVIEWS",
    f"{df['rating_count'].sum():,.0f}",
    "#F8D7DA",
    "#F5C6CB",
    "04_total_reviews.png",
)


# --- 2. HORIZONTAL BAR CHARTS WITH BLACK BORDER & END LABELS ---
def save_horizontal_bar_chart(
    data,
    x_col,
    y_col,
    title,
    xlabel,
    ylabel,
    color,
    output_filename,
    is_count=False,
    is_percentage=False,
):
    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)

    # Sort and take top 10
    top_data = data.head(10).iloc[::-1]  # reverse for top-down view

    y_pos = np.arange(len(top_data))
    bars = ax.barh(
        y_pos,
        top_data[x_col],
        height=0.68,
        color=color,
        edgecolor="black",
        linewidth=1.0,
    )

    ax.set_yticks(y_pos)
    ax.set_yticklabels(top_data[y_col], fontsize=9)
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_title(title, fontsize=15, fontweight="bold", pad=15)

    ax.grid(axis="x", linestyle="--", alpha=0.4, color="#cccccc")
    ax.set_axisbelow(True)

    max_val = top_data[x_col].max()
    for bar, val in zip(bars, top_data[x_col]):
        width = bar.get_width()
        if is_count:
            label_text = f"{int(val):,}"
        elif is_percentage:
            label_text = f"{val:.0f}%"
        else:
            label_text = f"{val:.1f}"

        ax.text(
            width + (max_val * 0.01),
            bar.get_y() + bar.get_height() / 2,
            label_text,
            va="center",
            ha="left",
            fontsize=10,
            fontweight="bold",
        )

    ax.set_xlim(0, max_val * 1.12)
    plt.tight_layout()
    plt.savefig(
        os.path.join(output_dir, output_filename), bbox_inches="tight"
    )
    plt.close()


# Top Reviewed Products (Figure 0.4 style - Blue)
df_reviewed = df.sort_values(by="rating_count", ascending=False)
save_horizontal_bar_chart(
    df_reviewed,
    "rating_count",
    "short_name",
    "Top 10 Most Reviewed Products",
    "Number of Reviews",
    "Product",
    "#4682B4",
    "top_10_reviewed_products.png",
    is_count=True,
)
save_horizontal_bar_chart(
    df_reviewed,
    "rating_count",
    "short_name",
    "Top 10 Most Reviewed Products",
    "Number of Reviews",
    "Product",
    "#4682B4",
    "08_top_reviewed_products.png",
    is_count=True,
)

# Top Highest Discount Products (Figure 0.5 style - Orange)
df_discount = df.sort_values(by="discount_percentage", ascending=False)
save_horizontal_bar_chart(
    df_discount,
    "discount_percentage",
    "short_name",
    "Top 10 Highest Discount Products",
    "Discount (%)",
    "Product",
    "#FFA500",
    "top_10_highest_discount_products.png",
    is_percentage=True,
)
save_horizontal_bar_chart(
    df_discount,
    "discount_percentage",
    "short_name",
    "Top 10 Highest Discount Products",
    "Discount (%)",
    "Product",
    "#FFA500",
    "09_top_discount_products.png",
    is_percentage=True,
)

# Top Highest Rated Products (Figure 0.6 style - Green)
df_rated = df.sort_values(
    by=["rating", "rating_count"], ascending=[False, False]
)
save_horizontal_bar_chart(
    df_rated,
    "rating",
    "short_name",
    "Top 10 Highest Rated Products",
    "Rating",
    "Product Name",
    "#228B22",
    "top_10_highest_rated_products.png",
)
save_horizontal_bar_chart(
    df_rated,
    "rating",
    "short_name",
    "Top 10 Highest Rated Products",
    "Rating",
    "Product Name",
    "#228B22",
    "07_top_rated_products.png",
)


# --- 3. SCATTER PLOT (Figure 0.7 style - Purple) ---
def save_scatter_plot(output_filename):
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=150)
    ax.scatter(
        df["discount_percentage"],
        df["rating"],
        color="#A5429E",
        edgecolor="#800080",
        alpha=0.7,
        s=50,
        linewidth=0.8,
    )
    ax.set_title(
        "Discount Percentage vs. Product Rating",
        fontsize=14,
        fontweight="bold",
        pad=15,
    )
    ax.set_xlabel("Discount (%)", fontsize=11)
    ax.set_ylabel("Rating (0 to 5)", fontsize=11)
    ax.grid(True, linestyle="--", alpha=0.4, color="#cccccc")
    ax.set_axisbelow(True)

    plt.tight_layout()
    plt.savefig(
        os.path.join(output_dir, output_filename), bbox_inches="tight"
    )
    plt.close()


save_scatter_plot("10_discount_vs_rating.png")
save_scatter_plot("discount_vs_rating_analysis.png")

print("All individual charts updated successfully!")