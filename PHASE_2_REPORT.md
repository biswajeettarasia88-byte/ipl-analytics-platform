# Phase 2 Report: Data Profiling and Validation

## Objective
To understand the raw dataset through automated profiling before making any modifications, and to identify potential data quality issues that need to be addressed in the subsequent Silver layer transformations.

## Automated Validation
- A profiling script (`src/validation/profiler.py`) was developed to iterate over the 1,243 raw JSON match files.
- Automated tests (`tests/test_validation.py`) were created and passed, confirming the schema integrity and metadata existence of the raw files.

## Summary of Findings (Data Quality Report)
- **Total Matches Profiled**: 1243
- **Total Innings**: 2514
- **Total Deliveries**: 295,732
- **Unique Teams**: 19
- **Unique Venues**: 60
- **Unique Players**: 966

### Critical Issues
- **None**: Zero malformed JSON records and zero highly suspicious deliveries (e.g., negative runs) were detected in the raw data.

### Warnings
- **Missing City**: 51 matches are missing the `city` attribute in their metadata. These will need to be imputed based on the `venue` during transformation.
- **Inconsistent Team Names**: Identified multiple teams that have undergone naming changes or contain minor inconsistencies, which will require standardization. Examples:
  - 'Delhi Daredevils' vs 'Delhi Capitals'
  - 'Kings XI Punjab' vs 'Punjab Kings'
  - 'Rising Pune Supergiant' vs 'Rising Pune Supergiants'
  - 'Royal Challengers Bangalore' vs 'Royal Challengers Bengaluru'

### Informational
- **Inconsistent Venue Names**: Total of 60 distinct venues found. Many of these are likely different spellings or historical names for the same physical stadiums (e.g., 'M Chinnaswamy Stadium' vs 'M.Chinnaswamy Stadium'). This will require a mapping dictionary in Phase 3.

## Decisions Made
- No raw files were modified. All data quality issues were merely profiled and flagged.
- A standardization mapping for teams and venues will be explicitly documented and implemented during Phase 3 (Data Cleaning).
- Missing cities will be mapped from their corresponding venues during the creation of the Silver layer.

## Next Recommended Phase
**Phase 3: Data Cleaning & Silver Layer**
- Apply the data transformations identified in this report.
- Standardize team names, venue names, and handle missing values.
- Flatten the hierarchical JSON into tabular formats (e.g., Matches, Deliveries) for analytical storage.
