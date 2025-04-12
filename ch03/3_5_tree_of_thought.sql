-- Prompt: “Using the Pagila dataset, calculate the average rental duration by film category. Try at least two different approaches and recommend the clearer one.”

-- Response:

-- Approach 1 - direct aggregation
SELECT c.name, AVG(r.return_date - r.rental_date) AS avg_duration
FROM rental r
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film f ON i.film_id = f.film_id
JOIN film_category fc ON f.film_id = fc.film_id
JOIN category c ON fc.category_id = c.category_id
GROUP BY c.name;

-- Approach 2 - using a CTE for readability:
WITH rental_durations AS (
  SELECT fc.category_id, c.name AS category,
         (r.return_date - r.rental_date) AS duration
  FROM rental r
  JOIN inventory i ON r.inventory_id = i.inventory_id
  JOIN film f ON i.film_id = f.film_id
  JOIN film_category fc ON f.film_id = fc.film_id
  JOIN category c ON fc.category_id = c.category_id
)
SELECT category, AVG(duration) AS avg_duration
FROM rental_durations
GROUP BY category;

-- Evaluation:
-- “Both queries return the same result, but the second one separates data prep from aggregation,
-- making it easier to read and debug. I recommend the second version for maintainability.”
