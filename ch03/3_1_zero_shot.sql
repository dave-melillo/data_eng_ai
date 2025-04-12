-- Prompt: “Using the Pagila dataset, write a SQL query to list the top 5 most rented films.”
-- Response (SQL extracted):

SELECT f.title, COUNT(*) AS rental_count
FROM rental r
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film f ON i.film_id = f.film_id
GROUP BY f.title
ORDER BY rental_count DESC
LIMIT 5;
