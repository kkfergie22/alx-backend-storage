-- Create SafeDiv Function

CREATE FUNCTION SafeDiv(a INT, b INT)
RETURNS INT
BEGIN
    DECLARE result INT DEFAULT 0;
    IF b != 0 THEN
        SET result = a / b;
    END IF;
    RETURN result;
END;
