-- Gaming Product Analytics
-- Dashboard-ready views

DROP VIEW IF EXISTS vw_game_overview;

CREATE VIEW vw_game_overview AS
SELECT
    app_id,
    title,
    release_year,
    price_type,
    price_final,
    is_discounted,
    rating,
    positive_ratio,
    total_reviews,
    unique_reviewers,
    recommendation_rate,
    avg_hours,
    median_hours,
    performance_segment
FROM reliable_games;


DROP VIEW IF EXISTS vw_pricing_performance;

CREATE VIEW vw_pricing_performance AS
SELECT
    price_type,
    COUNT(*) AS games,
    ROUND(AVG(recommendation_rate), 2) AS avg_recommendation_rate,
    ROUND(AVG(median_hours), 2) AS avg_median_playtime,
    ROUND(AVG(total_reviews), 2) AS avg_reviews
FROM reliable_games
GROUP BY price_type;


DROP VIEW IF EXISTS vw_performance_segments;

CREATE VIEW vw_performance_segments AS
SELECT
    performance_segment,
    COUNT(*) AS games,
    ROUND(AVG(recommendation_rate), 2) AS avg_recommendation_rate,
    ROUND(AVG(median_hours), 2) AS avg_median_playtime,
    ROUND(AVG(total_reviews), 2) AS avg_reviews
FROM reliable_games
GROUP BY performance_segment;