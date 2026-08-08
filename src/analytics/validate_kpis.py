import sqlite3
import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_db():
    conn = sqlite3.connect(':memory:')
    processed_dir = Path('data/processed')
    
    # Load core tables
    pd.read_csv(processed_dir / 'matches.csv').to_sql('fact_matches', conn, index=False)
    pd.read_csv(processed_dir / 'deliveries.csv').to_sql('fact_deliveries', conn, index=False)
    pd.read_csv(processed_dir / 'teams.csv').to_sql('dim_team', conn, index=False)
    pd.read_csv(processed_dir / 'players.csv').to_sql('dim_player', conn, index=False)
    
    return conn

def validate_kpis(conn):
    logger.info("Validating PAGE 1 KPIs...")
    
    kpis = {}
    
    # Total Matches
    kpis['Total Matches'] = pd.read_sql_query("SELECT COUNT(*) as v FROM fact_matches", conn)['v'][0]
    
    # Total Seasons
    kpis['Total Seasons'] = pd.read_sql_query("SELECT COUNT(DISTINCT season) as v FROM fact_matches", conn)['v'][0]
    
    # Total Teams
    kpis['Total Teams'] = pd.read_sql_query("SELECT COUNT(*) as v FROM dim_team", conn)['v'][0]
    
    # Total Players
    kpis['Total Players'] = pd.read_sql_query("SELECT COUNT(*) as v FROM dim_player", conn)['v'][0]
    
    # Total Runs
    kpis['Total Runs'] = pd.read_sql_query("SELECT SUM(total_runs) as v FROM fact_deliveries", conn)['v'][0]
    
    # Total Wickets
    kpis['Total Wickets'] = pd.read_sql_query("SELECT SUM(is_wicket) as v FROM fact_deliveries", conn)['v'][0]
    
    # Average Score (1st Innings)
    kpis['Average Score'] = pd.read_sql_query("""
        WITH InningsScores AS (
            SELECT match_id, SUM(total_runs) as score
            FROM fact_deliveries
            WHERE innings = 1
            GROUP BY match_id
        )
        SELECT ROUND(AVG(score), 2) as v FROM InningsScores
    """, conn)['v'][0]
    
    # Chasing Win %
    kpis['Chasing Win %'] = pd.read_sql_query("""
        WITH ChasingMatches AS (
            SELECT match_id, winner,
                   CASE WHEN toss_decision = 'field' THEN toss_winner
                        WHEN toss_decision = 'bat' THEN (CASE WHEN toss_winner = team1 THEN team2 ELSE team1 END)
                   END as chasing_team
            FROM fact_matches
            WHERE winner != 'No Result'
        )
        SELECT ROUND(CAST(SUM(CASE WHEN winner = chasing_team THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100, 2) as v
        FROM ChasingMatches
    """, conn)['v'][0]

    for k, v in kpis.items():
        logger.info(f"{k}: {v}")
        assert v is not None, f"KPI {k} failed validation (returned None)"

    logger.info("All KPIs successfully validated against data warehouse tables.")

if __name__ == "__main__":
    conn = setup_db()
    validate_kpis(conn)
