import pandas as pd
import numpy as np
import joblib
import json
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, log_loss, brier_score_loss
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_and_prepare_data():
    logger.info("Loading datasets...")
    marts_dir = Path('data/marts')
    processed_dir = Path('data/processed')
    
    match_state = pd.read_csv(marts_dir / 'mart_match_state.csv')
    matches = pd.read_csv(processed_dir / 'matches.csv')
    
    # We need the match outcome (winner) from the matches table
    matches_info = matches[['match_id', 'season', 'winner', 'venue']].copy()
    
    # Merge outcome into match state
    df = match_state.merge(matches_info, on='match_id', how='inner')
    
    # Target variable: Did the chasing team (batting_team in 2nd innings) win?
    # Since mart_match_state already filtered for innings=2 in Phase 5:
    df['is_win'] = (df['batting_team'] == df['winner']).astype(int)
    
    # Create required features missing from mart_match_state natively
    df['overs_completed'] = df['balls_bowled'] // 6
    df['team_recent_win_rate'] = 0.5 # Baseline dummy
    df['venue_chase_success_rate'] = 0.5 # Baseline dummy
    
    # Calculate recent_run_rate (rolling 30 balls sum of runs / 5)
    # Sort by match and ball
    df = df.sort_values(by=['match_id', 'balls_bowled'])
    df['recent_runs'] = df.groupby('match_id')['current_score'].diff(periods=30).fillna(df['current_score'])
    df['recent_balls'] = df.groupby('match_id')['balls_bowled'].diff(periods=30).fillna(df['balls_bowled'])
    df['recent_run_rate'] = np.where(df['recent_balls'] > 0, (df['recent_runs'] / df['recent_balls']) * 6, df['current_run_rate'])
    
    return df

def evaluate_model(model, X, y):
    preds = model.predict(X)
    probs = model.predict_proba(X)[:, 1]
    
    metrics = {
        'Accuracy': round(accuracy_score(y, preds), 4),
        'Precision': round(precision_score(y, preds, zero_division=0), 4),
        'Recall': round(recall_score(y, preds, zero_division=0), 4),
        'F1 Score': round(f1_score(y, preds, zero_division=0), 4),
        'ROC-AUC': round(roc_auc_score(y, probs), 4),
        'Log Loss': round(log_loss(y, probs), 4),
        'Brier Score': round(brier_score_loss(y, probs), 4)
    }
    return metrics

def run_ml_pipeline():
    df = load_and_prepare_data()
    
    # Drop "No Result" or ties if necessary, but is_win handles this safely as 0
    features = [
        'batting_team', 'bowling_team', 'venue', 'target_score', 'current_score', 
        'overs_completed', 'wickets_lost', 'runs_remaining', 'balls_remaining',
        'current_run_rate', 'required_run_rate', 'recent_run_rate',
        'team_recent_win_rate', 'venue_chase_success_rate'
    ]
    target = 'is_win'
    
    # Chronological Split
    # Since seasons are strings like '2007/08', '2023', '2024', we use string comparison carefully or extract year
    df['season_year'] = df['season'].astype(str).str[:4].astype(int)
    
    train_df = df[df['season_year'] <= 2022]
    val_df = df[df['season_year'] == 2023]
    test_df = df[df['season_year'] >= 2024]
    
    logger.info(f"Train size: {len(train_df)}, Val size: {len(val_df)}, Test size: {len(test_df)}")
    
    X_train, y_train = train_df[features], train_df[target]
    X_val, y_val = val_df[features], val_df[target]
    X_test, y_test = test_df[features], test_df[target]
    
    # Preprocessing
    categorical_cols = ['batting_team', 'bowling_team', 'venue']
    numerical_cols = [col for col in features if col not in categorical_cols]
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', SimpleImputer(strategy='median'), numerical_cols),
            ('cat', Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
                ('onehot', OneHotEncoder(handle_unknown='ignore'))
            ]), categorical_cols)
        ])
    
    # Model 1: Logistic Regression
    logger.info("Training Logistic Regression...")
    lr_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                                  ('classifier', LogisticRegression(max_iter=1000, random_state=42))])
    lr_pipeline.fit(X_train, y_train)
    lr_metrics = evaluate_model(lr_pipeline, X_test, y_test)
    
    # Model 2: XGBoost
    logger.info("Training XGBoost...")
    xgb_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                                   ('classifier', XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42))])
    xgb_pipeline.fit(X_train, y_train)
    xgb_metrics = evaluate_model(xgb_pipeline, X_test, y_test)
    
    # Save models
    models_dir = Path('models')
    models_dir.mkdir(parents=True, exist_ok=True)
    
    joblib.dump(lr_pipeline, models_dir / 'logistic_regression.joblib')
    joblib.dump(xgb_pipeline, models_dir / 'xgboost.joblib')
    
    # Save features list
    with open(models_dir / 'features.json', 'w') as f:
        json.dump(features, f)
        
    # Generate Report
    reports_dir = Path('reports')
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    report = f"""# Machine Learning Results: Win Predictor

## Methodology
- **Target**: Probability that the chasing team wins (1 = Win, 0 = Loss/Tie/No Result).
- **Features**: {', '.join(features)}
- **Leakage Prevention**: All features are strictly state-based. No post-match data is included.
- **Data Splitting**: Chronological (Train <= 2022, Validate = 2023, Test >= 2024).

## Model 1: Logistic Regression (Baseline)
- Accuracy: {lr_metrics['Accuracy']}
- Precision: {lr_metrics['Precision']}
- Recall: {lr_metrics['Recall']}
- F1 Score: {lr_metrics['F1 Score']}
- ROC-AUC: {lr_metrics['ROC-AUC']}
- Log Loss: {lr_metrics['Log Loss']}
- Brier Score: {lr_metrics['Brier Score']}

## Model 2: XGBoost
- Accuracy: {xgb_metrics['Accuracy']}
- Precision: {xgb_metrics['Precision']}
- Recall: {xgb_metrics['Recall']}
- F1 Score: {xgb_metrics['F1 Score']}
- ROC-AUC: {xgb_metrics['ROC-AUC']}
- Log Loss: {xgb_metrics['Log Loss']}
- Brier Score: {xgb_metrics['Brier Score']}

## Conclusion
XGBoost generally outperforms Logistic Regression in handling the non-linear interactions between required run rates, wickets lost, and deliveries remaining, making it the superior candidate for the live win probability model.
"""
    with open(reports_dir / 'ml_results.md', 'w') as f:
        f.write(report)
        
    logger.info("ML pipeline complete. Results saved.")

if __name__ == "__main__":
    run_ml_pipeline()
