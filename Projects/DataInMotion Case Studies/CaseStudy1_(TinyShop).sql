--**Query #1**
--1) Which product has the highest price? Only return a single row.
  
    SELECT product_name, 
    	   price
    FROM Products
    ORDER BY price DESC
    LIMIT 1;

| product_name | price |
| ------------ | ----- |
| Product M    | 70.00 |

--------------------------------------------------------------------------------------------
--**Query #2**
--2) Which customer has made the most orders?
  
    SELECT CONCAT(customers.first_name,' ',customers.last_name) as Name, 
    	   COUNT(DISTINCT orders.order_id) as Total_Orders
    FROM Customers
    JOIN Orders ON 
    customers.customer_id = orders.customer_id
    GROUP BY customers.customer_id 
    ORDER BY Total_orders DESC
    LIMIT 1;

| name     | total_orders |
| -------- | ------------ |
| John Doe | 2            |

--------------------------------------------------------------------------------------------
--**Query #3**
--3) What’s the total revenue per product?
  
    SELECT products.product_name,
    	   (products.price * SUM(order_items.quantity)) as Revenue
    FROM Products
    JOIN Order_items ON 
    Products.product_id = Order_items.product_id
    GROUP BY products.product_id
    ORDER BY Revenue DESC
    LIMIT 3;

| product_name | revenue |
| ------------ | ------- |
| Product M    | 420.00  |
| Product J    | 330.00  |
| Product F    | 210.00  |

--------------------------------------------------------------------------------------------
--**Query #4**
--4) Find the day with the highest revenue.

    SELECT orders.order_date, 
    	   SUM(products.price * order_items.quantity) as Revenue
    FROM Orders
    JOIN Order_items ON
    Orders.order_id = Order_items.order_id
    JOIN Products ON
    Products.product_id = Order_items.product_id
    GROUP BY orders.order_date
    ORDER BY Revenue DESC
    LIMIT 1;

| order_date               | revenue |
| ------------------------ | ------- |
| 2023-05-16T00:00:00.000Z | 340.00  |

--------------------------------------------------------------------------------------------
--**Query #5**
--5) Find the first order (by date) for each customer.
  
    SELECT customer_id, MIN(order_date) as First_Order
    FROM orders
    GROUP BY customer_id
    ORDER BY Customer_id;

| customer_id | first_order              |
| ----------- | ------------------------ |
| 1           | 2023-05-01T00:00:00.000Z |
| 2           | 2023-05-02T00:00:00.000Z |
| 3           | 2023-05-03T00:00:00.000Z |
| 4           | 2023-05-07T00:00:00.000Z |
| 5           | 2023-05-08T00:00:00.000Z |
| 6           | 2023-05-09T00:00:00.000Z |
| 7           | 2023-05-10T00:00:00.000Z |
| 8           | 2023-05-11T00:00:00.000Z |
| 9           | 2023-05-12T00:00:00.000Z |
| 10          | 2023-05-13T00:00:00.000Z |
| 11          | 2023-05-14T00:00:00.000Z |
| 12          | 2023-05-15T00:00:00.000Z |
| 13          | 2023-05-16T00:00:00.000Z |

--------------------------------------------------------------------------------------------
--**Query #6**
--6) Find the top 3 customers who have ordered the most distinct products
  
    SELECT CONCAT(customers.first_name,' ',customers.last_name) as Name, 	    COUNT(DISTINCT order_items.product_id) as Items_Bought
    FROM customers
    JOIN orders ON 
    customers.customer_id = orders.customer_id
    JOIN order_items ON 
    orders.order_id = order_items.order_id
    GROUP BY customers.customer_id
    ORDER BY Items_Bought DESC
    LIMIT 3;

| name        | items_bought |
| ----------- | ------------ |
| Jane Smith  | 3            |
| Bob Johnson | 3            |
| John Doe    | 3            |

--------------------------------------------------------------------------------------------
--**Query #7**
--7) Which product has been bought the least in terms of quantity?
  
    SELECT products.product_name, SUM(order_items.quantity) as Quantity
    FROM products
    JOIN order_items ON 
    products.product_id = order_items.product_id
    GROUP BY products.product_name, Quantity
    ORDER BY Quantity ASC
    LIMIT 3;

| product_name | quantity |
| ------------ | -------- |
| Product I    | 1        |
| Product E    | 1        |
| Product G    | 1        |

--------------------------------------------------------------------------------------------
--**Query #8**
--8) What is the median order total?
  
    WITH order_totals AS (
    SELECT order_items.order_id, SUM(products.price * order_items.quantity) AS Total
    FROM order_items 
    JOIN products ON
    order_items.product_id = products.product_id
    GROUP BY order_items.order_id
    ORDER BY order_items.order_id
    )
    SELECT PERCENTILE_CONT(0.5) WITHIN GROUP(ORDER BY total)
    FROM order_totals;

| percentile_cont |
| --------------- |
| 112.5           |

--------------------------------------------------------------------------------------------
--**Query #9**
--9) For each order, determine if it was ‘Expensive’ (total over 300), ‘Affordable’ (total over 100), or ‘Cheap’.
  
    WITH order_totals AS (
    SELECT order_items.order_id, SUM(products.price * order_items.quantity) AS Total
    FROM order_items 
    JOIN products ON
    order_items.product_id = products.product_id
    GROUP BY order_items.order_id
    ORDER BY order_items.order_id
    )
    SELECT order_id, CASE 
    	WHEN Total > 300 THEN 'Expensive'
        WHEN Total > 100 THEN 'Cheap'
        ELSE 'Cheap' END AS order_type
    FROM order_totals;

| order_id | order_type |
| -------- | ---------- |
| 1        | Cheap      |
| 2        | Cheap      |
| 3        | Cheap      |
| 4        | Cheap      |
| 5        | Cheap      |
| 6        | Cheap      |
| 7        | Cheap      |
| 8        | Cheap      |
| 9        | Cheap      |
| 10       | Cheap      |
| 11       | Cheap      |
| 12       | Cheap      |
| 13       | Cheap      |
| 14       | Cheap      |
| 15       | Cheap      |
| 16       | Expensive  |

--------------------------------------------------------------------------------------------
--**Query #10**
--10) Find customers who have ordered the product with the highest price.
  
    WITH customer AS (
    SELECT CONCAT(customers.first_name,' ',customers.last_name) as Name,
    	   orders.order_id
    FROM customers
    JOIN orders ON
    customers.customer_id = orders.customer_id
    GROUP BY orders.customer_id, Name, orders.order_id
    ORDER BY orders.customer_id
    )
    
    ,prices AS (
    SELECT order_items.order_id, 
      	   products.product_id, 
      	   products.price
    FROM order_items
    JOIN products ON
    products.product_id = order_items.product_id
    )
    
    SELECT Name, price
    FROM customer 
    JOIN prices ON
    customer.order_id = prices.order_id
    WHERE price = (
      SELECT MAX(price) FROM prices);

| name          | price |
| ------------- | ----- |
| Ivy Jones     | 70.00 |
| Sophia Thomas | 70.00 |

--------------------------------------------------------------------------------------------

--[View on DB Fiddle](https://www.db-fiddle.com/f/5NT4w4rBa1cvFayg2CxUjr/224)
