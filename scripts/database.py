"""
database.py

Amazon Product Data Analysis
Step 5: MySQL Database Import

Author: Jitendra More
"""

import os
from getpass import getpass

import mysql.connector
import pandas as pd
from mysql.connector import Error


# ============================================================
# 1. SETTINGS
# ============================================================

DATA_PATH = os.path.join("output", "cleaned_data.csv")

MYSQL_HOST = "localhost"
MYSQL_USER = "root"
DATABASE_NAME = "amazon"
TABLE_NAME = "amazon_products"


# ============================================================
# 2. HEADER
# ============================================================

print("=" * 60)
print("MYSQL DATABASE IMPORT")
print("=" * 60)


# ============================================================
# 3. CHECK CLEANED DATASET
# ============================================================

if not os.path.exists(DATA_PATH):
    print("\nERROR: Cleaned dataset not found.")
    print(f"Expected File: {DATA_PATH}")
    print("Run clean_data.py first.")
    raise SystemExit(1)


# ============================================================
# 4. LOAD CLEANED DATASET
# ============================================================

try:
    df = pd.read_csv(DATA_PATH)

except Exception as error:
    print("\nERROR: Could not read cleaned dataset.")
    print(error)
    raise SystemExit(1)


print("\nClean Dataset Loaded Successfully")
print("-" * 60)
print(f"Rows Found              : {len(df):,}")
print(f"Columns Found           : {len(df.columns):,}")


# ============================================================
# 5. REQUIRED COLUMN VALIDATION
# ============================================================

required_columns = [
    "product_id",
    "product_name",
    "category",
    "discounted_price",
    "actual_price",
    "discount_percentage",
    "rating",
    "rating_count",
    "about_product",
    "user_id",
    "user_name",
    "review_id",
    "review_title",
    "review_content",
    "img_link",
    "product_link",
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:
    print("\nERROR: Required columns are missing:")
    for column in missing_columns:
        print(f" - {column}")

    raise SystemExit(1)


print("Required Columns         : OK")


# ============================================================
# 6. NUMERIC VALIDATION
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
        errors="coerce",
    )


# ============================================================
# 7. REMOVE INVALID PRODUCT IDS
# ============================================================

df = df.dropna(
    subset=[
        "product_id",
        "product_name",
    ]
).copy()

df["product_id"] = df["product_id"].astype(str).str.strip()

df = df[
    df["product_id"] != ""
].copy()


# ============================================================
# 8. PRODUCT-LEVEL VALIDATION
# ============================================================

duplicate_product_ids = df["product_id"].duplicated().sum()

if duplicate_product_ids > 0:
    print(
        f"\nWARNING: {duplicate_product_ids:,} duplicate "
        "Product IDs found."
    )

    print("Keeping the first record for each Product ID.")

    df = df.drop_duplicates(
        subset="product_id",
        keep="first",
    ).copy()


df.reset_index(
    drop=True,
    inplace=True,
)


python_rows = len(df)

unique_product_ids = df["product_id"].nunique()


print("\nProduct-Level Validation")
print("-" * 60)
print(f"Rows Ready              : {python_rows:,}")
print(f"Unique Product IDs      : {unique_product_ids:,}")
print(
    f"Duplicate Product IDs   : "
    f"{df['product_id'].duplicated().sum():,}"
)


# ============================================================
# 9. CONVERT NaN TO None FOR MYSQL
# ============================================================

df = df.astype(object).where(
    pd.notnull(df),
    None,
)


# ============================================================
# 10. GET MYSQL PASSWORD
# ============================================================

print("\nMySQL Login")
print("-" * 60)

MYSQL_PASSWORD = getpass(
    "Enter MySQL root password: "
)


# ============================================================
# 11. INITIALIZE CONNECTION VARIABLES
# ============================================================

server_connection = None
connection = None
cursor = None


