-- Monthly Revenue
SELECT
DATE_TRUNC('month', order_date) AS month,
SUM(price * quantity) AS revenue
FROM orders
GROUP BY month
ORDER BY month;


-- Revenue by Category
SELECT
category,
SUM(price * quantity) AS revenue
FROM orders
GROUP BY category
ORDER BY revenue DESC;


-- Top Products
SELECT
product,
SUM(quantity) AS units_sold
FROM orders
GROUP BY product
ORDER BY units_sold DESC
LIMIT 10;

-- Daily revenue
SELECT
order_date,
SUM(price * quantity) AS daily_revenue
FROM orders
GROUP BY order_date
ORDER BY order_date;

-- Running total revenue
SELECT
order_date,
SUM(price * quantity) AS daily_revenue,
SUM(SUM(price * quantity)) OVER (ORDER BY order_date) AS cumulative_revenue
FROM orders
GROUP BY order_date
ORDER BY order_date;


-- Customer purchase frequency
SELECT
customer_id,
COUNT(order_id) AS total_orders
FROM orders
GROUP BY customer_id
ORDER BY total_orders DESC
LIMIT 10;