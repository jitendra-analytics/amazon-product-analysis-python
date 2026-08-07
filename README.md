# 🛒 Amazon Product Data Analysis using Python & MySQL

An end-to-end **Data Analytics Portfolio Project** built using **Python, Pandas, Matplotlib, Seaborn, MySQL, and SQL**.

This project demonstrates a complete data analytics workflow, starting from raw Amazon product data and progressing through **data loading, cleaning, exploratory analysis, visualization, MySQL database integration, SQL business analysis, and validation**.

---

## 📌 Project Overview

The objective of this project is to analyze Amazon product data and identify useful insights related to:

- Product ratings
- Customer reviews
- Discounts
- Product pricing
- Product categories
- Popular products
- Highly rated products
- Product-level business performance

The project follows a structured analytics workflow from raw data to business insights.

---

## 🔄 Project Workflow

```text
Raw Amazon Dataset
        ↓
Data Loading
        ↓
Data Validation
        ↓
Data Cleaning
        ↓
Exploratory Data Analysis
        ↓
Data Visualization
        ↓
MySQL Database Import
        ↓
SQL Business Analysis
        ↓
Final Validation
        ↓
Business Insights
```

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Data processing and project automation |
| Pandas | Data cleaning and analysis |
| NumPy | Numerical operations |
| Matplotlib | Data visualization |
| Seaborn | Statistical visualization |
| MySQL | Database management |
| SQL | Business analysis and queries |
| VS Code | Development environment |
| Git | Version control |
| GitHub | Project hosting and portfolio |

---

## 📂 Project Structure

```text
amazon-product-analysis-python/
│
├── data/
│   └── amazon.csv
│
├── output/
│   ├── cleaned_data.csv
│   ├── charts/
│   └── reports/
│
├── scripts/
│   ├── load_data.py
│   ├── clean_data.py
│   ├── analysis.py
│   ├── visualization.py
│   └── database.py
│
├── sql/
│   ├── create_table.sql
│   └── business_queries.sql
│
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 📊 Dataset Overview

The original Amazon dataset contains product, pricing, rating, review, category, and customer review information.

### Dataset Summary

| Metric | Value |
|---|---:|
| Original Rows | 1,465 |
| Original Columns | 16 |
| Rows Removed Due to Missing Required Values | 3 |
| Cleaned Rows | 1,462 |
| Unique Product IDs | 1,348 |
| Final Product-Level Records | 1,348 |

The dataset contains **16 columns**, including:

- `product_id`
- `product_name`
- `category`
- `discounted_price`
- `actual_price`
- `discount_percentage`
- `rating`
- `rating_count`
- `about_product`
- `user_id`
- `user_name`
- `review_id`
- `review_title`
- `review_content`
- `img_link`
- `product_link`

---

## 🧹 Data Cleaning

The data cleaning process includes:

- Checking dataset shape
- Checking column names and data types
- Missing value analysis
- Exact duplicate detection
- Numeric data conversion
- Removing currency symbols from prices
- Removing percentage symbols
- Removing commas from review counts
- Converting ratings to numeric format
- Removing records missing required analytical fields
- Product ID validation
- Product-level duplicate handling
- Resetting the DataFrame index
- Exporting the cleaned dataset

### Numeric Columns Converted

```text
discounted_price
actual_price
discount_percentage
rating
rating_count
```

The cleaned dataset is saved as:

```text
output/cleaned_data.csv
```

---

## 🔍 Data Validation

Several validation checks are performed before analysis and database import.

### Cleaning Validation

```text
Original Rows              : 1,465
Original Columns           : 16
Rows Removed (Missing)     : 3
Cleaned Rows               : 1,462
Unique Product IDs         : 1,348
Remaining Exact Duplicates : 0
```

### Product-Level Database Validation

```text
Rows Ready              : 1,348
Unique Product IDs      : 1,348
Duplicate Product IDs   : 0
```

### MySQL Validation

```text
Python Rows             : 1,348
Rows Inserted           : 1,348
Database Rows           : 1,348
Unique Product IDs      : 1,348
Invalid Product IDs     : 0

STATUS                  : PASSED
```

This confirms that the final Python product-level dataset and MySQL table contain matching records.

---

## 📊 Python Analysis

The analysis module calculates important product and business metrics, including:

- Total unique products
- Average product rating
- Average discount percentage
- Total customer reviews
- Highest-rated product
- Most-reviewed product
- Highest-discount product
- Top product categories

It also supports:

- Rating analysis
- Discount analysis
- Price analysis
- Category analysis
- Product performance analysis
- Statistical analysis

---

## 📈 Data Visualizations

The visualization pipeline generates **13 charts and KPI visuals**.

### KPI Cards

1. Total Products
2. Average Product Rating
3. Average Discount
4. Total Reviews

### Analytical Charts

5. Rating Distribution
6. Discount Percentage Distribution
7. Top 10 Highest Rated Products
8. Top 10 Most Reviewed Products
9. Top 10 Highest Discount Products
10. Discount Percentage vs Product Rating
11. Top 10 Product Categories
12. Correlation Matrix
13. Top 10 Category Share

### Generated Files

```text
output/charts/

