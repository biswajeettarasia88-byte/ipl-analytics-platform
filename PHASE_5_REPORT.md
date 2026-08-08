# Phase 5 Report: Feature Engineering

## Objective
Build analytical features and data marts tailored for both BI reporting and downstream Machine Learning models. Crucially, all ML features must be constructed strictly to prevent target leakage.

## Implementation Details

### Data Marts Generated
The `src/analytics/feature_engineering.py` script successfully materialized the following analytical marts into `data/marts/`:

1. **`mart_batting`**: Aggregated batting statistics.
   - Features tested: `runs`, `balls`, `strike_rate`, `boundaries`, `dot_ball_percentage`.
2. **`mart_bowling`**: Aggregated bowling statistics.
   - Features tested: `wickets`, `economy`, `runs_conceded`, `dot_ball_percentage`.
3. **`mart_venue`**: Venue historical trends.
   - Features tested: `average_score`, `chasing_success_rate` (via filtering toss decisions and innings scores).
4. **`mart_match_state` (ML Features)**: Ball-by-ball context features for the win probability predictor.
   - Features tested: `current_score`, `target`, `runs_remaining`, `balls_remaining`, `wickets_remaining`, `current_run_rate`, `required_run_rate`, `recent_run_rate`.

### Leakage Prevention (CRITICAL)
- The ML dataset (`mart_match_state`) was rigorously structured such that features at delivery `N` only incorporate historical data up to delivery `N-1` (the preceding state of the match).
- `runs_remaining` and `required_run_rate` logically only exist during the second innings, and are securely derived by joining the final aggregated score of the 1st innings.
- No match outcome variables (e.g. final winner, final win margin) were included as features in the `mart_match_state` dataset.

### Documentation Created
- Created `docs/feature_dictionary.md` detailing the business logic, math, and definitions for every generated feature.
- Example SQL view queries (e.g. `sql/marts/mart_team_season.sql`) have been staged for direct database translation.

## Validation
- All features were successfully calculated using Pandas. No mathematical errors (e.g., divide by zero on 0 balls faced/bowled) occurred due to proper handling with `numpy.where()`.

## Next Recommended Phase
**Phase 6: Machine Learning Preparation**
- Validate chronological splitting mechanisms for training vs testing.
- Handle categorical encoding and missing value imputation for the model pipeline.
