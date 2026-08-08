# Power BI KPI Dictionary

This document defines the exact logic and DAX/SQL formulations for the Key Performance Indicators (KPIs) displayed across the Power BI Dashboard.

## PAGE 1 — IPL OVERVIEW
- **Total Matches**: `DISTINCTCOUNT(fact_matches[match_id])`
- **Total Seasons**: `DISTINCTCOUNT(fact_matches[season_sk])`
- **Total Teams**: `COUNTROWS(dim_team)`
- **Total Players**: `COUNTROWS(dim_player)`
- **Total Runs**: `SUM(fact_deliveries[total_runs])` *(Uses pre-aggregated total_runs column)*
- **Total Wickets**: `SUM(fact_deliveries[is_wicket])`
- **Average Score (First Innings)**: `AVERAGEX(SUMMARIZE(FILTER(fact_deliveries, fact_deliveries[innings] = 1), fact_deliveries[match_id], "Score", SUM(fact_deliveries[total_runs])), [Score])`
- **Chasing Win %**: 
  - **SQL**: `SUM(CASE WHEN chasing_team_sk = winner_team_sk THEN 1 ELSE 0 END) / COUNT(match_id)` (Derived from joining `fact_deliveries` innings 2).
  - **DAX Approximation**: `DIVIDE(CALCULATE(COUNT(fact_matches[match_id]), fact_matches[win_margin_wickets] > 0), CALCULATE(COUNT(fact_matches[match_id]), fact_matches[result_type] <> "no result"))`

## PAGE 2 — TEAM ANALYTICS
- **Win Percentage**: `DIVIDE(CALCULATE(COUNT(fact_matches[match_id]), fact_matches[winner_team_sk] = SELECTEDVALUE(dim_team[team_sk])), Total Matches Played)`
- **Powerplay Run Rate**: `DIVIDE(SUM(fact_deliveries[total_runs]) * 6, COUNT(fact_deliveries[delivery_sk]))` where `over_num <= 5` *(0-indexed)*.
- **Death Over Run Rate**: `DIVIDE(SUM(fact_deliveries[total_runs]) * 6, COUNT(fact_deliveries[delivery_sk]))` where `over_num >= 15`.

## PAGE 3 — PLAYER ANALYTICS
- **Batting Average**: `DIVIDE(SUM(fact_deliveries[batter_runs]), SUM(fact_deliveries[is_wicket]))` *(Assuming wicket applies to batter)*.
- **Strike Rate**: `DIVIDE(SUM(fact_deliveries[batter_runs]), CALCULATE(COUNT(fact_deliveries[delivery_sk]), fact_deliveries[extras_type] <> "wides")) * 100`
- **Bowling Economy**: `DIVIDE(SUM(fact_deliveries[total_runs]) * 6, CALCULATE(COUNT(fact_deliveries[delivery_sk]), fact_deliveries[extras_type] IN {BLANK(), "legbyes", "byes"}))`
- **Player Consistency**: Percentage of innings where a batter scores 30+ runs.

## PAGE 4 — VENUE ANALYTICS
- **Average Score**: Average 1st innings total at the selected venue.
- **Batting-First Success**: `DIVIDE(CALCULATE(COUNT(fact_matches[match_id]), fact_matches[win_margin_runs] > 0), CALCULATE(COUNT(fact_matches[match_id]), fact_matches[result_type] <> "no result"))`

## PAGE 5 — MATCH ANALYTICS
- **Toss Impact**: `DIVIDE(CALCULATE(COUNT(fact_matches[match_id]), fact_matches[toss_winner_sk] = fact_matches[winner_team_sk]), COUNT(fact_matches[match_id]))`
- **Close Matches**: `CALCULATE(COUNT(fact_matches[match_id]), fact_matches[win_margin_runs] <= 5 || fact_matches[win_margin_wickets] <= 2)`
- **Early Wicket Impact**: Win percentage of teams that lose a wicket in `over_num = 0`.
