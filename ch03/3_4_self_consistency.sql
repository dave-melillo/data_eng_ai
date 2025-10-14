-- Prompt: “Using the Pagila dataset, how many customers have rented more than 10 times? Try solving this two different ways.”

-- Response (Version 1):
SELECT COUNT(*) 
FROM (
  SELECT customer_id
  FROM rental
  GROUP BY customer_id
  HAVING COUNT(*) > 10
) AS sub;

-- Response (Version 2):
WITH rental_counts AS (
  SELECT customer_id, COUNT(*) AS rental_count
  FROM rental
  GROUP BY customer_id
)
SELECT COUNT(*) 
FROM rental_counts
WHERE rental_count > 10;
