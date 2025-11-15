-- TITLE: FIND_TOP_RATED_PROPS_IN_CITY
-- AUTHOR: Sophia Priola
--   Compare an unoptimized and optimized version of a query that finds
--   the top-rated properties in a given city, ordered from highest to lowest
--   average star rating.
SELECT 
    P.PROPERTY_ID,    -- ID of the property
    A.CITY,           -- City that the property is located 
    (
    -- For each property row, compute the average STARS from REVIEW
        SELECT AVG(R.STARS)  
        FROM REVIEW AS R
        WHERE R.PROPERTY_ID = P.PROPERTY_ID
    ) AS AVG_RATING
FROM PROPERTY AS P
JOIN ADDRESS AS A
    ON P.ADDR_ID = A.ADDR_ID
WHERE A.CITY = 'Portland'    -- Only look at properties in 'Portland'
ORDER BY AVG_RATING DESC;    -- Display highest rated properties first 
-- Duration: 0.00139550 seconds

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
