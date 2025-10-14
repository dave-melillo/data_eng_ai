WITH RevenueCTE AS (
    SELECT c.customer_id, c.name, SUM(ol.price) AS total_revenue
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_lines ol ON o.order_id = ol.order_id
    WHERE o.date > NOW() - INTERVAL '30 days'
    GROUP BY c.customer_id, c.name
)
SELECT r.customer_id, r.name, r.total_revenue
FROM RevenueCTE r
JOIN customers c ON r.customer_id = c.customer_id
WHERE c.status = 'Active'
HAVING r.total_revenue > 200;
