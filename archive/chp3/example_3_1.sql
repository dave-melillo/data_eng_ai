SELECT c.customer_id, c.name, SUM(ol.price) AS total_revenue
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_lines ol ON o.order_id = ol.order_id
GROUP BY c.customer_id, c.name;
