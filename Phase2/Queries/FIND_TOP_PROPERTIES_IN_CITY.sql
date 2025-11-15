-- TITLE: FIND_TOP_RATED_PROPETIES_IN_CITY
-- AUTHOR: Sophia Priola
-- Before optimization, find the top rated properties in a city and order them from greatest to least

SELECT 
    P.PROPERTY_ID,
    A.CITY,
    (
        SELECT AVG(R.STARS)  
        FROM REVIEW AS R
        WHERE R.PROPERTY_ID = P.PROPERTY_ID
    ) AS AVG_RATING
FROM PROPERTY AS P
JOIN ADDRESS AS A
    ON P.ADDR_ID = A.ADDR_ID
WHERE A.CITY = 'Portland'
ORDER BY AVG_RATING DESC; -- Orders largest to smallest 
-- Query runtime: 60.65ms before optimization

-- After optimization, find the top rated properties in a city and order them from greatest to least
SELECT 
    P.PROPERTY_ID,
    A.CITY,
    AVG(R.STARS) AS AVG_RATING
FROM PROPERTY AS P
JOIN ADDRESS AS A
    ON P.ADDR_ID = A.ADDR_ID
JOIN REVIEW AS R
    ON R.PROPERTY_ID = P.PROPERTY_ID
WHERE A.CITY = 'Portland'
GROUP BY 
    P.PROPERTY_ID,
    A.CITY
ORDER BY AVG_RATING DESC;

-- Query runtime after optimization: 43.55ms
