# Feature Dictionary

This document defines the analytical and machine learning features constructed for the IPL Analytics & Decision Intelligence Platform.

## 1. Batting Mart (`mart_batting`)
Aggregates player batting performance across their career and per season.
- `runs`: Total runs scored by the batter.
- `balls`: Total legal deliveries faced (excluding wides).
- `strike_rate`: `(runs / balls) * 100`.
- `boundaries`: Total count of fours and sixes hit.
- `dot_ball_percentage`: Percentage of balls faced where 0 runs were scored.

## 2. Bowling Mart (`mart_bowling`)
Aggregates player bowling performance.
- `wickets`: Total legitimate wickets taken (excluding run-outs).
- `runs_conceded`: Total runs conceded off the bowler's bowling.
- `economy`: `(runs_conceded / (balls_bowled / 6))`.
- `dot_ball_percentage`: Percentage of balls bowled where 0 runs were scored.

## 3. Team & Season Mart (`mart_team_season`)
Tracks team performance metrics contextually.
- `win_rate`: Overall percentage of matches won.
- `recent_win_rate`: Win rate over the last `N` matches (rolling window to avoid target leakage).
- `chasing_success_rate`: Win percentage when batting second.
- `batting_first_success_rate`: Win percentage when batting first.
- `powerplay_run_rate`: Average run rate during overs 1-6.
- `death_over_run_rate`: Average run rate during overs 16-20.

## 4. Venue Mart (`mart_venue`)
Tracks historical venue statistics.
- `average_score`: Average first innings total at the venue.
- `chasing_success_rate`: How often the chasing team wins here.
- `batting_first_success_rate`: How often the team batting first wins here.

## 5. Match State Mart (`mart_match_state`) - *ML Features*
Ball-by-ball contextual state features for the Match Win Probability model.
> **CRITICAL (LEAKAGE PREVENTION)**: All features here are calculated *before* the current ball is bowled. It relies strictly on the state of the match up to `ball N-1`. Future match outcomes are strictly excluded.

- `current_score`: Total runs scored by the batting team up to the previous ball.
- `target`: The total runs required to win (only available in 2nd innings).
- `runs_remaining`: `target - current_score` (only in 2nd innings).
- `balls_remaining`: `120 - (completed_overs * 6 + balls_in_current_over)`.
- `wickets_remaining`: `10 - wickets_lost_so_far`.
- `current_run_rate`: `(current_score / balls_bowled) * 6`.
- `required_run_rate`: `(runs_remaining / balls_remaining) * 6` (capped at 36).
- `recent_run_rate`: Run rate over the last 30 balls (5 overs).
