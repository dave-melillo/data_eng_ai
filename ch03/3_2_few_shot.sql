-- Prompt: “Using the Pagila dataset and the structure of SQL queries below, generate a new SQL query for Report: Most rented categories”
-- Report: Most active customers

-- WITH customer_rentals AS (
--   SELECT customer_id, COUNT(*) AS rental_count
--   FROM rental
--   GROUP BY customer_id
-- )
-- SELECT customer_id, rental_count
-- FROM customer_rentals
-- ORDER BY rental_count DESC
-- LIMIT 5;

-- Report: Highest-grossing stores

-- WITH store_revenue AS (
--   SELECT s.store_id, SUM(p.amount) AS revenue
--   FROM payment p
--   JOIN staff s ON p.staff_id = s.staff_id
--   GROUP BY s.store_id
-- )
-- SELECT store_id, revenue
-- FROM store_revenue
-- ORDER BY revenue DESC;

-- Response:

WITH category_rentals AS (
  SELECT c.name AS category, COUNT(*) AS rental_count
  FROM rental r
  JOIN inventory i ON r.inventory_id = i.inventory_id
  JOIN film f ON i.film_id = f.film_id
  JOIN film_category fc ON f.film_id = fc.film_id
  JOIN category c ON fc.category_id = c.category_id
  GROUP BY c.name
)
SELECT category, rental_count
FROM category_rentals
ORDER BY rental_count DESC;
