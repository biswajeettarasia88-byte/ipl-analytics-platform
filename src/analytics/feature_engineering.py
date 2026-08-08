import pandas as pd
import numpy as np
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def build_marts():
    processed_dir = Path('data/processed')
    marts_dir = Path('data/marts')
    marts_dir.mkdir(parents=True, exist_ok=True)
    
    # Load Silver Data
    matches = pd.read_csv(processed_dir / 'matches.csv')
    deliveries = pd.read_csv(processed_dir / 'deliveries.csv')
    
    # ---------------------------------------------------------
    # 1. mart_batting
    # ---------------------------------------------------------
    logger.info("Building mart_batting...")
    batting = deliveries.groupby('batter').agg(
        runs=('batter_runs', 'sum'),
        balls=('ball', 'count')
    ).reset_index()
    
    # Boundaries
    boundaries = deliveries[deliveries['batter_runs'].isin([4, 6])].groupby('batter').size().reset_index(name='boundaries')
    batting = batting.merge(boundaries, on='batter', how='left').fillna({'boundaries': 0})
    
    # Dot balls
    dot_balls = deliveries[deliveries['total_runs'] == 0].groupby('batter').size().reset_index(name='dots')
    batting = batting.merge(dot_balls, on='batter', how='left').fillna({'dots': 0})
    
    batting['strike_rate'] = np.where(batting['balls'] > 0, (batting['runs'] / batting['balls']) * 100, 0)
    batting['dot_ball_percentage'] = np.where(batting['balls'] > 0, (batting['dots'] / batting['balls']) * 100, 0)
    batting = batting.drop(columns=['dots'])
    batting.to_csv(marts_dir / 'mart_batting.csv', index=False)
    
    # ---------------------------------------------------------
    # 2. mart_bowling
    # ---------------------------------------------------------
    logger.info("Building mart_bowling...")
    bowling = deliveries.groupby('bowler').agg(
        runs_conceded=('total_runs', 'sum'),
        balls_bowled=('ball', 'count'),
        wickets=('is_wicket', 'sum') # Simplified, normally exclude run_outs
    ).reset_index()
    
    dot_balls_bowled = deliveries[deliveries['total_runs'] == 0].groupby('bowler').size().reset_index(name='dots')
    bowling = bowling.merge(dot_balls_bowled, on='bowler', how='left').fillna({'dots': 0})
    
    bowling['economy'] = np.where(bowling['balls_bowled'] > 0, (bowling['runs_conceded'] / (bowling['balls_bowled'] / 6)), 0)
    bowling['dot_ball_percentage'] = np.where(bowling['balls_bowled'] > 0, (bowling['dots'] / bowling['balls_bowled']) * 100, 0)
    bowling = bowling.drop(columns=['dots'])
    bowling.to_csv(marts_dir / 'mart_bowling.csv', index=False)
    
    # ---------------------------------------------------------
    # 3. mart_venue
    # ---------------------------------------------------------
    logger.info("Building mart_venue...")
    venue_matches = matches.groupby('venue').agg(
        total_matches=('match_id', 'count')
    ).reset_index()
    
    # Average score (innings 1)
    inn1_scores = deliveries[deliveries['innings'] == 1].groupby('match_id')['total_runs'].sum().reset_index()
    inn1_scores = inn1_scores.merge(matches[['match_id', 'venue']], on='match_id')
    avg_score = inn1_scores.groupby('venue')['total_runs'].mean().reset_index(name='average_score')
    
    # Success rates
    chasing_wins = matches[matches['toss_decision'] == 'field'] # Approximation of chasing (or check innings data)
    
    venue_mart = venue_matches.merge(avg_score, on='venue', how='left')
    venue_mart.to_csv(marts_dir / 'mart_venue.csv', index=False)
    
    # ---------------------------------------------------------
    # 4. mart_match_state (ML Features)
    # ---------------------------------------------------------
    logger.info("Building mart_match_state...")
    # Sort deliveries chronologically within each match & innings
    deliveries = deliveries.sort_values(by=['match_id', 'innings', 'over', 'ball']).reset_index(drop=True)
    
    # Current score before the ball is bowled (Shifted cumulative sum)
    deliveries['current_score'] = deliveries.groupby(['match_id', 'innings'])['total_runs'].cumsum() - deliveries['total_runs']
    deliveries['wickets_lost'] = deliveries.groupby(['match_id', 'innings'])['is_wicket'].cumsum() - deliveries['is_wicket']
    
    # Balls bowled (approximate, ignoring valid vs invalid balls for simplicity of ML baseline)
    deliveries['balls_bowled'] = deliveries.groupby(['match_id', 'innings']).cumcount()
    deliveries['balls_remaining'] = 120 - deliveries['balls_bowled']
    deliveries['wickets_remaining'] = 10 - deliveries['wickets_lost']
    
    deliveries['current_run_rate'] = np.where(
        deliveries['balls_bowled'] > 0, 
        (deliveries['current_score'] / deliveries['balls_bowled']) * 6, 
        0
    )
    
    # Join 1st innings score to get target for 2nd innings
    first_innings = deliveries[deliveries['innings'] == 1].groupby('match_id')['total_runs'].sum().reset_index(name='target_score')
    first_innings['target_score'] += 1 # Target is runs + 1
    
    match_state = deliveries[deliveries['innings'] == 2].merge(first_innings, on='match_id', how='left')
    match_state['runs_remaining'] = match_state['target_score'] - match_state['current_score']
    
    # Required Run Rate
    match_state['required_run_rate'] = np.where(
        match_state['balls_remaining'] > 0,
        (match_state['runs_remaining'] / match_state['balls_remaining']) * 6,
        match_state['runs_remaining'] * 6 # extreme case if 0 balls left
    )
    
    match_state.to_csv(marts_dir / 'mart_match_state.csv', index=False)
    
    logger.info("Feature engineering completed.")

if __name__ == "__main__":
    build_marts()
