-- IPL Analytics Platform DDL Script
-- Target: PostgreSQL
-- Type: Dimensional Model (Star Schema)

-- ==========================================
-- DIMENSION TABLES
-- ==========================================

CREATE TABLE IF NOT EXISTS dim_team (
    team_sk SERIAL PRIMARY KEY,
    team_name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_player (
    player_sk SERIAL PRIMARY KEY,
    player_id VARCHAR(50) UNIQUE NOT NULL,
    player_name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_venue (
    venue_sk SERIAL PRIMARY KEY,
    venue_name VARCHAR(150) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_season (
    season_sk SERIAL PRIMARY KEY,
    season VARCHAR(20) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_date (
    date_sk SERIAL PRIMARY KEY,
    full_date DATE UNIQUE NOT NULL,
    year INT NOT NULL,
    month INT NOT NULL,
    day INT NOT NULL,
    day_of_week VARCHAR(15) NOT NULL
);

-- ==========================================
-- FACT TABLES
-- ==========================================

CREATE TABLE IF NOT EXISTS fact_matches (
    match_id VARCHAR(50) PRIMARY KEY,
    season_sk INT NOT NULL REFERENCES dim_season(season_sk),
    date_sk INT NOT NULL REFERENCES dim_date(date_sk),
    venue_sk INT NOT NULL REFERENCES dim_venue(venue_sk),
    city VARCHAR(100),
    team1_sk INT NOT NULL REFERENCES dim_team(team_sk),
    team2_sk INT NOT NULL REFERENCES dim_team(team_sk),
    toss_winner_sk INT REFERENCES dim_team(team_sk),
    toss_decision VARCHAR(20),
    winner_team_sk INT REFERENCES dim_team(team_sk),
    result_type VARCHAR(20),
    win_margin_runs INT,
    win_margin_wickets INT,
    player_of_match_sk INT REFERENCES dim_player(player_sk)
);

CREATE TABLE IF NOT EXISTS fact_match_teams (
    match_id VARCHAR(50) REFERENCES fact_matches(match_id),
    team_sk INT REFERENCES dim_team(team_sk),
    is_home_team BOOLEAN,
    PRIMARY KEY (match_id, team_sk)
);

CREATE TABLE IF NOT EXISTS fact_deliveries (
    delivery_sk SERIAL PRIMARY KEY,
    match_id VARCHAR(50) NOT NULL REFERENCES fact_matches(match_id),
    innings INT NOT NULL,
    over_num INT NOT NULL,
    ball_num INT NOT NULL,
    batting_team_sk INT NOT NULL REFERENCES dim_team(team_sk),
    bowling_team_sk INT NOT NULL REFERENCES dim_team(team_sk),
    batter_sk INT NOT NULL REFERENCES dim_player(player_sk),
    bowler_sk INT NOT NULL REFERENCES dim_player(player_sk),
    non_striker_sk INT NOT NULL REFERENCES dim_player(player_sk),
    batter_runs INT NOT NULL,
    extras_runs INT NOT NULL,
    total_runs INT NOT NULL,
    extras_type VARCHAR(50),
    is_wicket INT NOT NULL,
    wicket_type VARCHAR(50),
    dismissed_player_sk INT REFERENCES dim_player(player_sk),
    UNIQUE (match_id, innings, over_num, ball_num)
);

CREATE TABLE IF NOT EXISTS fact_player_match_performance (
    performance_sk SERIAL PRIMARY KEY,
    match_id VARCHAR(50) NOT NULL REFERENCES fact_matches(match_id),
    player_sk INT NOT NULL REFERENCES dim_player(player_sk),
    team_sk INT NOT NULL REFERENCES dim_team(team_sk),
    runs_scored INT DEFAULT 0,
    balls_faced INT DEFAULT 0,
    fours INT DEFAULT 0,
    sixes INT DEFAULT 0,
    wickets_taken INT DEFAULT 0,
    runs_conceded INT DEFAULT 0,
    balls_bowled INT DEFAULT 0,
    catches INT DEFAULT 0,
    run_outs INT DEFAULT 0,
    UNIQUE (match_id, player_sk)
);

-- ==========================================
-- INDEXES
-- ==========================================
CREATE INDEX idx_fact_matches_season ON fact_matches(season_sk);
CREATE INDEX idx_fact_matches_venue ON fact_matches(venue_sk);
CREATE INDEX idx_fact_matches_teams ON fact_matches(team1_sk, team2_sk);
CREATE INDEX idx_fact_deliveries_match ON fact_deliveries(match_id);
CREATE INDEX idx_fact_deliveries_batter ON fact_deliveries(batter_sk);
CREATE INDEX idx_fact_deliveries_bowler ON fact_deliveries(bowler_sk);
CREATE INDEX idx_perf_player ON fact_player_match_performance(player_sk);
