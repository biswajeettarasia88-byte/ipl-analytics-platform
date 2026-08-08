import pytest
import joblib
import json
import pandas as pd
from pathlib import Path

@pytest.fixture
def ml_assets():
    models_dir = Path('models')
    try:
        pipeline = joblib.load(models_dir / 'xgboost.joblib')
        with open(models_dir / 'features.json', 'r') as f:
            features = json.load(f)
        return pipeline, features
    except FileNotFoundError:
        pytest.skip("Models not trained yet.")

def test_ml_feature_schema(ml_assets):
    pipeline, features = ml_assets
    assert len(features) == 14, "Expected exactly 14 features for the model"
    assert 'required_run_rate' in features
    assert 'current_score' in features

def test_prediction_shape_and_range(ml_assets):
    pipeline, features = ml_assets
    
    # Create a dummy dataframe representing one ball
    dummy_data = {
        'batting_team': 'Chennai Super Kings',
        'bowling_team': 'Mumbai Indians',
        'venue': 'Wankhede Stadium',
        'target_score': 180,
        'current_score': 100,
        'overs_completed': 12,
        'wickets_lost': 2,
        'runs_remaining': 80,
        'balls_remaining': 48,
        'current_run_rate': 8.33,
        'required_run_rate': 10.0,
        'recent_run_rate': 9.0,
        'team_recent_win_rate': 0.6,
        'venue_chase_success_rate': 0.55
    }
    
    df = pd.DataFrame([dummy_data])[features]
    
    # Test Prediction Shape
    preds = pipeline.predict_proba(df)
    assert preds.shape == (1, 2), "Predict proba should return shape (1, 2)"
    
    # Test Probability Range
    prob = preds[0][1]
    assert 0.0 <= prob <= 1.0, "Probability must be between 0 and 1"
    
def test_leakage_checks():
    # Ensure no 'final_score', 'winner' or 'win_margin' is in the features.json
    models_dir = Path('models')
    try:
        with open(models_dir / 'features.json', 'r') as f:
            features = json.load(f)
            
        assert 'winner' not in features
        assert 'win_margin' not in features
        assert 'final_score' not in features
        assert 'is_win' not in features
    except FileNotFoundError:
        pytest.skip("Models not trained yet.")
