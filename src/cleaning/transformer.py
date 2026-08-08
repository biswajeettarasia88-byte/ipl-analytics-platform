import os
import json
import logging
import pandas as pd
from pathlib import Path
import yaml

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

TEAM_MAPPING = {
    'Delhi Daredevils': 'Delhi Capitals',
    'Kings XI Punjab': 'Punjab Kings',
    'Rising Pune Supergiant': 'Rising Pune Supergiants',
    'Royal Challengers Bangalore': 'Royal Challengers Bengaluru',
    'Pune Warriors': 'Pune Warriors India'
}

VENUE_MAPPING = {
    'M Chinnaswamy Stadium': 'M Chinnaswamy Stadium, Bengaluru',
    'M.Chinnaswamy Stadium': 'M Chinnaswamy Stadium, Bengaluru',
    'Feroz Shah Kotla': 'Arun Jaitley Stadium, Delhi',
    'Arun Jaitley Stadium': 'Arun Jaitley Stadium, Delhi',
    'Sardar Patel Stadium, Motera': 'Narendra Modi Stadium, Ahmedabad',
    'Narendra Modi Stadium': 'Narendra Modi Stadium, Ahmedabad',
    'Rajiv Gandhi International Stadium, Uppal': 'Rajiv Gandhi International Stadium, Hyderabad',
    'Rajiv Gandhi Intl. Cricket Stadium': 'Rajiv Gandhi International Stadium, Hyderabad',
    'Punjab Cricket Association Stadium, Mohali': 'IS Bindra Stadium, Mohali',
    'Punjab Cricket Association IS Bindra Stadium, Mohali': 'IS Bindra Stadium, Mohali',
    'Punjab Cricket Association IS Bindra Stadium': 'IS Bindra Stadium, Mohali',
    'MA Chidambaram Stadium, Chepauk': 'MA Chidambaram Stadium, Chennai',
    'MA Chidambaram Stadium': 'MA Chidambaram Stadium, Chennai',
    'MA Chidambaram Stadium, Chepauk, Chennai': 'MA Chidambaram Stadium, Chennai',
    'Wankhede Stadium': 'Wankhede Stadium, Mumbai',
    'Wankhede Stadium, Mumbai': 'Wankhede Stadium, Mumbai',
    'Eden Gardens': 'Eden Gardens, Kolkata',
    'Eden Gardens, Kolkata': 'Eden Gardens, Kolkata',
    'Sawai Mansingh Stadium': 'Sawai Mansingh Stadium, Jaipur',
    'Sawai Mansingh Stadium, Jaipur': 'Sawai Mansingh Stadium, Jaipur'
}

def standardize_team(team):
    return TEAM_MAPPING.get(team, team)

def standardize_venue(venue):
    return VENUE_MAPPING.get(venue, venue)

