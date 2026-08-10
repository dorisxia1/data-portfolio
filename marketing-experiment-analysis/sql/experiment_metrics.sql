-- Marketing Experiment & Incrementality Analysis
-- Reproduce core A/B test metrics from the cleaned experiment data.

-- 1. Experiment group summary
SELECT
    "test group" AS experiment_group,
    COUNT(*) AS users,
    SUM(CASE WHEN converted = 1 THEN 1 ELSE 0 END) AS conversions,
    ROUND(
        100.0 * SUM(CASE WHEN converted = 1 THEN 1 ELSE 0 END) / COUNT(*),
        3
    ) AS conversion_rate_pct
FROM marketing_ab
GROUP BY "test group"
ORDER BY experiment_group;

-- 2. Treatment allocation
SELECT
    "test group" AS experiment_group,
    COUNT(*) AS users,
    ROUND(
        100.0 * COUNT(*) / SUM(COUNT(*)) OVER (),
        2
    ) AS allocation_pct
FROM marketing_ab
GROUP BY "test group"
ORDER BY users DESC;

-- 3. Conversion by exposure band
WITH exposure_bands AS (
    SELECT
        *,
        CASE
            WHEN "total ads" BETWEEN 1 AND 5 THEN '1–5'
            WHEN "total ads" BETWEEN 6 AND 10 THEN '6–10'
            WHEN "total ads" BETWEEN 11 AND 20 THEN '11–20'
            WHEN "total ads" BETWEEN 21 AND 30 THEN '21–30'
            WHEN "total ads" BETWEEN 31 AND 50 THEN '31–50'
            WHEN "total ads" BETWEEN 51 AND 100 THEN '51–100'
            WHEN "total ads" BETWEEN 101 AND 200 THEN '101–200'
            ELSE '201+'
        END AS exposure_band,
        CASE
            WHEN "total ads" BETWEEN 1 AND 5 THEN 1
            WHEN "total ads" BETWEEN 6 AND 10 THEN 2
            WHEN "total ads" BETWEEN 11 AND 20 THEN 3
            WHEN "total ads" BETWEEN 21 AND 30 THEN 4
            WHEN "total ads" BETWEEN 31 AND 50 THEN 5
            WHEN "total ads" BETWEEN 51 AND 100 THEN 6
            WHEN "total ads" BETWEEN 101 AND 200 THEN 7
            ELSE 8
        END AS exposure_order
    FROM marketing_ab
)

SELECT
    exposure_band,
    "test group" AS experiment_group,
    COUNT(*) AS users,
    SUM(CASE WHEN converted = 1 THEN 1 ELSE 0 END) AS conversions,
    ROUND(
        100.0 * SUM(CASE WHEN converted = 1 THEN 1 ELSE 0 END) / COUNT(*),
        3
    ) AS conversion_rate_pct
FROM exposure_bands
GROUP BY
    exposure_band,
    exposure_order,
    "test group"
ORDER BY
    exposure_order,
    experiment_group;

