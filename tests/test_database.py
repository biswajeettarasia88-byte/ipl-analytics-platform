import pandas as pd
from pathlib import Path
import pytest

# Load dataframes
processed_dir = Path('data/processed')
df_matches = pd.read_csv(processed_dir / 'matches.csv')
df_deliveries = pd.read_csv(processed_dir / 'deliveries.csv')
df_teams = pd.read_csv(processed_dir / 'teams.csv')
df_venues = pd.read_csv(processed_dir / 'venues.csv')
df_players = pd.read_csv(processed_dir / 'players.csv')

def test_duplicate_prevention_matches():
    # Verify no duplicate match IDs
    assert df_matches['match_id'].duplicated().sum() == 0, "Duplicate matches found!"

def test_duplicate_prevention_deliveries():
    # Verify no duplicate deliveries (match_id, innings, over, ball)
    # Note: In rare cases, a ball can be re-bowled due to a dead ball and might share the same ball_num in raw data.
    # But Cricsheet typically uses ball fractions for extras, or increments normally.
    # Let's ensure (match_id, innings, over, ball, batter) is unique at least.
    duplicates = df_deliveries.duplicated(subset=['match_id', 'innings', 'over', 'ball'])
    assert duplicates.sum() == 0, f"Found {duplicates.sum()} duplicate deliveries"

def test_no_orphan_records_deliveries_to_matches():
    # Verify all match_ids in deliveries exist in matches
    delivery_match_ids = set(df_deliveries['match_id'])
    match_ids = set(df_matches['match_id'])
    orphans = delivery_match_ids - match_ids
    assert len(orphans) == 0, f"Found {len(orphans)} orphan deliveries without a valid match"

def test_no_orphan_records_teams():
    # Verify all teams in matches exist in teams dimension
    valid_teams = set(df_teams['team_name'])
    match_teams = set(df_matches['team1'].dropna()).union(set(df_matches['team2'].dropna()))
    orphans = match_teams - valid_teams
    assert len(orphans) == 0, f"Found {len(orphans)} orphan teams in matches"

def test_no_orphan_records_venues():
    # Verify all venues in matches exist in venues dimension
    valid_venues = set(df_venues['venue_name'])
    match_venues = set(df_matches['venue'].dropna())
    orphans = match_venues - valid_venues
    assert len(orphans) == 0, f"Found {len(orphans)} orphan venues in matches"

def test_row_counts_matches():
    assert len(df_matches) == 1243

def test_row_counts_deliveries():
    assert len(df_deliveries) > 295000
