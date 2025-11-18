DELIMITER $$

CREATE PROCEDURE CALL_ADD_PROPERTY_FOR_ALL()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE v_street VARCHAR(200);
    DECLARE v_city VARCHAR(100);
    DECLARE v_state CHAR(2);
    DECLARE v_zip CHAR(5);
    DECLARE v_unit VARCHAR(50);
    DECLARE v_rent INT;
    DECLARE v_sqft INT UNSIGNED;
    DECLARE v_bedrooms FLOAT(2,1);
    DECLARE v_bathrooms FLOAT(2,1);
    DECLARE v_can_rent TINYINT(1);

    DECLARE cur CURSOR FOR
        SELECT Street, City, State, Zipcode, Unit, Rent, SqFt, Bedrooms, Bathrooms, available
        FROM apartments;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO v_street, v_city, v_state, v_zip, v_unit, v_rent, v_sqft, v_bedrooms, v_bathrooms, v_can_rent;
        IF done THEN
            LEAVE read_loop;
        END IF;

        -- Call your procedure
        CALL ADD_PROPERTY(v_street, v_city, v_state, v_zip, v_unit, v_rent, v_sqft, v_bedrooms, v_bathrooms, v_can_rent);
    END LOOP;

    CLOSE cur;
END$$

DELIMITER ;

-- Then execute:
CALL CALL_ADD_PROPERTY_FOR_ALL();
DROP TABLE apartments
