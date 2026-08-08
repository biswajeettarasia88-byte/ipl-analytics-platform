import pandas as pd
from pathlib import Path
import pytest

def test_silver_files_exist():
    out_dir = Path('data/processed')
    assert (out_dir / 'matches.csv').exists()
    assert (out_dir / 'deliveries.csv').exists()
    assert (out_dir / 'players.csv').exists()
    assert (out_dir / 'teams.csv').exists()
    assert (out_dir / 'venues.csv').exists()
    
def test_matches_schema():
    df = pd.read_csv('data/processed/matches.csv')
    assert len(df) > 1000
    assert 'match_id' in df.columns
    assert 'city' in df.columns
    assert df['city'].isnull().sum() == 0, "Cities should have been imputed"
    
def test_deliveries_schema():
    df = pd.read_csv('data/processed/deliveries.csv')
    assert len(df) > 250000
    assert 'match_id' in df.columns
    assert 'batter_runs' in df.columns
    
def test_standardization():
    df_teams = pd.read_csv('data/processed/teams.csv')
    teams = df_teams['team_name'].tolist()
    assert 'Delhi Daredevils' not in teams, "Team names not standardized"
    assert 'Kings XI Punjab' not in teams
