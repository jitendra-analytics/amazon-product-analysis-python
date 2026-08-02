"""
database.py
Import Cleaned Amazon Dataset into MySQL
Author: Jitendra More
"""

import pandas as pd
import mysql.connector

# ======================================
# MySQL Connection
# ======================================

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Root@1705",
    database="amazon"
)

cursor = connection.cursor()

print("=" * 60)
print("CONNECTED TO MYSQL")
print("=" * 60)

# ======================================
# Load CSV
# ======================================

df = pd.read_csv("output/cleaned_data.csv")

print("Rows Found :", len(df))

# ======================================
# Clean Numeric Columns
# ======================================

df["discounted_price"] = (
    df["discounted_price"]
    .astype(str)
    .str.replace("₹", "", regex=False)
    .str.replace(",", "", regex=False)
)

df["actual_price"] = (
    df["actual_price"]
    .astype(str)
    .str.replace("₹", "", regex=False)
    .str.replace(",", "", regex=False)
)

df["discount_percentage"] = (
    df["discount_percentage"]
    .astype(str)
    .str.replace("%", "", regex=False)
)

df["rating_count"] = (
    df["rating_count"]
    .astype(str)
    .str.replace(",", "", regex=False)
)

numeric_columns = [
    "discounted_price",
    "actual_price",
    "discount_percentage",
    "rating",
    "rating_count"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.where(pd.notnull(df), None)

# ======================================
# Insert Query
# ======================================

query = """
INSERT IGNORE INTO amazon_products
(
product_id,
product_name,
category,
discounted_price,
actual_price,
discount_percentage,
rating,
rating_count,
about_product,
user_id,
user_name,
review_id,
review_title,
review_content,
img_link,
product_link
)
VALUES
(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""

count = 0

for _, row in df.iterrows():

    values = (
        row["product_id"],
        row["product_name"],
        row["category"],
        row["discounted_price"],
        row["actual_price"],
        row["discount_percentage"],
        row["rating"],
        row["rating_count"],
        row["about_product"],
        row["user_id"],
        row["user_name"],
        row["review_id"],
        row["review_title"],
        row["review_content"],
        row["img_link"],
        row["product_link"]
    )

    try:
        cursor.execute(query, values)
        count += 1

    except mysql.connector.Error as e:
        print(e)

connection.commit()

print("=" * 60)
print("Rows Inserted :", count)
print("=" * 60)

cursor.close()
connection.close()

print("DATABASE IMPORT COMPLETED")