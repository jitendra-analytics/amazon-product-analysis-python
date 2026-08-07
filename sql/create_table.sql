-- ============================================================
-- AMAZON PRODUCT DATA ANALYSIS
-- Database & Table Creation
-- Author: Jitendra More
-- ============================================================

-- 1. Create Database
CREATE DATABASE IF NOT EXISTS amazon;

-- 2. Select Database
USE amazon;

-- 3. Drop old table if it exists
DROP TABLE IF EXISTS amazon_products;

-- 4. Create Amazon Products Table
CREATE TABLE amazon_products
(
    product_id VARCHAR(50) PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    discounted_price DECIMAL(10,2),
    actual_price DECIMAL(10,2),
    discount_percentage DECIMAL(5,2),
    rating DECIMAL(3,2),
    rating_count INT,
    about_product LONGTEXT,
    user_id TEXT,
    user_name TEXT,
    review_id TEXT,
    review_title TEXT,
    review_content LONGTEXT,
    img_link TEXT,
    product_link TEXT
);

-- ============================================================
-- VALIDATION
-- ============================================================

-- Check Table Structure
DESCRIBE amazon_products;

-- Count Total Rows
SELECT COUNT(*) AS total_rows
FROM amazon_products;

-- Count Unique Products
SELECT COUNT(DISTINCT product_id) AS unique_products
FROM amazon_products;

-- ============================================================
-- END
-- ============================================================