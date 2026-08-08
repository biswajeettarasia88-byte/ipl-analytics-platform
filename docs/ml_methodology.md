# Machine Learning Methodology: Win Probability Model

## Objective
To construct a real-time predictive model that estimates the win probability of the chasing team at any given delivery during the second innings of an IPL match.

## Target Variable
- **`is_win`**: Binary indicator (1 = Chasing Team Wins, 0 = Chasing Team Loses / Match Tied / No Result).

## Strict Leakage Prevention Rules
Target leakage is the most critical risk in sports predictive modeling. To ensure the model performs identically in production as it does in training:
1. **No Future Data**: At delivery $N$, the model only has access to aggregated match states up to delivery $N-1$.
2. **No Post-Match Labels**: Features like `final_score`, `win_margin`, or `player_of_match` are strictly excluded from the feature space.
3. **No Random Delivery Splitting**: Standard `train_test_split` with shuffling would cause leakage, as deliveries from the same match would appear in both train and test sets, allowing the model to "memorize" the outcome of a match it has partially seen.

## Chronological Data Splitting
To simulate real-world deployment, the dataset is split by season (temporally):
- **Training Set**: Matches from inception (2008) through 2022. The model learns historical pacing, run rates, and team strengths.
- **Validation Set**: 2023 Season. Used for hyperparameter tuning and early stopping.
- **Test Set**: 2024 to latest available. Used exclusively for final metric reporting to judge how the model adapts to the modern era (e.g., the introduction of the Impact Player rule and highly inflated run rates).

## Feature Space
- **Categorical**: `batting_team`, `bowling_team`, `venue`.
- **Match State (Continuous)**: `current_score`, `wickets_lost`, `overs_completed`, `balls_remaining`, `runs_remaining`.
- **Derived Metrics**: `current_run_rate`, `required_run_rate`, `recent_run_rate` (last 5 overs).
- **Contextual**: `target_score`, `team_recent_win_rate`, `venue_chase_success_rate`.

## Models Evaluated
1. **Logistic Regression**: Serves as a highly interpretable, fast-calibrating baseline model.
2. **XGBoost**: Tree-based gradient boosting model capable of capturing complex, non-linear inflection points (e.g., the sudden drop in win probability when required run rate crosses 12 with 3 wickets left).

## Evaluation Metrics
- **Log Loss / Brier Score**: The primary metrics. Since the objective is a continuous *probability* (not just a binary Win/Loss label), calibrating the confidence of the prediction is paramount.
- **ROC-AUC**: Measures the model's ability to discriminate between eventual wins and losses at various thresholds.
- **Accuracy / F1**: Standard classification metrics computed at a default 0.5 probability threshold.