try:

    # ========================================================
    # 12. CONNECT TO MYSQL SERVER
    # ========================================================

    server_connection = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
    )

    server_cursor = server_connection.cursor()

    print("\nConnected to MySQL Successfully")


    # ========================================================
    # 13. CREATE DATABASE
    # ========================================================

    server_cursor.execute(
        f"CREATE DATABASE IF NOT EXISTS `{DATABASE_NAME}` "
        "CHARACTER SET utf8mb4 "
        "COLLATE utf8mb4_unicode_ci"
    )

    server_connection.commit()

    print(f"Database Ready          : {DATABASE_NAME}")

    server_cursor.close()
    server_connection.close()

    server_connection = None


    # ========================================================
    # 14. CONNECT TO AMAZON DATABASE
    # ========================================================

    connection = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=DATABASE_NAME,
        charset="utf8mb4",
    )

    cursor = connection.cursor()


    # ========================================================
    # 15. CREATE TABLE
    # ========================================================

    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS `{TABLE_NAME}` (

        product_id VARCHAR(100) NOT NULL,

        product_name TEXT,

        category TEXT,

        discounted_price DECIMAL(12,2),

        actual_price DECIMAL(12,2),

        discount_percentage DECIMAL(6,2),

        rating DECIMAL(3,2),

        rating_count BIGINT,

        about_product LONGTEXT,

        user_id LONGTEXT,

        user_name LONGTEXT,

        review_id LONGTEXT,

        review_title LONGTEXT,

        review_content LONGTEXT,

        img_link TEXT,

        product_link TEXT,

        PRIMARY KEY (product_id)

    )
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci
    """

    cursor.execute(create_table_query)

    connection.commit()

    print(f"Table Ready             : {TABLE_NAME}")


    # ========================================================
    # 16. CLEAR OLD TABLE DATA
    # ========================================================

    cursor.execute(
        f"TRUNCATE TABLE `{TABLE_NAME}`"
    )

    connection.commit()

    print("Previous Table Data     : Cleared")


    # ========================================================
    # 17. INSERT QUERY
    # ========================================================

    insert_query = f"""
    INSERT INTO `{TABLE_NAME}` (
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
    VALUES (
        %s, %s, %s, %s,
        %s, %s, %s, %s,
        %s, %s, %s, %s,
        %s, %s, %s, %s
    )
    """


    # ========================================================
    # 18. PREPARE RECORDS
    # ========================================================

    records = []

    for row in df[required_columns].itertuples(
        index=False,
        name=None,
    ):
        records.append(row)


    # ========================================================
    # 19. INSERT DATA
    # ========================================================

    print("\nImporting Data...")

    cursor.executemany(
        insert_query,
        records,
    )

    connection.commit()

    inserted_rows = cursor.rowcount


    # ========================================================
    # 20. DATABASE VALIDATION
    # ========================================================

    cursor.execute(
        f"SELECT COUNT(*) FROM `{TABLE_NAME}`"
    )

    database_rows = cursor.fetchone()[0]


    cursor.execute(
        f"""
        SELECT COUNT(DISTINCT product_id)
        FROM `{TABLE_NAME}`
        """
    )

    database_unique_products = cursor.fetchone()[0]


    # ========================================================
    # 21. NULL PRODUCT ID VALIDATION
    # ========================================================

    cursor.execute(
        f"""
        SELECT COUNT(*)
        FROM `{TABLE_NAME}`
        WHERE product_id IS NULL
           OR TRIM(product_id) = ''
        """
    )

    invalid_product_ids = cursor.fetchone()[0]


    # ========================================================
    # 22. FINAL IMPORT REPORT
    # ========================================================

    print("\n" + "=" * 60)
    print("DATABASE IMPORT SUMMARY")
    print("=" * 60)

    print(f"Database                : {DATABASE_NAME}")
    print(f"Table                   : {TABLE_NAME}")
    print(f"Python Rows             : {python_rows:,}")
    print(f"Rows Inserted           : {inserted_rows:,}")
    print(f"Database Rows           : {database_rows:,}")
    print(
        f"Unique Product IDs      : "
        f"{database_unique_products:,}"
    )
    print(
        f"Invalid Product IDs     : "
        f"{invalid_product_ids:,}"
    )


    # ========================================================
    # 23. FINAL VALIDATION
    # ========================================================

    validation_passed = (
        python_rows == database_rows
        and
        unique_product_ids == database_unique_products
        and
        invalid_product_ids == 0
    )


    print("\n" + "=" * 60)
    print("FINAL VALIDATION")
    print("=" * 60)

    if validation_passed:

        print("STATUS                  : PASSED")
        print(
            "Python and MySQL row counts match."
        )

    else:

        print("STATUS                  : FAILED")

        if python_rows != database_rows:
            print(
                "WARNING: Python rows and "
                "MySQL rows do not match."
            )

        if (
            unique_product_ids
            != database_unique_products
        ):
            print(
                "WARNING: Unique Product ID "
                "counts do not match."
            )

        if invalid_product_ids != 0:
            print(
                "WARNING: Invalid Product IDs "
                "exist in MySQL."
            )


    # ========================================================
    # 24. SAMPLE DATABASE RECORDS
    # ========================================================

    cursor.execute(
        f"""
        SELECT
            product_id,
            product_name,
            rating,
            rating_count,
            discount_percentage
        FROM `{TABLE_NAME}`
        ORDER BY rating_count DESC
        LIMIT 5
        """
    )

    sample_rows = cursor.fetchall()


    print("\nTop 5 Sample Records")
    print("-" * 60)

    for number, row in enumerate(
        sample_rows,
        start=1,
    ):

        product_id = row[0]
        product_name = str(row[1])[:55]
        rating = row[2]
        reviews = row[3]
        discount = row[4]

        print(
            f"{number}. {product_id} | "
            f"{product_name} | "
            f"Rating: {rating} | "
            f"Reviews: {reviews:,} | "
            f"Discount: {discount}%"
        )


    # ========================================================
    # 25. SUCCESS MESSAGE
    # ========================================================

    print("\n" + "=" * 60)

    if validation_passed:
        print(
            "DATABASE IMPORT COMPLETED SUCCESSFULLY"
        )
    else:
        print(
            "DATABASE IMPORT COMPLETED "
            "WITH VALIDATION WARNINGS"
        )

    print("=" * 60)


# ============================================================
# 26. MYSQL ERROR HANDLING
# ============================================================

except Error as error:

    print("\n" + "=" * 60)
    print("MYSQL ERROR")
    print("=" * 60)

    print(error)

    if connection is not None:
        try:
            connection.rollback()
        except Error:
            pass

    raise SystemExit(1)


# ============================================================
# 27. GENERAL ERROR HANDLING
# ============================================================

except Exception as error:

    print("\n" + "=" * 60)
    print("UNEXPECTED ERROR")
    print("=" * 60)

    print(error)

    if connection is not None:
        try:
            connection.rollback()
        except Error:
            pass

    raise SystemExit(1)


# ============================================================
# 28. CLOSE CONNECTION
# ============================================================

finally:

    if cursor is not None:
        try:
            cursor.close()
        except Error:
            pass

    if connection is not None:
        try:
            if connection.is_connected():
                connection.close()
        except Error:
            pass

    if server_connection is not None:
        try:
            if server_connection.is_connected():
                server_connection.close()
        except Error:
            pass