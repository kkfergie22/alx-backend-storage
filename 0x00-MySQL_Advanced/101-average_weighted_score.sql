-- Task: Write a SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers that computes and store the average weighted score for all students.

-- Procedure to compute the average weighted score for all students
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE user_id INT;
    DECLARE total_score DECIMAL(10,2);
    DECLARE total_weight DECIMAL(10,2);
    DECLARE avg_score DECIMAL(10,2);
    DECLARE cur CURSOR FOR SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- Drop the average_weighted_score column if it already exists
    IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'users' AND COLUMN_NAME = 'average_weighted_score') THEN
        ALTER TABLE users DROP COLUMN average_weighted_score;
    END IF;

    -- Add the average_weighted_score column to the users table
    ALTER TABLE users ADD COLUMN average_weighted_score DECIMAL(10,2) AFTER total_score;

    -- Loop through all users
    OPEN cur;
    read_loop: LOOP
        FETCH cur INTO user_id;
        IF done THEN
            LEAVE read_loop;
        END IF;

        -- Compute the total score and weight for the user
        SET total_score = (SELECT SUM(score * weight) FROM corrections WHERE user_id = user_id);
        SET total_weight = (SELECT SUM(weight) FROM corrections WHERE user_id = user_id);

        -- Compute the average score for the user
        IF total_weight > 0 THEN
            SET avg_score = total_score / total_weight;
        ELSE
            SET avg_score = 0;
        END IF;

        -- Update the user's average weighted score
        UPDATE users SET average_weighted_score = avg_score WHERE id = user_id;
    END LOOP;
    CLOSE cur;
END //
DELIMITER ;
