-- Before optimization
EXPLAIN ANALYZE
SELECT a.City, a.State_Code

       (
       SELECT COUNT(*)
       FROM PROPERTY p
       WHERE p.ADDR_ID = a.ADDR_ID
       AND p.RENT_COST BETWEEN 2500 AND 2600
       ) AS NumProperties,
(
       SELECT MIN(p.RENT_COST)
       FROM PROPERTY p 
       WHERE p.ADDR_ID = a.ADDR_ID
       AND p.RENT_COST BETWEEN 2500 AND 2600
       ) AS MinRent,
(
       SELECT MAX(p.RENT_COST)
       FROM PROPERTY p
       WHERE p.ADDR_ID = a.ADDR_ID
       AND p.RENT_COST BETWEEN 2500 AND 2600
       ) AS MaxRent 
FROM ADDRESS a
ORDER BY NumProperties DESC;

-- After optimization
EXPLAIN ANALYZE
SELECT a.City, a.State_Code, 
       COUNT(*) AS NumProperties,
       MIN(p.RENT_COST) AS MinRent,
       MAX(p.RENT_COST) AS MaxRent
FROM PROPERTY p
JOIN ADDRESS a ON p.ADDR_ID = a.ADDR_ID
WHERE p.RENT_COST BETWEEN 2500 AND 2600
GROUP BY a.City, a.State_Code
ORDER BY NumProperties DESC
