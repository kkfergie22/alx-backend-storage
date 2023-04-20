-- Create the stored procedure
DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser (IN p_user_id INT)
BEGIN
    -- Declare variables to hold the total score and count of corrections
    DECLARE total_score DECIMAL(10,2);
    DECLARE corrections_count INT;

    -- Calculate the total score and count of corrections for the given user
    SELECT SUM(score), COUNT(*) INTO total_score, corrections_count
    FROM corrections
    WHERE user_id = p_user_id;

    -- Calculate the average score and update the user's record in the users table
    IF corrections_count > 0 THEN
        SET @avg_score = total_score / corrections_count;
        UPDATE users SET average_score = @avg_score WHERE id = p_user_id;
    END IF;
END$$

-- Reset the delimiter to semicolon
DELIMITER ;
