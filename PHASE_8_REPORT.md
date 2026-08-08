# Phase 8 Report: Machine Learning Win Predictor

## Objective
Predict the probability that the batting (chasing) team wins a second-innings IPL match based on the real-time, ball-by-ball match state, without introducing target leakage.

## Implementation Details

### Data Preprocessing & Leakage Prevention
- Constructed the target variable (`is_win`) accurately from the match outcomes.
- Implemented chronological splitting to guarantee zero leakage of future states into historical training:
  - **Training Set (<= 2022)**: 108,910 deliveries.
  - **Validation Set (2023)**: 8,621 deliveries.
  - **Test Set (>= 2024)**: 24,772 deliveries.
- Ensured features strictly represented the state of the match *prior* to a delivery being bowled.

### Model Training
Trained two classification pipelines, using One-Hot Encoding for categorical variables (`batting_team`, `bowling_team`, `venue`) and Median Imputation for continuous variables:
1. **Logistic Regression** (Baseline model for fast, interpretable calibration).
2. **XGBoost Classifier** (Advanced tree-based model to capture non-linear relationships, like exponential pressure in death overs).

### Validation and Results
The full evaluation metrics (Accuracy, Precision, Recall, F1, ROC-AUC, Log Loss, Brier Score) are documented in the detailed report:
- `reports/ml_results.md`

XGBoost successfully optimized the logarithmic loss (`eval_metric='logloss'`), generating robust probability distributions suitable for live broadcasting overlays.

## Artifacts Generated
- `models/logistic_regression.joblib` (Trained LR model)
- `models/xgboost.joblib` (Trained XGBoost model)
- `models/features.json` (List of ordered features required for inference)
- `docs/ml_methodology.md` (Detailed methodological documentation regarding leakage prevention and evaluation)
- `reports/ml_results.md` (Final evaluation metric comparison)

## Next Recommended Phase
**Phase 9: Application Development**
- Embed the trained XGBoost model into an interactive frontend (e.g., Streamlit) allowing users to tweak match states and see real-time win probability shifts.
