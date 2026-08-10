-- Gaming Product Analytics
-- Database setup and schema definition

DROP TABLE IF EXISTS game_analysis;

CREATE TABLE game_analysis (
    app_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    date_release TEXT,
    win TEXT,
    mac TEXT,
    linux TEXT,
    rating TEXT,
    positive_ratio INTEGER,
    user_reviews INTEGER,
    price_final REAL,
    price_original REAL,
    discount REAL,
    steam_deck TEXT,
    release_year INTEGER,
    price_type TEXT,
    is_discounted TEXT,
    total_reviews INTEGER,
    unique_reviewers INTEGER,
    recommendation_rate REAL,
    avg_hours REAL,
    median_hours REAL
);

DROP TABLE IF EXISTS reliable_games;

CREATE TABLE reliable_games (
    app_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    date_release TEXT,
    win TEXT,
    mac TEXT,
    linux TEXT,
    rating TEXT,
    positive_ratio INTEGER,
    user_reviews INTEGER,
    price_final REAL,
    price_original REAL,
    discount REAL,
    steam_deck TEXT,
    release_year INTEGER,
    price_type TEXT,
    is_discounted TEXT,
    total_reviews INTEGER,
    unique_reviewers INTEGER,
    recommendation_rate REAL,
    avg_hours REAL,
    median_hours REAL,
    performance_segment TEXT
);

.mode csv

.import --skip 1 data/processed/game_analysis.csv game_analysis
.import --skip 1 data/processed/reliable_games.csv reliable_games

SELECT 'game_analysis' AS table_name, COUNT(*) AS row_count
FROM game_analysis;

SELECT 'reliable_games' AS table_name, COUNT(*) AS row_count
FROM reliable_games;