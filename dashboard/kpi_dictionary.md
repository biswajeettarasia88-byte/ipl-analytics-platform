# Power BI KPI Dictionary

This document defines the exact logic and DAX/SQL formulations for the Key Performance Indicators (KPIs) displayed across the Power BI Dashboard.

## PAGE 1 — IPL OVERVIEW
- **Total Matches**: `COUNT(fact_matches[match_id])`
- **Total Seasons**: `DISTINCTCOUNT(fact_matches[season_sk])`
- **Total Teams**: `COUNTROWS(dim_team)`
- **Total Players**: `COUNTROWS(dim_player)`
- **Total Runs**: `SUM(fact_deliveries[batter_runs]) + SUM(fact_deliveries[extras_runs])`
- **Total Wickets**: `SUM(fact_deliveries[is_wicket])`
- **Average Score (First Innings)**: `AVERAGEX(SUMMARIZE(FILTER(fact_deliveries, fact_deliveries[innings] = 1), fact_deliveries[match_id], "Score", SUM(fact_deliveries[total_runs])), [Score])`
- **Chasing Win %**: `DIVIDE(CALCULATE(COUNT(fact_matches[match_id]), fact_matches[toss_decision] = "field" && fact_matches[toss_winner_sk] = fact_matches[winner_team_sk]), CALCULATE(COUNT(fact_matches[match_id]), fact_matches[toss_decision] = "field"))` *(Simplified logic: Total wins by team batting second / Total matches)*

## PAGE 2 — TEAM ANALYTICS
- **Win Percentage**: `DIVIDE(Total Wins, Total Matches Played)`
- **Powerplay Run Rate**: `DIVIDE(SUM(Powerplay Runs), SUM(Powerplay Overs))` where Overs <= 6.
- **Death Over Run Rate**: `DIVIDE(SUM(Death Overs Runs), SUM(Death Overs))` where Overs >= 16.

## PAGE 3 — PLAYER ANALYTICS
- **Batting Average**: `DIVIDE(Total Runs, Total Outs)`
- **Strike Rate**: `DIVIDE(Total Runs, Total Balls Faced) * 100`
- **Bowling Economy**: `DIVIDE(Total Runs Conceded, Total Overs Bowled)`
- **Player Consistency**: Percentage of innings where a batter scores 30+ runs.

## PAGE 4 — VENUE ANALYTICS
- **Average Score**: Average 1st innings total at the selected venue.
- **Batting-First Success**: Percentage of matches won by the team defending a total at the venue.

## PAGE 5 — MATCH ANALYTICS
- **Toss Impact**: Percentage of matches where the toss winner also won the match.
- **Close Matches**: Count of matches won by <= 5 runs or <= 2 wickets.
- **Early Wicket Impact**: Win percentage of teams that lose a wicket in over 0 (the first over).
