import os
import yaml
import urllib.request
import zipfile
import json
import logging
from datetime import datetime
from pathlib import Path

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_config():
    """Load the project configuration."""
    config_path = Path('config/config.yaml')
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path.absolute()}")
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def download_and_extract(source_url: str, dest_dir: Path):
    """Download zip file and extract to destination directory."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    zip_path = dest_dir / "ipl_temp.zip"
    
    logger.info(f"Downloading data from {source_url}...")
    urllib.request.urlretrieve(source_url, zip_path)
    logger.info("Download completed.")
    
    logger.info(f"Extracting files to {dest_dir}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(dest_dir)
        
    logger.info("Extraction completed. Removing zip file.")
    zip_path.unlink()

def generate_metadata(raw_dir: Path, source_url: str):
    """Generate metadata for the raw dataset."""
    logger.info("Generating metadata...")
    
    json_files = list(raw_dir.glob("*.json"))
    
    # Optional: we can remove the README.txt if it exists to keep only raw data
    readme_path = raw_dir / "README.txt"
    if readme_path.exists():
        # Keep it, but don't count it as a match
        pass
        
    seasons = set()
    matches_count = 0
    
    for jf in json_files:
        try:
            with open(jf, 'r', encoding='utf-8') as f:
                data = json.load(f)
            # Cricsheet format: data['info']['season']
            season = data.get('info', {}).get('season')
            if season:
                if isinstance(season, list):
                    seasons.update(season)
                else:
                    seasons.add(str(season))
            matches_count += 1
        except Exception as e:
            logger.warning(f"Could not parse {jf.name}: {e}")
            
    sorted_seasons = sorted(list(seasons))
    
    metadata = {
        "source": "Cricsheet",
        "url": source_url,
        "download_timestamp": datetime.now().isoformat(),
        "file_format": "JSON",
        "number_of_matches": matches_count,
        "seasons_covered": sorted_seasons
    }
    
    metadata_path = raw_dir / "metadata.json"
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=4)
        
    logger.info(f"Metadata saved to {metadata_path}")
    logger.info(f"Total matches ingested: {matches_count}")
    logger.info(f"Seasons covered: {sorted_seasons}")

def main():
    try:
        config = load_config()
        source_url = config['data']['source_url']
        raw_dir = Path(config['data']['raw_path'])
        
        # Download and extract
        download_and_extract(source_url, raw_dir)
        
        # Generate metadata
        generate_metadata(raw_dir, source_url)
        
        logger.info("Ingestion phase completed successfully.")
        
    except Exception as e:
        logger.error(f"Ingestion failed: {e}")
        raise

if __name__ == "__main__":
    main()
