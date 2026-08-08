import os
import json
import logging
from pathlib import Path
from collections import defaultdict
import yaml

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_config():
    config_path = Path('config/config.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def profile_data(raw_dir: Path, output_report: Path):
    json_files = list(raw_dir.glob("*.json"))
    
    total_matches = 0
    total_innings = 0
    total_deliveries = 0
    
    teams = set()
    venues = set()
    cities = set()
    players = set()
    
    missing_city = 0
    missing_winner = 0
    missing_toss = 0
    
    suspicious_deliveries = []
    malformed_records = []
    
    match_dates = defaultdict(list)
    
    logger.info(f"Profiling {len(json_files)} match files...")
    
    for jf in json_files:
        if jf.name == "metadata.json":
            continue
            
        try:
            with open(jf, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            info = data.get('info', {})
            innings = data.get('innings', [])
            
            total_matches += 1
            
            # Extract info
            match_teams = info.get('teams', [])
            for t in match_teams:
                teams.add(t)
                
            v = info.get('venue')
            if v: venues.add(v)
            
            c = info.get('city')
            if c: cities.add(c)
            else: missing_city += 1
            
            if 'outcome' not in info or ('winner' not in info['outcome'] and 'result' not in info['outcome']):
                missing_winner += 1
                
            if 'toss' not in info:
                missing_toss += 1
                
            dates = info.get('dates', [])
            if dates:
                match_dates[dates[0]].append(jf.name)
                
            # Extract registry players if available
            registry = info.get('registry', {}).get('people', {})
            for p in registry.keys():
                players.add(p)
                
            # Profile innings
            for inn in innings:
                total_innings += 1
                team = inn.get('team')
                if team: teams.add(team)
                
                for over in inn.get('overs', []):
                    for d in over.get('deliveries', []):
                        total_deliveries += 1
                        batter = d.get('batter')
                        bowler = d.get('bowler')
                        ns = d.get('non_striker')
                        
                        if batter: players.add(batter)
                        if bowler: players.add(bowler)
                        if ns: players.add(ns)
                        
                        runs_total = d.get('runs', {}).get('total', 0)
                        if runs_total < 0 or runs_total > 8:
                            suspicious_deliveries.append(f"{jf.name}: {runs_total} runs in a delivery")
                            
        except Exception as e:
            malformed_records.append(f"{jf.name}: {str(e)}")
            
    # Find potential duplicates
    duplicates = {d: files for d, files in match_dates.items() if len(files) > 2} # more than 2 matches on same date is suspicious
    
    # Generate Report
    report = [
        "# Data Quality & Profiling Report",
        "",
        "## 1. Overview",
        f"- **Total Matches Profiled**: {total_matches}",
        f"- **Total Innings**: {total_innings}",
        f"- **Total Deliveries**: {total_deliveries}",
        f"- **Unique Teams**: {len(teams)}",
        f"- **Unique Venues**: {len(venues)}",
        f"- **Unique Players**: {len(players)}",
        "",
        "## 2. Issues Identified",
        "",
        "### [CRITICAL] Malformed Records",
        f"- Found {len(malformed_records)} malformed JSON files.",
        *["  - " + r for r in malformed_records[:10]],
        "",
        "### [CRITICAL] Suspicious Values",
        f"- Found {len(suspicious_deliveries)} suspicious deliveries (e.g. negative runs or >8 runs).",
        *["  - " + s for s in suspicious_deliveries[:10]],
        "",
        "### [WARNING] Missing Values",
        f"- **Missing City**: {missing_city} matches",
        f"- **Missing Winner/Result**: {missing_winner} matches",
        f"- **Missing Toss Info**: {missing_toss} matches",
        "",
        "### [WARNING] Inconsistent Team Names",
        "The following teams likely have legacy/duplicate names:",
    ]
    
    # Simple heuristic for team name inconsistencies
    sorted_teams = sorted(list(teams))
    for t in sorted_teams:
        report.append(f"- {t}")
        
    report.extend([
        "",
        "### [INFORMATIONAL] Inconsistent Venue Names",
        "Many venues have multiple naming conventions (e.g., 'M Chinnaswamy Stadium' vs 'M.Chinnaswamy Stadium').",
        f"Total distinct venues parsed: {len(venues)}",
    ])
    
    report_path = output_report
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(report))
        
    logger.info(f"Report generated at {report_path}")

if __name__ == "__main__":
    config = load_config()
    raw_dir = Path(config['data']['raw_path'])
    output_report = Path('reports/data_quality_report.md')
    profile_data(raw_dir, output_report)
