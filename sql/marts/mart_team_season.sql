-- mart_team_season.sql
-- Aggregates team performance on a seasonal basis

CREATE OR REPLACE VIEW mart_team_season AS
WITH team_matches AS (
    SELECT 
        season_sk,
        team1_sk AS team_sk,
        CASE WHEN team1_sk = winner_team_sk THEN 1 ELSE 0 END AS won
    FROM fact_matches
    UNION ALL
    SELECT 
        season_sk,
        team2_sk AS team_sk,
        CASE WHEN team2_sk = winner_team_sk THEN 1 ELSE 0 END AS won
    FROM fact_matches
)
SELECT 
    season_sk,
    team_sk,
    COUNT(*) as total_matches,
    SUM(won) as total_wins,
    ROUND(SUM(won)::NUMERIC / COUNT(*), 4) AS win_rate
FROM team_matches
GROUP BY season_sk, team_sk;
