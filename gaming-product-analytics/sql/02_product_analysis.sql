-- Gaming Product Analytics
-- Product analysis queries

-- 1. Overview of the reliable game sample
SELECT
    COUNT(*) AS total_games,
    ROUND(AVG(recommendation_rate), 2) AS avg_recommendation_rate,
    ROUND(AVG(median_hours), 2) AS avg_median_playtime,
    ROUND(AVG(total_reviews), 2) AS avg_reviews
FROM reliable_games;


-- 2. Compare free vs. paid game performance
SELECT
    price_type,
    COUNT(*) AS games,
    ROUND(AVG(recommendation_rate), 2) AS avg_recommendation_rate,
    ROUND(AVG(median_hours), 2) AS avg_median_playtime,
    ROUND(AVG(total_reviews), 2) AS avg_reviews
FROM reliable_games
GROUP BY price_type
ORDER BY avg_median_playtime DESC;


-- 3. Recreate performance segments using sample benchmarks
WITH benchmarks AS (
    SELECT
        84.21 AS recommendation_benchmark,
        6.30 AS engagement_benchmark
),
segmented_games AS (
    SELECT
        r.app_id,
        r.title,
        r.recommendation_rate,
        r.median_hours,
        r.total_reviews,
        CASE
            WHEN r.recommendation_rate >= b.recommendation_benchmark
                 AND r.median_hours >= b.engagement_benchmark
                THEN 'High Satisfaction / High Engagement'

            WHEN r.recommendation_rate >= b.recommendation_benchmark
                 AND r.median_hours < b.engagement_benchmark
                THEN 'High Satisfaction / Low Engagement'

            WHEN r.recommendation_rate < b.recommendation_benchmark
                 AND r.median_hours >= b.engagement_benchmark
                THEN 'Low Satisfaction / High Engagement'

            ELSE 'Low Satisfaction / Low Engagement'
        END AS performance_segment
    FROM reliable_games r
    CROSS JOIN benchmarks b
)
SELECT
    performance_segment,
    COUNT(*) AS games,
    ROUND(AVG(recommendation_rate), 2) AS avg_recommendation_rate,
    ROUND(AVG(median_hours), 2) AS avg_median_playtime,
    ROUND(AVG(total_reviews), 2) AS avg_reviews
FROM segmented_games
GROUP BY performance_segment
ORDER BY games DESC;


-- 4. Identify large-scale high-engagement games with below-median satisfaction
WITH benchmarks AS (
    SELECT
        84.21 AS recommendation_benchmark,
        6.30 AS engagement_benchmark
)
SELECT
    r.title,
    ROUND(r.recommendation_rate, 2) AS recommendation_rate,
    ROUND(r.median_hours, 1) AS median_hours,
    r.total_reviews,
    ROUND(r.price_final, 2) AS price_final
FROM reliable_games r
CROSS JOIN benchmarks b
WHERE r.recommendation_rate < b.recommendation_benchmark
  AND r.median_hours >= b.engagement_benchmark
ORDER BY r.total_reviews DESC
LIMIT 15;


-- 5. Rank games within each pricing model by recommendation rate
-- using a window function to compare strong performers fairly
WITH ranked_games AS (
    SELECT
        title,
        price_type,
        recommendation_rate,
        median_hours,
        total_reviews,
        ROW_NUMBER() OVER (
            PARTITION BY price_type
            ORDER BY recommendation_rate DESC, total_reviews DESC
        ) AS rank_within_price_type
    FROM reliable_games
    WHERE total_reviews >= 500
)
SELECT
    price_type,
    rank_within_price_type,
    title,
    ROUND(recommendation_rate, 2) AS recommendation_rate,
    ROUND(median_hours, 1) AS median_hours,
    total_reviews
FROM ranked_games
WHERE rank_within_price_type <= 10
ORDER BY
    price_type,
    rank_within_price_type;

