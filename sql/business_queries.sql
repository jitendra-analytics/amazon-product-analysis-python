-- ============================================================
-- AMAZON PRODUCT DATA ANALYSIS
-- SQL BUSINESS QUERIES
-- Author: Jitendra More
-- Database: amazon
-- Table: amazon_products
-- ============================================================

USE amazon;

-- ============================================================
-- 1. TOTAL PRODUCTS
-- ============================================================

SELECT COUNT(*) AS total_products
FROM amazon_products;


-- ============================================================
-- 2. AVERAGE PRODUCT RATING
-- ============================================================

SELECT ROUND(AVG(rating), 2) AS average_rating
FROM amazon_products;


-- ============================================================
-- 3. AVERAGE DISCOUNT PERCENTAGE
-- ============================================================

SELECT ROUND(AVG(discount_percentage), 2) AS average_discount
FROM amazon_products;


-- ============================================================
-- 4. TOTAL REVIEWS
-- ============================================================

SELECT SUM(rating_count) AS total_reviews
FROM amazon_products;


-- ============================================================
-- 5. HIGHEST RATED PRODUCT
-- Tie-breaker: higher review count
-- ============================================================

SELECT
    product_id,
    product_name,
    rating,
    rating_count
FROM amazon_products
ORDER BY rating DESC, rating_count DESC
LIMIT 1;


-- ============================================================
-- 6. MOST REVIEWED PRODUCT
-- ============================================================

SELECT
    product_id,
    product_name,
    rating_count,
    rating
FROM amazon_products
ORDER BY rating_count DESC
LIMIT 1;


-- ============================================================
-- 7. HIGHEST DISCOUNT PRODUCT
-- ============================================================

SELECT
    product_id,
    product_name,
    discount_percentage,
    actual_price,
    discounted_price
FROM amazon_products
ORDER BY discount_percentage DESC
LIMIT 1;


-- ============================================================
-- 8. TOP 10 HIGHEST RATED PRODUCTS
-- ============================================================

SELECT
    product_id,
    product_name,
    rating,
    rating_count
FROM amazon_products
ORDER BY rating DESC, rating_count DESC
LIMIT 10;


-- ============================================================
-- 9. TOP 10 MOST REVIEWED PRODUCTS
-- ============================================================

SELECT
    product_id,
    product_name,
    rating_count,
    rating
FROM amazon_products
ORDER BY rating_count DESC
LIMIT 10;


-- ============================================================
-- 10. TOP 10 HIGHEST DISCOUNT PRODUCTS
-- ============================================================

SELECT
    product_id,
    product_name,
    discount_percentage,
    actual_price,
    discounted_price
FROM amazon_products
ORDER BY discount_percentage DESC
LIMIT 10;


-- ============================================================
-- 11. PRODUCTS WITH RATING ABOVE 4.5
-- ============================================================

SELECT
    product_id,
    product_name,
    rating,
    rating_count
FROM amazon_products
WHERE rating > 4.5
ORDER BY rating DESC, rating_count DESC;


-- ============================================================
-- 12. COUNT OF PRODUCTS WITH RATING 4.5 OR HIGHER
-- ============================================================

SELECT
    COUNT(*) AS high_rated_products
FROM amazon_products
WHERE rating >= 4.5;


-- ============================================================
-- 13. PRODUCTS WITH DISCOUNT ABOVE 70%
-- ============================================================

SELECT
    product_id,
    product_name,
    discount_percentage,
    actual_price,
    discounted_price
FROM amazon_products
WHERE discount_percentage > 70
ORDER BY discount_percentage DESC;


-- ============================================================
-- 14. COUNT OF PRODUCTS WITH DISCOUNT ABOVE 70%
-- ============================================================

SELECT
    COUNT(*) AS products_above_70_percent_discount
FROM amazon_products
WHERE discount_percentage > 70;


-- ============================================================
-- 15. PRODUCTS COSTING ABOVE RS. 10,000
-- ============================================================

SELECT
    product_id,
    product_name,
    actual_price,
    discounted_price,
    discount_percentage
FROM amazon_products
WHERE discounted_price > 10000
ORDER BY discounted_price DESC;


-- ============================================================
-- 16. TOP 10 MOST EXPENSIVE PRODUCTS
-- ============================================================

SELECT
    product_id,
    product_name,
    actual_price,
    discounted_price,
    discount_percentage
FROM amazon_products
ORDER BY actual_price DESC
LIMIT 10;


-- ============================================================
-- 17. TOP 10 LOWEST PRICED PRODUCTS
-- ============================================================

SELECT
    product_id,
    product_name,
    actual_price,
    discounted_price
FROM amazon_products
ORDER BY discounted_price ASC
LIMIT 10;


-- ============================================================
-- 18. PRODUCTS WITH THE LARGEST PRICE SAVINGS
-- ============================================================

SELECT
    product_id,
    product_name,
    actual_price,
    discounted_price,
    ROUND(actual_price - discounted_price, 2) AS savings_amount,
    discount_percentage
FROM amazon_products
ORDER BY savings_amount DESC
LIMIT 10;


