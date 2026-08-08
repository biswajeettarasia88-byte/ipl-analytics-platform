# Phase 1 Report: Data Acquisition

## Objective
Acquire authentic IPL match and ball-by-ball data from Cricsheet, preserving it in a raw, immutable format within the Bronze data layer.

## Ingestion Process Details
- **Source**: Cricsheet
- **Format Chosen**: JSON (`ipl_json.zip`) was selected as the most practical format because it preserves the nested, rich metadata (toss decisions, officials, match conditions, player registries) required for advanced analytics and modeling, which is sometimes lost or flattened prematurely in CSV formats.
- **Script**: Developed a reproducible Python ingestion script located at `src/ingestion/ingest.py`. It uses configurable paths from `config/config.yaml` to securely download and extract the data without hardcoded secrets.

## Verification & Metadata
- **Storage**: All raw JSON files (one per match) were successfully extracted to `data/raw/` (Bronze layer). No cleaning or transformations were performed.
- **Readable Files**: Verified that 1243 match JSON files exist and are correctly structured.
- **Seasons Detected**: The extracted metadata confirmed the presence of data spanning from the inaugural season ('2007/08') up to '2026'.

### `metadata.json` Summary
```json
{
    "source": "Cricsheet",
    "url": "https://cricsheet.org/downloads/ipl_json.zip",
    "download_timestamp": "2026-08-08T22:57:12.449",
    "file_format": "JSON",
    "number_of_matches": 1243,
    "seasons_covered": [
        "2007/08", "2009", "2009/10", "2011", "2012", "2013", 
        "2014", "2015", "2016", "2017", "2018", "2019", 
        "2020/21", "2021", "2022", "2023", "2024", "2025", "2026"
    ]
}
```

## Updates
- `docs/data_sources.md` was created to catalog our primary data sources.
- Phase 1 checkpoint is completed.

## Next Recommended Phase
**Phase 2: Data Quality & Validation**
- Implement schema and null checks on the Bronze JSON data.
- Ensure referential integrity before passing the data to the Silver layer.
