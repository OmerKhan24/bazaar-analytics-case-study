--  1. Total Number of Orders
SELECT COUNT(DISTINCT order_number) AS total_orders
FROM [Data Analytics Internship Dataset - Bazaar];

--  2. Total Sales Revenue
SELECT 
    SUM(ordered_quantity * (amount_per_unit - item_discount)) AS total_sales_revenue
FROM [Data Analytics Internship Dataset - Bazaar];

--  3. Average Order Value (AOV)
SELECT 
    SUM(ordered_quantity * (amount_per_unit - item_discount)) / COUNT(DISTINCT order_number) AS average_order_value
FROM [Data Analytics Internship Dataset - Bazaar];

--  4. Distribution of Orders by Warehouse and Store
SELECT 
    order_warehouse_id,
    store_id,
    COUNT(DISTINCT order_number) AS order_count
FROM [Data Analytics Internship Dataset - Bazaar]
GROUP BY order_warehouse_id, store_id
ORDER BY order_count DESC;

--  5. Top 5 Selling Items
SELECT 
    item_id,
    item_name,
    SUM(ordered_quantity) AS total_quantity_sold
FROM [Data Analytics Internship Dataset - Bazaar]
GROUP BY item_id, item_name
ORDER BY total_quantity_sold DESC
LIMIT 5;
