# 🛒 Amazon Product Data Analysis using Python, MySQL.

An end-to-end **Data Analytics Portfolio Project** built using **Python, MySQL**. This project demonstrates the complete data analytics workflow from raw data cleaning to business insights, database integration, and interactive dashboard development.

---

# 📌 Project Overview

This project covers the complete Data Analysis process.

### Project Workflow

- 📥 Data Loading
- 🧹 Data Cleaning
- 📊 Exploratory Data Analysis (EDA)
- 📈 Professional Data Visualization
- 🗄️ MySQL Database Import
- 💻 SQL Business Queries
- 📊 Interactive chart and graph

---

# 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Data Processing |
| Pandas | Data Cleaning & Analysis |
| NumPy | Numerical Computing |
| Matplotlib | Data Visualization |
| MySQL | Database |
| SQL | Business Queries |
| VS Code | Development |
| Git & GitHub | Version Control |

---

# 📂 Project Structure

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
├
│
├── main.py
├── requirements.txt
└── README.md
```

---

# 📊 Python Analysis

The project performs:

- Load Dataset
- Missing Value Analysis
- Duplicate Removal
- Data Type Conversion
- Rating Analysis
- Discount Analysis
- Price Analysis
- Category Analysis
- Product Analysis
- Statistical Summary

---

# 📈 Generated Charts

- ✅ Total Products KPI
- ✅ Average Rating KPI
- ✅ Average Discount KPI
- ✅ Total Reviews KPI
- ✅ Top Rated Products
- ✅ Top Reviewed Products
- ✅ Highest Discount Products
- ✅ Rating Distribution
- ✅ Discount Distribution
- ✅ Discount vs Rating
- ✅ Top Categories
- ✅ Price Distribution
- ✅ Actual Price vs Discounted Price
- ✅ Correlation Heatmap
- ✅ Category Share Pie Chart

---

# 🗄️ MySQL Database

Database Name

```sql
amazon
```

Table Name

```sql
amazon_products
```

The cleaned dataset is imported into MySQL using Python for business analysis.

---

# 💻 SQL Business Queries

## 1. Total Products

```sql
SELECT COUNT(*) AS Total_Products
FROM amazon_products;
```

## 2. Average Rating

```sql
SELECT ROUND(AVG(rating),2) AS Average_Rating
FROM amazon_products;
```

## 3. Average Discount

```sql
SELECT ROUND(AVG(discount_percentage),2) AS Average_Discount
FROM amazon_products;
```

## 4. Total Reviews

```sql
SELECT SUM(rating_count) AS Total_Reviews
FROM amazon_products;
```

## 5. Highest Rated Product

```sql
SELECT product_name, rating
FROM amazon_products
ORDER BY rating DESC
LIMIT 1;
```

## 6. Most Reviewed Product

```sql
SELECT product_name, rating_count
FROM amazon_products
ORDER BY rating_count DESC
LIMIT 1;
```

## 7. Highest Discount Product

```sql
SELECT product_name, discount_percentage
FROM amazon_products
ORDER BY discount_percentage DESC
LIMIT 1;
```

## 8. Top 10 Highest Rated Products

```sql
SELECT product_name, rating
FROM amazon_products
ORDER BY rating DESC
LIMIT 10;
```

## 9. Top 10 Most Reviewed Products

```sql
SELECT product_name, rating_count
FROM amazon_products
ORDER BY rating_count DESC
LIMIT 10;
```

## 10. Top 10 Highest Discount Products

```sql
SELECT product_name, discount_percentage
FROM amazon_products
ORDER BY discount_percentage DESC
LIMIT 10;
```

## 11. Products with Rating Above 4.5

```sql
SELECT product_name, rating
FROM amazon_products
WHERE rating > 4.5;
```

## 12. Products with Discount Greater Than 70%

```sql
SELECT product_name, discount_percentage
FROM amazon_products
WHERE discount_percentage > 70;
```

## 13. Products Costing Above ₹10,000

```sql
SELECT product_name, discounted_price
FROM amazon_products
WHERE discounted_price > 10000;
```

---

# 📊 Power BI Dashboard

The dashboard includes:

## KPI Cards

- Total Products
- Average Rating
- Average Discount
- Total Reviews
- Average Actual Price
- Average Discounted Price

## Visualizations

- Top Categories
- Rating Distribution
- Discount Distribution
- Discount vs Rating
- Category Share
- Price Distribution
- Top Reviewed Products
- Top Rated Products
- Correlation Analysis

## Filters

- Category
- Rating

---

# 🚀 How to Run

## Install Required Libraries

```bash
pip install -r requirements.txt
```

## Run Complete Project

```bash
python main.py
```

Or run individual scripts:

```bash
python scripts/load_data.py
python scripts/clean_data.py
python scripts/analysis.py
python scripts/visualization.py
python scripts/database.py
```

---

# 📷 Project Output

The project generates:

- Cleaned Dataset
- Analysis Report
- Professional Charts
- MySQL Database
- SQL Business Reports


---

# 🎯 Skills Demonstrated

- Python Programming
- Data Cleaning
- Exploratory Data Analysis (EDA)
- Data Visualization
- SQL Query Writing
- MySQL Database
- Business Intelligence
- Data Storytelling

---

# 👨‍💻 Author

**Jitendra More**

**Aspiring Data Analyst**

- Python
- MySQL
- Pandas
- Data Visualization

---

# ⭐ Support

If you found this project helpful, please consider giving this repository a **Star ⭐** on GitHub.