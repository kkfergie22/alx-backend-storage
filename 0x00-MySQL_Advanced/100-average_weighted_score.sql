-- Create procedure to calculate weighted average

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_score INT;
    DECLARE total_weight INT;
    DECLARE avg_score DECIMAL(10,2);

    SELECT SUM(score * weight) INTO total_score, SUM(weight) INTO total_weight
    FROM corrections
    WHERE user_id = user_id;

    IF total_weight IS NOT NULL AND total_weight <> 0 THEN
        SET avg_score = total_score / total_weight;
    ELSE
        SET avg_score = 0;
    END IF;

    INSERT INTO average_weighted_scores (user_id, score) VALUES (user_id, avg_score)
    ON DUPLICATE KEY UPDATE score = avg_score;
END //

DELIMITER ;
