-- 20 Analytical SQL Queries for IPL Data Warehouse
-- See docs/sql_insights.md for results and business interpretation.

-- 1. Top run scorers
SELECT batter, SUM(batter_runs) as total_runs
FROM fact_deliveries
GROUP BY batter
ORDER BY total_runs DESC
LIMIT 5;

-- 2. Top wicket takers
SELECT bowler, SUM(is_wicket) as total_wickets
FROM fact_deliveries
WHERE is_wicket = 1 AND wicket_type NOT IN ('run out', 'retired hurt', 'obstructing the field')
GROUP BY bowler
ORDER BY total_wickets DESC
LIMIT 5;

-- 3. Orange Cap by season
WITH SeasonRuns AS (
    SELECT m.season, d.batter, SUM(d.batter_runs) as runs
    FROM fact_deliveries d
    JOIN fact_matches m ON d.match_id = m.match_id
    GROUP BY m.season, d.batter
),
RankedScorers AS (
    SELECT season, batter, runs,
           RANK() OVER(PARTITION BY season ORDER BY runs DESC) as rnk
    FROM SeasonRuns
)
SELECT season, batter, runs
FROM RankedScorers
WHERE rnk = 1
ORDER BY season;

-- 4. Purple Cap by season
WITH SeasonWickets AS (
    SELECT m.season, d.bowler, SUM(d.is_wicket) as wickets
    FROM fact_deliveries d
    JOIN fact_matches m ON d.match_id = m.match_id
    WHERE d.is_wicket = 1 AND d.wicket_type NOT IN ('run out', 'retired hurt', 'obstructing the field')
    GROUP BY m.season, d.bowler
),
RankedBowlers AS (
    SELECT season, bowler, wickets,
           RANK() OVER(PARTITION BY season ORDER BY wickets DESC) as rnk
    FROM SeasonWickets
)
SELECT season, bowler, wickets
FROM RankedBowlers
WHERE rnk = 1
ORDER BY season;

-- 5. Team win percentage
WITH TeamMatches AS (
    SELECT team1 as team, match_id, winner FROM fact_matches WHERE team1 IS NOT NULL
    UNION ALL
    SELECT team2 as team, match_id, winner FROM fact_matches WHERE team2 IS NOT NULL
)
SELECT team, 
       COUNT(match_id) as total_matches,
       SUM(CASE WHEN team = winner THEN 1 ELSE 0 END) as total_wins,
       ROUND(CAST(SUM(CASE WHEN team = winner THEN 1 ELSE 0 END) AS FLOAT) / COUNT(match_id) * 100, 2) as win_pct
FROM TeamMatches
GROUP BY team
HAVING total_matches > 50
ORDER BY win_pct DESC;

-- 6. Team performance trends (Wins by Season)
WITH TeamSeasonWins AS (
    SELECT winner as team, season, COUNT(match_id) as wins
    FROM fact_matches
    WHERE winner IS NOT NULL AND winner != 'No Result'
    GROUP BY winner, season
)
SELECT team, season, wins,
       LAG(wins) OVER(PARTITION BY team ORDER BY season) as prev_season_wins
FROM TeamSeasonWins
WHERE team IN ('Chennai Super Kings', 'Mumbai Indians')
ORDER BY team, season;

-- 7. Toss impact
SELECT 
    COUNT(*) as total_matches,
    SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) as toss_and_match_winner,
    ROUND(CAST(SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100, 2) as toss_win_impact_pct
FROM fact_matches
WHERE winner != 'No Result';

-- 8. Venue advantage (Home team advantage approximation by Toss Winner = Home)
SELECT venue,
       COUNT(*) as matches_played,
       SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) as wins_by_toss_winner
FROM fact_matches
GROUP BY venue
ORDER BY matches_played DESC
LIMIT 5;

