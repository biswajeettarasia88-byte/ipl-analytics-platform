# Data Sources

## Primary Source: Cricsheet
- **URL**: https://cricsheet.org/
- **Format Used**: JSON
- **Description**: Cricsheet provides structured, ball-by-ball data for various cricket matches. We ingest the IPL JSON dump, which contains rich metadata (toss, officials, season, venue, player registry) and detailed delivery-level events.

### Ingestion Details
- The data is downloaded as a compressed `.zip` archive.
- Extracted into the `data/raw/` directory.
- This directory serves as our immutable Bronze layer. No data cleaning or transformation is performed on these files.
- An automated metadata JSON is generated upon ingestion to track the extraction timestamp, total matches, and covered seasons.
