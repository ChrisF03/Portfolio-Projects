-- 1) How many customers did we have each day?  

SELECT DISTINCT date, COUNT(Distinct order_id) as Total_Orders
FROM orders
GROUP BY date
 
-- 2) Were there any peak hours?

SELECT substring(Time, 0,4) || '00' as HOUR, COUNT(DISTINCT order_id) as Total_Orders
FROM orders
GROUP BY HOUR
ORDER BY Total_Orders DESC;

-- 3) How many pizzas were typically in an order? 

WITH orders_ AS (
SELECT DISTINCT order_id, SUM(quantity) as Total_Pizzas
FROM order_details
GROUP BY order_id
)
SELECT ROUND(AVG(Total_Pizzas)) as Avg_Pizzas_per_Order
FROM orders_

-- 4) Do we have any bestsellers?

SELECT DISTINCT p.pizza_type_id, SUM(od.quantity) as Amount_Sold
FROM order_details od 
JOIN pizzas p ON od.pizza_id = p.pizza_id
GROUP BY p.pizza_type_id
ORDER BY Amount_Sold DESC
LIMIT 3;

-- 5) How much money did we make this year? 

WITH Profits AS (
SELECT DISTINCT od.pizza_id, SUM(od.quantity) as Total_Sold, SUM(od.quantity) * p.price as Money_Made
FROM order_details od
JOIN pizzas p ON od.pizza_id = p.pizza_id
GROUP BY od.pizza_id
)
SELECT '$ ' || SUM(Money_Made) as Total_Profit
FROM Profits

-- 6) Can we indentify any seasonality in the sales?

SELECT substring(Date, 5,4) as Month, COUNT(DISTINCT order_id) as Total_Orders
FROM orders
GROUP BY Month
ORDER BY Total_Orders DESC;

-- 7) What was the average total per order ? 

WITH Order_Totals AS (
SELECT DISTINCT od.order_id, SUM(p.price) OVER (PARTITION BY od.order_id) as bill
FROM order_details od
JOIN pizzas p ON od.pizza_id = p.pizza_id
GROUP BY od.order_details_id
)
SELECT '$ ' || ROUND(AVG(bill),2) as AVERAGE_ORDER_TOTAL
FROM Order_Totals

-- 8) Which pizzas made us the most money ?

SELECT DISTINCT p.pizza_type_id, '$ ' || ROUND(SUM(p.price),2) as Revenue, SUM(od.quantity) as Amount_Sold
FROM order_details od 
JOIN pizzas p ON od.pizza_id = p.pizza_id
GROUP BY p.pizza_type_id
ORDER BY Revenue DESC
LIMIT 3;
