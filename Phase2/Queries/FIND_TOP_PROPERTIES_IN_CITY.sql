-- TITLE: FIND_TOP_RATED_PROPS_IN_CITY
-- AUTHOR: Sophia Priola
-- Before optimization, find the top rated properties in a city and order them from largest to smallest 

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

-- After optimization, find the top rated properties in a city and order them from largest to smallest 
SELECT 
    P.PROPERTY_ID,
    A.CITY,
    AVG(R.RATING) AS AVG_RATING
FROM PROPERTY AS P
JOIN ADDRESS AS A
    ON A.ADDRESS_ID = P.PROP_ID
WHERE P.CITY = 'Portland'
GROUP BY 
    P.PROPERTY_ID,
    P.CITY
ORDER BY AVG_RATING DESC; -- Orders by largest to smallest 
