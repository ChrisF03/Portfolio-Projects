# Plato's Pizzeria Sales Analysis
### *Tools Used: Excel, SQL, Tableau*

Dashboard Link : [Coming Soon](https://public.tableau.com/app/profile/chrisf03)

For this project, I took on the role of a data analyst for Plato's Pizzeria, a Greek-inspired pizza place in New Jersey.
<br><br>
Plato's has been collecting [transactional data](https://mavenanalytics.io/challenges/maven-pizza-challenge/4) for the past year, but really haven't been able to put it to good use. <br><br>Tasked with analyzing the data and putting together a report to help them find opportunities to drive more sales and work more efficiently, here are some questions that I came up with and answered using SQL : 

<b> 1) How many customers did we have each day? </b> 
```sql
SELECT DISTINCT date, COUNT(Distinct order_id) as Total_Orders
FROM orders
GROUP BY date
```
OUTPUT: 

|date|Total_Orders|
|----|------------|
|2015-01-01|69|
|2015-01-02|67|
|2015-01-03|66|
|2015-01-04|52|
|...|...|

<b> 2) Were there any peak hours? </b>
```sql
SELECT substring(Time, 0,4) || '00' as HOUR, COUNT(DISTINCT order_id) as Total_Orders
FROM orders
GROUP BY HOUR
ORDER BY Total_Orders DESC;
```
OUTPUT:

|HOUR|Total_Orders|
|----|------------|
|12:00|2520|
|13:00|2455|
|18:00|2399|
|17:00|2336|
|...|...|

<b> 3) How many pizzas were typically in an order? </b>
```sql
WITH orders_ AS (
SELECT DISTINCT order_id, SUM(quantity) as Total_Pizzas
FROM order_details
GROUP BY order_id
)
SELECT ROUND(AVG(Total_Pizzas)) as Avg_Pizzas_per_Order
FROM orders_
```
OUTPUT: 

|Avg_Pizzas_per_Order|
|------------|
|2.0|

<b> 4) Do we have any bestsellers? </b>
```sql
SELECT DISTINCT p.pizza_type_id, SUM(od.quantity) as Amount_Sold
FROM order_details od 
JOIN pizzas p ON od.pizza_id = p.pizza_id
GROUP BY p.pizza_type_id
ORDER BY Amount_Sold DESC
LIMIT 3;
```
OUTPUT:

|pizza_type_id|Amount_Sold|
|-------------|-----------|
|classic_dlx|2453|
|bbq_ckn|2432|
|hawaiian|2422|

<b> 5) How much money did we make this year? </b>
```sql
WITH Profits AS (
SELECT DISTINCT od.pizza_id, SUM(od.quantity) as Total_Sold, SUM(od.quantity) * p.price as Money_Made
FROM order_details od
JOIN pizzas p ON od.pizza_id = p.pizza_id
GROUP BY od.pizza_id
)
SELECT '$ ' || SUM(Money_Made) as Total_Profit
FROM Profits
```
OUTPUT:

|Total_Profit|
|------------|
|$ 817,860.05|

<b> 6) Can we indentify any seasonality in the sales? </b>
```sql
SELECT substring(Date, 5,4) as Month, COUNT(DISTINCT order_id) as Total_Orders
FROM orders
GROUP BY Month
ORDER BY Total_Orders DESC;
```
OUTPUT:

|Month|Total_Orders|
|----|------------|
|-07-|1935|
|-05-|2455|
|-01-|2399|
|-08-|2336|
|...|...|

<b> 7) What was the average total per order ? </b>
```sql
WITH Order_Totals AS (
SELECT DISTINCT od.order_id, SUM(p.price) OVER (PARTITION BY od.order_id) as bill
FROM order_details od
JOIN pizzas p ON od.pizza_id = p.pizza_id
GROUP BY od.order_details_id
)
SELECT '$ ' || ROUND(AVG(bill),2) as AVERAGE_ORDER_TOTAL
FROM Order_Totals
```
OUTPUT:

|AVERAGE_ORDER_TOTAL|
|------------|
|$ 37.56|

<b> 8) Which pizzas made us the most money ? </b>
```sql
SELECT DISTINCT p.pizza_type_id, '$ ' || ROUND(SUM(p.price),2) as Revenue, SUM(od.quantity) as Amount_Sold
FROM order_details od 
JOIN pizzas p ON od.pizza_id = p.pizza_id
GROUP BY p.pizza_type_id
ORDER BY Revenue DESC
LIMIT 3;
```
OUTPUT:

|pizza_type_id|Revenue|Amount_Sold|
|-------------|-------|-----------|
|thai_ckn|$ 42,332.25|2371|
|bbq_ckn|$ 41,683.00|2432|
|cali_ckn|$ 40,166.50|2370|
|...|...|...|

