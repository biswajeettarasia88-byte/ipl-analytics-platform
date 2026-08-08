import json
from pathlib import Path
import pytest

def test_raw_data_metadata_exists():
    metadata_path = Path('data/raw/metadata.json')
    assert metadata_path.exists(), "Metadata file should exist in data/raw/"
    
def test_raw_data_match_count():
    with open('data/raw/metadata.json', 'r') as f:
        metadata = json.load(f)
    assert metadata['number_of_matches'] > 0, "There should be at least 1 match ingested."
    
def test_sample_raw_file_schema():
    raw_dir = Path('data/raw')
    json_files = list(raw_dir.glob("*.json"))
    json_files = [jf for jf in json_files if jf.name != 'metadata.json']
    
    if len(json_files) > 0:
        sample = json_files[0]
        with open(sample, 'r') as f:
            data = json.load(f)
        
        # Verify basic schema
        assert 'info' in data, f"'info' key missing in {sample.name}"
        assert 'innings' in data, f"'innings' key missing in {sample.name}"
        
        # Verify info schema
        assert 'teams' in data['info'], f"'teams' missing in {sample.name} info"
        assert len(data['info']['teams']) == 2, f"Match should have exactly 2 teams"
