-- Data Source : https://github.com/lerocha/chinook-database
-- In this project, I queried a database with multiple tables in it to quantify statistics about a digital media store.

--List all customers (full name, ID and country) who are not in the US.
SELECT FirstName, LastName, CustomerId, Country
FROM Customer
WHERE Country NOT LIKE '%USA%';

--Show only the Customers from Brazil.
SELECT *
FROM Customer
WHERE Country LIKE '%Brazil%';

--Find the Invoices of customers who are from Brazil. 
--The resulting table should show the customer's full name, Invoice ID, Date of the invoice, and billing country.
SELECT c.FirstName, c.LastName, i.InvoiceId, i.InvoiceDate, i.BillingCountry
FROM Customer as c
JOIN Invoice as i
ON c.CustomerId = i.CustomerId
WHERE i.BillingCountry = 'Brazil';

--Show the Employees who are Sales Agents.
SELECT *
FROM Employee
WHERE Title = "Sales Support Agent";

--Find a unique/distinct list of billing countries from the Invoice table.
SELECT DISTINCT BillingCountry
FROM Invoice;

--Provide a query that shows the invoices associated with each sales agent. The resulting table should include the Sales Agent's full name.
SELECT e.FirstName, e.LastName, i.InvoiceId
FROM Employee as e
JOIN Customer as c 
ON e.EmployeeId = c.SupportRepId
JOIN Invoice i 
ON c.CustomerId = i.CustomerID;

--Show the Invoice Total, Customer name, Country, and Sales Agent name for all invoices and customers.
SELECT i.Total, c.FirstName, c.LastName, c.Country, e.FirstName, e.LastName
FROM Invoice as i
JOIN Customer as c
ON i.CustomerId = c.CustomerId
JOIN Employee e
ON c.SupportRepId = e.EmployeeId;

--How many Invoices were there in 2009?
SELECT COUNT(*)
FROM Invoice
WHERE InvoiceDate LIKE '2009%';

--What are the total sales for 2009?
SELECT SUM(Total)
FROM Invoice
WHERE InvoiceDate BETWEEN '2009-01-01' AND '2009-12-31';

--Write a query that includes the purchased track name with each invoice line ID.
SELECT i.InvoiceLineId, t.Name
FROM InvoiceLine as i
JOIN Track as t
ON i.TrackId = t.TrackId;

--Write a query that includes the purchased track name AND artist name with each invoice line ID.
SELECT i.InvoiceLineId, t.Name AS Track, ar.Name AS Artist
FROM InvoiceLine as i
JOIN Track as t
ON i.TrackId = t.TrackId
JOIN Album as al
ON t.AlbumId = al.AlbumId
JOIN Artist ar
ON al.ArtistId = ar.ArtistID;

--Provide a query that shows all the Tracks, and include the Album name, Media type, and Genre.
SELECT t.Name AS Track, a.Title AS AlbumName, m.Name AS MediaType, g.Name As Genre
FROM Track as t
JOIN Album as a
ON t.AlbumId = a.AlbumId
JOIN MediaType as m
ON t.MediaTypeId = m.MediaTypeId
JOIN Genre as g
ON t.GenreId = g.GenreId;

--Show the total sales made by each sales agent.
SELECT e.FirstName, e.LastName, ROUND(sum(i.Total),2) AS 'Total Sales'
FROM Employee as e
JOIN Customer as c
ON e.EmployeeId = c.SupportRepId
JOIN Invoice as i
ON c.CustomerId = i.CustomerId
WHERE e.Title = "Sales Support Agent"
GROUP BY e.LastName;

--Which sales agent made the most dollars in sales in 2009?
SELECT e.FirstName, e.LastName, ROUND(sum(i.Total),2) AS 'Total Sales'
FROM Employee as e
JOIN Customer as c
ON e.EmployeeId = c.SupportRepId
JOIN Invoice as i
ON c.CustomerId = i.CustomerId
WHERE e.Title = "Sales Support Agent" AND i.InvoiceDate BETWEEN '2009-01-01' AND '2009-12-31'
GROUP BY e.LastName
ORDER BY ROUND(sum(i.Total),2) DESC
Limit 1;

--Which playlist(s) of songs costs the most money?
SELECT pt.PlaylistID, p.Name, (COUNT(pt.TrackId)*t.UnitPrice) AS TotalPrice
FROM PlaylistTrack as pt
JOIN Playlist as p
ON pt.PlaylistId = p.PlaylistId
JOIN Track as t
ON pt.TrackId = t.TrackId
GROUP BY pt.playlistID
ORDER BY TotalPrice DESC
LIMIT 2;

--Which album had the most song sales, how many songs were sold, and what is the artist of that album?
SELECT COUNT(i.TrackId) AS SongsSold, al.Title AS AlbumName, a.Name AS Artisit
FROM InvoiceLine as i
JOIN Track as t
ON i.TrackID = t.TrackId
JOIN Album as al
ON t.AlbumId = al.AlbumID
JOIN Artist as a
ON al.ArtistID = a.ArtistID
GROUP BY AlbumName
ORDER BY COUNT(i.TrackId) DESC
LIMIT 1;
