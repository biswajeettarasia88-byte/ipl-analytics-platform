import pytest
import pandas as pd
from pathlib import Path

def test_feature_calculations():
    # Load the mart_match_state.csv which contains derived ML features
    marts_dir = Path('data/marts')
    if not (marts_dir / 'mart_match_state.csv').exists():
        pytest.skip("mart_match_state.csv not found. Did Phase 5 run?")
        
    df = pd.read_csv(marts_dir / 'mart_match_state.csv')
    
    # Check that runs_remaining is strictly decreasing or constant within an innings
    # For a random match:
    sample_match = df['match_id'].iloc[0]
    match_data = df[df['match_id'] == sample_match].sort_values('balls_bowled')
    
    assert match_data['runs_remaining'].is_monotonic_decreasing or \
           all(x >= y for x, y in zip(match_data['runs_remaining'], match_data['runs_remaining'][1:])), "Runs remaining should decrease or stay constant"
           
    # Check that wickets lost is strictly increasing
    assert match_data['wickets_lost'].is_monotonic_increasing, "Wickets lost should always increase"

def test_aggregates_and_derived_metrics():
    # Load validation from phase 7 validation script
    from src.analytics.validate_kpis import setup_db, validate_kpis
    
    try:
        conn = setup_db()
        validate_kpis(conn)
    except Exception as e:
        pytest.fail(f"KPI Validation failed: {e}")
