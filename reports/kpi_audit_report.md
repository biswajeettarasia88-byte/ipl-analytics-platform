# Power BI KPI Audit Report

## Executive Summary
A comprehensive audit of the `kpi_dictionary.md` was conducted against the actual PostgreSQL star schema. Most standard aggregations (Total Runs, Wickets, Matches) were correctly defined. However, the `Chasing Win %` metric contained a critical logical flaw, incorrectly defining a chasing match based solely on the `toss_decision`. This has been identified and structurally corrected. 

## Database Schema Used
The audit relies strictly on the current project schema defined in `sql/ddl/schema.sql`, which includes `fact_matches`, `fact_deliveries`, `fact_match_teams`, `dim_team`, `dim_player`, and `dim_venue`.

## KPI Audit Table

| KPI | Current Definition | Correct Definition | Status | Evidence | Required Change |
|---|---|---|---|---|---|
| Total Matches | `COUNT(fact_matches[match_id])` | `DISTINCTCOUNT(fact_matches[match_id])` | WARNING | COUNT can double-count if joined to granular tables. | Change to `DISTINCTCOUNT`. |
| Total Seasons | `DISTINCTCOUNT(fact_matches[season_sk])` | `DISTINCTCOUNT(fact_matches[season_sk])` | PASS | Directly correlates to `dim_season`. | None. |
| Total Teams | `COUNTROWS(dim_team)` | `COUNTROWS(dim_team)` | PASS | Valid DAX for a dimension table. | None. |
| Total Players | `COUNTROWS(dim_player)` | `COUNTROWS(dim_player)` | PASS | Valid DAX for a dimension table. | None. |
| Total Runs | `SUM(fact_deliveries[batter_runs]) + ...` | `SUM(fact_deliveries[total_runs])` | WARNING | `total_runs` already includes extras in schema. | Update DAX to use `total_runs`. |
| Total Wickets | `SUM(fact_deliveries[is_wicket])` | `SUM(fact_deliveries[is_wicket])` | PASS | `is_wicket` is INT (0 or 1) in schema. | None. |
| Average First Innings Score | `AVERAGEX(...)` | `AVERAGEX(SUMMARIZE(FILTER(fact_deliveries, fact_deliveries[innings] = 1), fact_deliveries[match_id], "Score", SUM(fact_deliveries[total_runs])), [Score])` | PASS | Uses valid sub-aggregation to avoid per-ball averaging. | None. |
| Chasing Win % | Uses `toss_decision = "field"` | Uses `fact_deliveries[innings]=2` batting team = match winner. | FAIL | Fails to count teams forced to chase after losing toss. | Rewrite SQL/DAX logic completely. |
| Win Percentage | `DIVIDE(Total Wins, Matches)` | `DIVIDE(Total Wins, Matches)` | PASS | Standard aggregation. | None. |
| Powerplay Run Rate | `DIVIDE(SUM(Runs), SUM(Overs))` | `DIVIDE(SUM(Runs)*6, COUNT(ball_num))` for Overs <= 5 | FAIL | Over is 0-indexed in DB (0-5 = powerplay), and RR is runs per 6 balls. | Update definition to reflect balls. |
| Death Over Run Rate | `DIVIDE(SUM(Runs), SUM(Overs))` | `DIVIDE(SUM(Runs)*6, COUNT(ball_num))` for Overs >= 15 | FAIL | Over is 0-indexed in DB (15-19 = death). | Update definition. |
| Batting Average | `DIVIDE(Runs, Outs)` | `DIVIDE(SUM(batter_runs), SUM(is_wicket))` | PASS | Assuming Outs = `is_wicket` for batter. | Clarify Outs definition. |
| Strike Rate | `DIVIDE(Runs, Balls) * 100` | `DIVIDE(SUM(batter_runs), COUNT(delivery_sk)) * 100` | WARNING | Must exclude wides from balls faced. | Add `extras_type <> 'wides'` filter. |
| Bowling Economy | `DIVIDE(Runs, Overs)` | `DIVIDE(SUM(total_runs_conceded) * 6, COUNT(legal_deliveries))` | WARNING | Must exclude byes/legbyes from bowler runs. | Clarify runs logic. |
| Player Consistency | % of innings >= 30 runs | % of innings >= 30 runs | PASS | Standard logical metric. | None. |
| Venue Average Score | Avg 1st innings total | Avg 1st innings total | PASS | Relies on Venue dimension filter. | None. |
| Batting-First Success | % defending wins | % defending wins | WARNING | Should use `win_margin_runs > 0` as proxy. | Explicitly define proxy. |
| Toss Impact | Toss win = Match win | Toss win = Match win | PASS | Direct join `toss_winner_sk = winner_team_sk` | None. |
| Close Matches | <= 5 runs or <= 2 wickets | <= 5 runs or <= 2 wickets | PASS | Uses `win_margin_runs` and `win_margin_wickets`. | None. |
| Early Wicket Impact | Wicket in Over 0 | Wicket in Over 0 | PASS | Filter `over_num = 0` and `is_wicket = 1`. | None. |

## 8. Chasing Win % (Critical Correction)
**Why it failed**:
The toss winner might choose to bat. If they do, the *other* team is chasing. The previous DAX only calculated the win percentage of teams that won the toss and chose to chase, leaving out exactly half of the chasing population (teams forced to chase).

**Correct Definition**:
```sql
WITH chasing_teams AS (
    SELECT DISTINCT match_id, batting_team_sk AS chasing_team_sk
    FROM fact_deliveries
    WHERE innings = 2
),
valid_matches AS (
    SELECT match_id, winner_team_sk
    FROM fact_matches
    WHERE result_type != 'no result'
)
SELECT 
    COUNT(v.match_id) AS total_chasing_matches,
    SUM(CASE WHEN c.chasing_team_sk = v.winner_team_sk THEN 1 ELSE 0 END) AS total_chasing_wins,
    ROUND(SUM(CASE WHEN c.chasing_team_sk = v.winner_team_sk THEN 1.0 ELSE 0.0 END) / COUNT(v.match_id) * 100, 2) AS chasing_win_pct
FROM valid_matches v
JOIN chasing_teams c ON v.match_id = c.match_id;
```
**Required Action**: 
In Power BI, it is highly recommended to materialize `chasing_team_sk` inside a `mart_match_results` table in PostgreSQL rather than forcing DAX to perform cross-table granular delivery filtering just to determine the chasing team. However, purely in DAX, it can be approximated by filtering `fact_matches[win_margin_wickets] > 0`.
