# Phase 3 Report: Data Cleaning and Silver Layer

## Objective
Create clean, standardized, and normalized datasets from the raw Bronze layer data while preserving traceability.

## Process Summary
- Executed the `src/cleaning/transformer.py` script to flatten and standardize the 1243 raw JSON match files into analytical relational tables.
- All extracted tables have been written to `data/processed/` (Silver layer) as CSV files.
- Automated validation tests (`tests/test_silver.py`) were run and passed.

## Output Statistics
- **Total Matches Generated**: 1,243
- **Total Deliveries Generated**: 295,732
- **Rows Removed**: 0 (No matches were removed. No deliveries were removed. Invalid duplicates were not found in the raw dataset during profiling, thus preserving all valid matches.)
- **Values Standardized (Team Names)**: Applied to 561 matches where legacy names (e.g., 'Delhi Daredevils', 'Kings XI Punjab', 'Rising Pune Supergiant') were converted to canonical forms.
- **Values Standardized (Venue Names)**: Applied to 566 matches where stadium names were consolidated (e.g., merging various spellings of 'M Chinnaswamy Stadium').
- **Missing Values Handled**: 51 matches lacked a `city` attribute in the raw data. 100% of these were successfully imputed using their corresponding standardized venue locations.

## Data Lineage
- Created `docs/data_lineage.md` detailing the transition and transformation logic from the JSON Bronze layer to the CSV Silver layer.
- Traceability is fully preserved via the original `match_id` present in both `matches.csv` and `deliveries.csv`.

## Next Recommended Phase
**Phase 4: Database Setup & Gold Layer**
- Design PostgreSQL schema (Fact and Dimension tables).
- Create DDL scripts.
- Ingest the Silver CSV data into the PostgreSQL relational database.