def load_config():
    config_path = Path('config/config.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def transform_data():
    config = load_config()
    raw_dir = Path(config['data']['raw_path'])
    out_dir = Path(config['data']['processed_path'])
    out_dir.mkdir(parents=True, exist_ok=True)
    
    json_files = list(raw_dir.glob("*.json"))
    json_files = [f for f in json_files if f.name != 'metadata.json']
    
    matches = []
    deliveries = []
    players_set = set()
    teams_set = set()
    venues_set = set()
    
    stats = {
        'missing_city_handled': 0,
        'team_names_standardized': 0,
        'venue_names_standardized': 0
    }
    
    for jf in json_files:
        with open(jf, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        match_id = jf.stem
        info = data.get('info', {})
        
        # Match data extraction
        raw_teams = info.get('teams', [])
        std_teams = [standardize_team(t) for t in raw_teams]
        if raw_teams != std_teams:
            stats['team_names_standardized'] += 1
            
        for t in std_teams: teams_set.add(t)
            
        raw_venue = info.get('venue')
        std_venue = standardize_venue(raw_venue)
        if raw_venue != std_venue:
            stats['venue_names_standardized'] += 1
        venues_set.add(std_venue)
        
        city = info.get('city')
        if not city:
            # Impute city from venue
            if 'Bengaluru' in std_venue or 'Bangalore' in std_venue: city = 'Bengaluru'
            elif 'Delhi' in std_venue: city = 'Delhi'
            elif 'Hyderabad' in std_venue: city = 'Hyderabad'
            elif 'Mumbai' in std_venue: city = 'Mumbai'
            elif 'Kolkata' in std_venue: city = 'Kolkata'
            elif 'Chennai' in std_venue: city = 'Chennai'
            elif 'Jaipur' in std_venue: city = 'Jaipur'
            elif 'Mohali' in std_venue: city = 'Chandigarh'
            elif 'Ahmedabad' in std_venue: city = 'Ahmedabad'
            else: city = 'Unknown'
            stats['missing_city_handled'] += 1
            
        toss_winner = standardize_team(info.get('toss', {}).get('winner'))
        toss_decision = info.get('toss', {}).get('decision')
        
        outcome = info.get('outcome', {})
        winner = standardize_team(outcome.get('winner', 'No Result'))
        result_type = outcome.get('result', 'normal')
        win_margin_runs = outcome.get('by', {}).get('runs', 0)
        win_margin_wickets = outcome.get('by', {}).get('wickets', 0)
        
        pom = info.get('player_of_match', [])
        pom_str = pom[0] if pom else None
        
        date = info.get('dates', [None])[0]
        season = info.get('season')
        
        matches.append({
            'match_id': match_id,
            'season': str(season),
            'date': date,
            'city': city,
            'venue': std_venue,
            'team1': std_teams[0] if len(std_teams) > 0 else None,
            'team2': std_teams[1] if len(std_teams) > 1 else None,
            'toss_winner': toss_winner,
            'toss_decision': toss_decision,
            'winner': winner,
            'result_type': result_type,
            'win_margin_runs': win_margin_runs,
            'win_margin_wickets': win_margin_wickets,
            'player_of_match': pom_str
        })
        
        # Player registry extraction
        registry = info.get('registry', {}).get('people', {})
        for player_name, player_id in registry.items():
            players_set.add((player_id, player_name))
            
        # Deliveries extraction
        innings_data = data.get('innings', [])
        for inn_idx, inn in enumerate(innings_data):
            batting_team = standardize_team(inn.get('team'))
            bowling_team = std_teams[1] if batting_team == std_teams[0] else std_teams[0]
            
            for over_data in inn.get('overs', []):
                over_num = over_data.get('over')
                for ball_idx, delivery in enumerate(over_data.get('deliveries', [])):
                    batter = delivery.get('batter')
                    bowler = delivery.get('bowler')
                    non_striker = delivery.get('non_striker')
                    
                    runs = delivery.get('runs', {})
                    batter_runs = runs.get('batter', 0)
                    extras_runs = runs.get('extras', 0)
                    total_runs = runs.get('total', 0)
                    
                    extras_type = ','.join(delivery.get('extras', {}).keys()) if delivery.get('extras') else None
                    
                    wickets = delivery.get('wickets', [])
                    wicket_type = wickets[0].get('kind') if wickets else None
                    dismissed_player = wickets[0].get('player_out') if wickets else None
                    
                    deliveries.append({
                        'match_id': match_id,
                        'innings': inn_idx + 1,
                        'batting_team': batting_team,
                        'bowling_team': bowling_team,
                        'over': over_num,
                        'ball': ball_idx + 1,
                        'batter': batter,
                        'bowler': bowler,
                        'non_striker': non_striker,
                        'batter_runs': batter_runs,
                        'extras_runs': extras_runs,
                        'total_runs': total_runs,
                        'extras_type': extras_type,
                        'is_wicket': 1 if wickets else 0,
                        'wicket_type': wicket_type,
                        'dismissed_player': dismissed_player
                    })
                    
    # Create DataFrames
    df_matches = pd.DataFrame(matches)
    df_matches['date'] = pd.to_datetime(df_matches['date'])
    
    df_deliveries = pd.DataFrame(deliveries)
    
    df_players = pd.DataFrame(list(players_set), columns=['player_id', 'player_name'])
    df_teams = pd.DataFrame(list(teams_set), columns=['team_name'])
    df_venues = pd.DataFrame(list(venues_set), columns=['venue_name'])
    
    # Save processed files
    df_matches.to_csv(out_dir / 'matches.csv', index=False)
    df_deliveries.to_csv(out_dir / 'deliveries.csv', index=False)
    df_players.to_csv(out_dir / 'players.csv', index=False)
    df_teams.to_csv(out_dir / 'teams.csv', index=False)
    df_venues.to_csv(out_dir / 'venues.csv', index=False)
    
    logger.info("Data Transformation Complete.")
    logger.info(f"Generated {len(df_matches)} matches records.")
    logger.info(f"Generated {len(df_deliveries)} deliveries records.")
    logger.info(f"Missing cities handled: {stats['missing_city_handled']}")
    logger.info(f"Matches with team names standardized: {stats['team_names_standardized']}")
    logger.info(f"Matches with venue names standardized: {stats['venue_names_standardized']}")
    
    # Write stats to json for the report to read
    with open('data/processed/silver_stats.json', 'w') as f:
        json.dump(stats, f)

if __name__ == "__main__":
    transform_data()