-- 9. Chasing success
SELECT 
    toss_decision,
    COUNT(*) as matches,
    SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) as wins,
    ROUND(CAST(SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100, 2) as win_pct
FROM fact_matches
WHERE toss_decision IN ('bat', 'field') AND winner != 'No Result'
GROUP BY toss_decision;

-- 10. Powerplay performance (Overs 1-6)
SELECT batting_team,
       SUM(total_runs) as powerplay_runs,
       COUNT(DISTINCT match_id) as matches,
       ROUND(CAST(SUM(total_runs) AS FLOAT) / COUNT(DISTINCT match_id), 2) as avg_powerplay_score
FROM fact_deliveries
WHERE over < 6
GROUP BY batting_team
ORDER BY avg_powerplay_score DESC
LIMIT 5;

-- 11. Death-over performance (Overs 16-20)
SELECT batting_team,
       SUM(total_runs) as death_runs,
       COUNT(DISTINCT match_id) as matches,
       ROUND(CAST(SUM(total_runs) AS FLOAT) / COUNT(DISTINCT match_id), 2) as avg_death_score
FROM fact_deliveries
WHERE over >= 15
GROUP BY batting_team
ORDER BY avg_death_score DESC
LIMIT 5;

-- 12. Player consistency (30+ scores)
WITH BatterMatchScores AS (
    SELECT batter, match_id, SUM(batter_runs) as match_runs
    FROM fact_deliveries
    GROUP BY batter, match_id
)
SELECT batter,
       COUNT(match_id) as innings_played,
       SUM(CASE WHEN match_runs >= 30 THEN 1 ELSE 0 END) as scores_30_plus,
       ROUND(CAST(SUM(CASE WHEN match_runs >= 30 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(match_id) * 100, 2) as consistency_pct
FROM BatterMatchScores
GROUP BY batter
HAVING innings_played > 50
ORDER BY consistency_pct DESC
LIMIT 5;

-- 13. Player-vs-team performance
SELECT batter, bowling_team, SUM(batter_runs) as total_runs
FROM fact_deliveries
WHERE batter = 'V Kohli'
GROUP BY batter, bowling_team
ORDER BY total_runs DESC
LIMIT 5;

-- 14. Player-vs-venue performance
SELECT d.batter, m.venue, SUM(d.batter_runs) as runs
FROM fact_deliveries d
JOIN fact_matches m ON d.match_id = m.match_id
WHERE d.batter = 'RG Sharma'
GROUP BY d.batter, m.venue
ORDER BY runs DESC
LIMIT 5;

-- 15. Winning margins (Average margin by runs)
SELECT winner,
       AVG(win_margin_runs) as avg_win_margin_runs
FROM fact_matches
WHERE result_type = 'runs'
GROUP BY winner
ORDER BY avg_win_margin_runs DESC
LIMIT 5;

-- 16. Close matches (Won by <= 5 runs or <= 2 wickets)
SELECT winner, COUNT(*) as close_wins
FROM fact_matches
WHERE (result_type = 'runs' AND win_margin_runs <= 5)
   OR (result_type = 'wickets' AND win_margin_wickets <= 2)
GROUP BY winner
ORDER BY close_wins DESC
LIMIT 5;

-- 17. Early wicket impact (Lost wicket in 1st over)
WITH WicketFirstOver AS (
    SELECT DISTINCT match_id, batting_team
    FROM fact_deliveries
    WHERE over = 0 AND is_wicket = 1
)
SELECT COUNT(w.match_id) as matches_with_early_wicket,
       SUM(CASE WHEN w.batting_team = m.winner THEN 1 ELSE 0 END) as wins_despite_early_wicket,
       ROUND(CAST(SUM(CASE WHEN w.batting_team = m.winner THEN 1 ELSE 0 END) AS FLOAT) / COUNT(w.match_id) * 100, 2) as win_pct
FROM WicketFirstOver w
JOIN fact_matches m ON w.match_id = m.match_id;

-- 18. Target-range success (180+ targets)
WITH FirstInnings AS (
    SELECT match_id, SUM(total_runs) as target_score
    FROM fact_deliveries
    WHERE innings = 1
    GROUP BY match_id
),
SecondInningsTeam AS (
    SELECT DISTINCT match_id, batting_team as chasing_team
    FROM fact_deliveries
    WHERE innings = 2
)
SELECT 
    COUNT(*) as total_180_chases,
    SUM(CASE WHEN s.chasing_team = m.winner THEN 1 ELSE 0 END) as successful_chases,
    ROUND(CAST(SUM(CASE WHEN s.chasing_team = m.winner THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100, 2) as success_pct
FROM FirstInnings f
JOIN SecondInningsTeam s ON f.match_id = s.match_id
JOIN fact_matches m ON f.match_id = m.match_id
WHERE f.target_score >= 180;

-- 19. Team recent form (Rolling 5 matches win pct)
WITH MatchResults AS (
    SELECT date, winner, team1, team2
    FROM fact_matches
    WHERE winner != 'No Result'
),
TeamMatches AS (
    SELECT date, team1 as team, CASE WHEN winner = team1 THEN 1 ELSE 0 END as won FROM MatchResults
    UNION ALL
    SELECT date, team2 as team, CASE WHEN winner = team2 THEN 1 ELSE 0 END as won FROM MatchResults
),
RollingForm AS (
    SELECT team, date, won,
           AVG(won) OVER (PARTITION BY team ORDER BY date ROWS BETWEEN 4 PRECEDING AND CURRENT ROW) as rolling_win_pct
    FROM TeamMatches
)
SELECT team, date, ROUND(rolling_win_pct * 100, 2) as form_pct
FROM RollingForm
WHERE team = 'Chennai Super Kings'
ORDER BY date DESC
LIMIT 5;

-- 20. Performance comparison (Batting Average vs Strike Rate)
WITH BatterStats AS (
    SELECT batter, 
           SUM(batter_runs) as runs, 
           COUNT(*) as balls,
           SUM(is_wicket) as outs
    FROM fact_deliveries
    GROUP BY batter
    HAVING runs > 1000
)
SELECT batter, 
       runs,
       ROUND(CAST(runs AS FLOAT) / NULLIF(outs, 0), 2) as batting_average,
       ROUND(CAST(runs AS FLOAT) / balls * 100, 2) as strike_rate
FROM BatterStats
ORDER BY strike_rate DESC
LIMIT 5;
