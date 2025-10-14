-- Prompt: “Using the Pagila dataset, find the top 3 customers by total amount spent. Let’s think step by step.”

-- Response:
-- To get total amount spent by each customer, we’ll need the payment table.
-- We'll join it to customer using customer_id, then group by customer,
-- sum the payment amounts, and sort by total. Finally, we’ll limit the result to the top 3.

SELECT c.first_name, c.last_name, SUM(p.amount) AS total_spent
FROM customer c
JOIN payment p ON c.customer_id = p.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY total_spent DESC
LIMIT 3;
