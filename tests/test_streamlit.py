import pytest
import sys
from pathlib import Path

# Add project root to python path to import app logic
sys.path.append(str(Path(__file__).parent.parent))

import importlib.util

spec = importlib.util.spec_from_file_location("app", str(Path(__file__).parent.parent / 'streamlit' / 'app.py'))
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)

load_ml_assets = app.load_ml_assets
get_prediction = app.get_prediction

def test_app_model_loading():
    pipeline, features = load_ml_assets()
    assert pipeline is not None
    assert features is not None
    assert len(features) == 14

def test_invalid_input_handling():
    # get_prediction(batting_team, bowling_team, venue, target, current_score, overs_completed, wickets_lost)
    
    # Test 1: current score > target
    res1 = get_prediction('A', 'B', 'V', 100, 110, 10, 2)
    assert res1 is None, "Should fail when current_score > target"
    
    # Test 2: Wickets lost > 10
    res2 = get_prediction('A', 'B', 'V', 100, 50, 10, 11)
    assert res2 is None, "Should fail when wickets > 10"
    
    # Test 3: Same team
    res3 = get_prediction('A', 'A', 'V', 100, 50, 10, 2)
    assert res3 is None, "Should fail when teams are the same"
    
def test_valid_input_prediction():
    res = get_prediction('Chennai Super Kings', 'Mumbai Indians', 'Wankhede Stadium', 180, 100, 12, 2)
    assert res is not None
    
    prob, df, crr, rrr, runs_rem, balls_rem = res
    assert 0 <= prob <= 1
    assert runs_rem == 80
    assert balls_rem == 48
    assert crr == (100 / 72) * 6 # 100 runs in 12 overs
    assert rrr == (80 / 48) * 6  # 80 runs in 48 balls