01_total_products.png
02_average_rating.png
03_average_discount.png
04_total_reviews.png
05_rating_distribution.png
06_discount_distribution.png
07_top_10_rated_products.png
08_top_10_reviewed_products.png
09_top_10_discount_products.png
10_discount_vs_rating.png
11_top_10_categories.png
14_correlation_heatmap.png
15_category_share.png
```

---

## 🗄️ MySQL Database Integration

The cleaned product-level dataset is imported into MySQL using Python and `mysql-connector-python`.

### Database

```sql
amazon
```

### Table

```sql
amazon_products
```

### Primary Key

```sql
product_id
```

The database import script performs:

- MySQL connection
- Database creation
- Table creation
- Column validation
- Product ID validation
- Duplicate Product ID handling
- Data import
- Row-count validation
- Unique Product ID validation
- Invalid Product ID validation

---

## 💻 SQL Business Analysis

SQL analysis is stored in:

```text
sql/business_queries.sql
```

The project includes **30 SQL business and validation queries**.

### Core KPI Analysis

```sql
-- Total Products
SELECT COUNT(*) AS total_products
FROM amazon_products;

-- Average Rating
SELECT ROUND(AVG(rating), 2) AS average_rating
FROM amazon_products;

-- Average Discount
SELECT ROUND(AVG(discount_percentage), 2) AS average_discount
FROM amazon_products;

-- Total Reviews
SELECT SUM(rating_count) AS total_reviews
FROM amazon_products;
```

---

## 🔝 Product Performance Analysis

SQL queries analyze:

- Highest-rated product
- Most-reviewed product
- Highest-discount product
- Top 10 highest-rated products
- Top 10 most-reviewed products
- Top 10 highest-discount products
- Products rated above 4.5
- Products with discounts above 70%
- Products costing above ₹10,000
- Most expensive products
- Lowest-priced products
- Products with the largest price savings

Example:

```sql
SELECT
    product_name,
    rating,
    rating_count
FROM amazon_products
ORDER BY rating DESC, rating_count DESC
LIMIT 10;
```

---

## 📦 Category Analysis

The SQL analysis also evaluates product categories using:

- Product count by category
- Average rating by category
- Average discount by category
- Total reviews by category

Example:

```sql
SELECT
    category,
    COUNT(*) AS total_products,
    ROUND(AVG(rating), 2) AS average_rating
FROM amazon_products
GROUP BY category
ORDER BY average_rating DESC, total_products DESC
LIMIT 10;
```

---

## 💰 Price & Discount Analysis

The project includes SQL analysis for:

- Average actual price
- Average discounted price
- Highest discounts
- Price savings
- Discount ranges
- Price ranges
- High-rating and high-review products
- High-rating and high-discount products

Example:

```sql
SELECT
    product_name,
    actual_price,
    discounted_price,
    ROUND(actual_price - discounted_price, 2) AS savings_amount
FROM amazon_products
ORDER BY savings_amount DESC
LIMIT 10;
```

---

## 🔎 Final SQL Validation

The final validation query checks the complete MySQL dataset:

```sql
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT product_id) AS unique_product_ids,
    ROUND(AVG(rating), 2) AS average_rating,
    ROUND(AVG(discount_percentage), 2) AS average_discount,
    SUM(rating_count) AS total_reviews,
    MIN(rating) AS minimum_rating,
    MAX(rating) AS maximum_rating,
    MIN(discount_percentage) AS minimum_discount,
    MAX(discount_percentage) AS maximum_discount,
    MIN(actual_price) AS minimum_actual_price,
    MAX(actual_price) AS maximum_actual_price
FROM amazon_products;
```

---

## 🚀 How to Run the Project

### 1. Clone the Repository

```bash
git clone <repository-url>
cd amazon-product-analysis-python
```

### 2. Install Required Python Libraries

```bash
pip install -r requirements.txt
```

### 3. Run the Complete Python Pipeline

```bash
python main.py
```

### 4. Run Scripts Individually

```bash
python scripts/load_data.py
python scripts/clean_data.py
python scripts/analysis.py
python scripts/visualization.py
```

### 5. Import Data into MySQL

```bash
python scripts/database.py
```

The database script securely asks for the MySQL password at runtime instead of storing the password directly in the source code.

---

## 📌 Key Project Outputs

The project produces:

- Cleaned Amazon product dataset
- Product-level analytical dataset
- Python EDA results
- KPI cards
- Data visualization charts
- MySQL database
- SQL table schema
- SQL business analysis queries
- Database validation results

---

## 🎯 Skills Demonstrated

This project demonstrates practical experience with:

- Python Programming
- Pandas
- NumPy
- Data Cleaning
- Data Validation
- Exploratory Data Analysis
- Data Visualization
- Matplotlib
- Seaborn
- MySQL
- SQL
- Database Integration
- Business Analysis
- Git & GitHub
- VS Code
- Data Storytelling

---

## 💡 Business Questions Answered

This project helps answer questions such as:

- Which products receive the highest ratings?
- Which products receive the most customer reviews?
- Which products offer the highest discounts?
- Which categories contain the most products?
- Which categories receive stronger ratings?
- Which categories generate the most reviews?
- How are discounts distributed across products?
- Is there a relationship between discount percentage and rating?
- Which products provide the highest monetary savings?
- Which highly rated products also have strong customer engagement?

---

## 👨‍💻 Author

**Jitendra More**

Aspiring Data Analyst

### Skills

`Python` • `Pandas` • `NumPy` • `Matplotlib` • `Seaborn` • `SQL` • `MySQL` • `Git` • `GitHub`

---

## ⭐ Support

If you found this project useful, consider giving the repository a **Star ⭐** on GitHub.