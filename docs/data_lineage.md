# Data Lineage

## Bronze Layer -> Silver Layer

### Source (Bronze)
- **Path**: `data/raw/*.json`
- **Format**: JSON
- **Description**: Immutable raw Cricsheet data files. Each file represents a single match.

### Transformations Applied
The Python script `src/cleaning/transformer.py` performs the following operations:
1. **Team Name Standardization**: Legacy and inconsistent team names (e.g., 'Delhi Daredevils' to 'Delhi Capitals', 'Kings XI Punjab' to 'Punjab Kings') are mapped to their canonical forms.
2. **Venue Name Standardization**: Multiple historical and spelled variations of stadiums are mapped to standard names (e.g., 'M Chinnaswamy Stadium' -> 'M Chinnaswamy Stadium, Bengaluru').
3. **Missing Value Handling**: Missing `city` attributes are deterministically imputed by parsing the standardized `venue` name string.
4. **Data Flattening**: The hierarchical JSON is decomposed into relational structures (Matches, Deliveries, Players, Teams, Venues).

### Destination (Silver)
- **Path**: `data/processed/`
- **Format**: CSV
- **Files**:
  - `matches.csv`: Match-level metadata (toss, outcome, season, venue). Traceable via `match_id`.
  - `deliveries.csv`: Ball-by-ball events. Traceable via `match_id`, `innings`, `over`, `ball`.
  - `teams.csv`: Distinct standardized teams.
  - `venues.csv`: Distinct standardized venues.
  - `players.csv`: Distinct player registry mappings.

_Note: All transformations preserve the original `match_id` to allow full traceability back to the Bronze JSON files._
