-- TITLE: BEST_DEAL_PROPERTIES
-- AUTHOR: Sophia Priola
-- This finds the best deals based on the city the user enters 
-- by finding properties under the average for the city they filtered
-- This is used to power the "Find me deals!" button in the 'Properties' page of our website

USE MAINEPAD;

-- We use view to build a derived table of the best deal properties
CREATE OR REPLACE VIEW BEST_DEAL_PROPERTIES AS
SELECT
    -- our basic info 
    P.PROPERTY_ID,
    P.UNIT_LABEL,
    P.RENT_COST,
    P.BEDROOMS,
    P.BATHROOMS,
    P.CAN_RENT,
    P.SQFT,
    -- location info 
    A.CITY,
    A.STATE_CODE,
    stats.avg_rent AS city_avg_rent,    -- average rent in this city 
    ROUND((P.RENT_COST / stats.avg_rent) * 100, 0) AS rent_pct_of_city_avg    -- how this unit compares to city average as a percentage 
FROM PROPERTY AS P
JOIN ADDRESS AS A
  ON P.ADDR_ID = A.ADDR_ID

-- our subquery calculates the average rent per city and only considers
-- unit that are currently available (CAN_RENT = 0).
JOIN (
    -- compute average rent per city for AVAILABLE units
    SELECT 
        A2.CITY,
        AVG(P2.RENT_COST) AS avg_rent
    FROM PROPERTY AS P2
    JOIN ADDRESS AS A2
      ON P2.ADDR_ID = A2.ADDR_ID
    WHERE P2.CAN_RENT = 0           -- only available
    GROUP BY A2.CITY
) AS stats
  ON stats.CITY = A.CITY
WHERE P.CAN_RENT = 0                 -- only currently available
  AND P.RENT_COST < stats.avg_rent;   -- finds properties less than the average rent 