-- ============================================================
-- 19. AVERAGE ACTUAL PRICE
-- ============================================================

SELECT
    ROUND(AVG(actual_price), 2) AS average_actual_price
FROM amazon_products;


-- ============================================================
-- 20. AVERAGE DISCOUNTED PRICE
-- ============================================================

SELECT
    ROUND(AVG(discounted_price), 2) AS average_discounted_price
FROM amazon_products;


-- ============================================================
-- 21. CATEGORY-WISE PRODUCT COUNT
-- Uses the complete category path stored in the database
-- ============================================================

SELECT
    category,
    COUNT(*) AS total_products
FROM amazon_products
GROUP BY category
ORDER BY total_products DESC
LIMIT 10;


-- ============================================================
-- 22. CATEGORY-WISE AVERAGE RATING
-- ============================================================

SELECT
    category,
    COUNT(*) AS total_products,
    ROUND(AVG(rating), 2) AS average_rating
FROM amazon_products
GROUP BY category
ORDER BY average_rating DESC, total_products DESC
LIMIT 10;


-- ============================================================
-- 23. CATEGORY-WISE AVERAGE DISCOUNT
-- ============================================================

SELECT
    category,
    COUNT(*) AS total_products,
    ROUND(AVG(discount_percentage), 2) AS average_discount
FROM amazon_products
GROUP BY category
ORDER BY average_discount DESC
LIMIT 10;


-- ============================================================
-- 24. CATEGORY-WISE TOTAL REVIEWS
-- ============================================================

SELECT
    category,
    SUM(rating_count) AS total_reviews
FROM amazon_products
GROUP BY category
ORDER BY total_reviews DESC
LIMIT 10;


-- ============================================================
-- 25. RATING DISTRIBUTION
-- ============================================================

SELECT
    rating,
    COUNT(*) AS total_products
FROM amazon_products
GROUP BY rating
ORDER BY rating DESC;


-- ============================================================
-- 26. DISCOUNT RANGE ANALYSIS
-- ============================================================

SELECT
    CASE
        WHEN discount_percentage = 0 THEN 'No Discount'
        WHEN discount_percentage <= 20 THEN '1-20%'
        WHEN discount_percentage <= 40 THEN '21-40%'
        WHEN discount_percentage <= 60 THEN '41-60%'
        WHEN discount_percentage <= 80 THEN '61-80%'
        ELSE 'Above 80%'
    END AS discount_range,

    COUNT(*) AS total_products,

    ROUND(AVG(rating), 2) AS average_rating

FROM amazon_products

GROUP BY
    CASE
        WHEN discount_percentage = 0 THEN 'No Discount'
        WHEN discount_percentage <= 20 THEN '1-20%'
        WHEN discount_percentage <= 40 THEN '21-40%'
        WHEN discount_percentage <= 60 THEN '41-60%'
        WHEN discount_percentage <= 80 THEN '61-80%'
        ELSE 'Above 80%'
    END

ORDER BY MIN(discount_percentage);


-- ============================================================
-- 27. PRICE RANGE ANALYSIS
-- ============================================================

SELECT
    CASE
        WHEN discounted_price < 500 THEN 'Below Rs.500'
        WHEN discounted_price < 1000 THEN 'Rs.500 - Rs.999'
        WHEN discounted_price < 5000 THEN 'Rs.1,000 - Rs.4,999'
        WHEN discounted_price < 10000 THEN 'Rs.5,000 - Rs.9,999'
        ELSE 'Rs.10,000 and Above'
    END AS price_range,

    COUNT(*) AS total_products,

    ROUND(AVG(rating), 2) AS average_rating

FROM amazon_products

GROUP BY
    CASE
        WHEN discounted_price < 500 THEN 'Below Rs.500'
        WHEN discounted_price < 1000 THEN 'Rs.500 - Rs.999'
        WHEN discounted_price < 5000 THEN 'Rs.1,000 - Rs.4,999'
        WHEN discounted_price < 10000 THEN 'Rs.5,000 - Rs.9,999'
        ELSE 'Rs.10,000 and Above'
    END

ORDER BY MIN(discounted_price);


-- ============================================================
-- 28. HIGH RATING + HIGH REVIEW PRODUCTS
-- Strong-performing products
-- ============================================================

SELECT
    product_id,
    product_name,
    rating,
    rating_count,
    discounted_price
FROM amazon_products
WHERE rating >= 4.5
  AND rating_count >= 10000
ORDER BY rating_count DESC;


-- ============================================================
-- 29. HIGH DISCOUNT + HIGH RATING PRODUCTS
-- ============================================================

SELECT
    product_id,
    product_name,
    rating,
    discount_percentage,
    actual_price,
    discounted_price
FROM amazon_products
WHERE rating >= 4.0
  AND discount_percentage >= 70
ORDER BY rating DESC, discount_percentage DESC;


-- ============================================================
-- 30. COMPLETE DATABASE VALIDATION
-- ============================================================

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


-- ============================================================
-- END OF AMAZON PRODUCT BUSINESS ANALYSIS
-- ============================================================