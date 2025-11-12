-- TITLE: Fosgate_ADD_MATCH
-- AUTHOR: Jeffrey Fosgate
-- DATE OF GITHUB COMMIT: 11/5/2025
-- A simple stored procedure for creating a new entry matching two roommates together.

DELIMITER $$
CREATE PROCEDURE ADD_MATCH (
    IN M_MATCH_ID INT UNSIGNED,
    IN M_RENTER_ID INT UNSIGNED
)
BEGIN
	INSERT INTO MATCHES
    VALUES (M_MATCH_ID, M_RENTER_ID);
END $$
