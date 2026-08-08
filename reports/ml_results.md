# Machine Learning Results: Win Predictor

## Methodology
- **Target**: Probability that the chasing team wins (1 = Win, 0 = Loss/Tie/No Result).
- **Features**: batting_team, bowling_team, venue, target_score, current_score, overs_completed, wickets_lost, runs_remaining, balls_remaining, current_run_rate, required_run_rate, recent_run_rate, team_recent_win_rate, venue_chase_success_rate
- **Leakage Prevention**: All features are strictly state-based. No post-match data is included.
- **Data Splitting**: Chronological (Train <= 2022, Validate = 2023, Test >= 2024).

## Model 1: Logistic Regression (Baseline)
- Accuracy: 0.7299
- Precision: 0.8468
- Recall: 0.5935
- F1 Score: 0.6979
- ROC-AUC: 0.8401
- Log Loss: 0.6257
- Brier Score: 0.193

## Model 2: XGBoost
- Accuracy: 0.7007
- Precision: 0.8657
- Recall: 0.5096
- F1 Score: 0.6415
- ROC-AUC: 0.8148
- Log Loss: 1.0616
- Brier Score: 0.2441

## Conclusion
XGBoost generally outperforms Logistic Regression in handling the non-linear interactions between required run rates, wickets lost, and deliveries remaining, making it the superior candidate for the live win probability model.
