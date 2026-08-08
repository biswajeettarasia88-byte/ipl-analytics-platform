# Architecture

The IPL Analytics & Decision Intelligence Platform follows a robust, production-grade architecture.

## Data Flow
`SOURCE -> INGESTION -> BRONZE -> VALIDATION -> SILVER -> TRANSFORMATION -> GOLD -> POSTGRESQL -> SQL ANALYTICS -> POWER BI -> ML -> SHAP -> STREAMLIT -> TESTING -> CI/CD -> DEPLOYMENT`

## Medallion Data Architecture
1. **Bronze (Raw)**: Immutable storage of raw data ingested from Cricsheet.
2. **Silver (Cleaned/Validated)**: Data that has passed quality checks, standardized formatting, and null handling.
3. **Gold (Analytical)**: Feature-engineered datasets and the PostgreSQL Star Schema.

## Technology Stack
- **Data Source**: Cricsheet
- **Programming**: Python
- **Data Processing**: Pandas
- **Database**: PostgreSQL
- **Analytics**: PostgreSQL SQL, Pandas + Plotly
- **Business Intelligence**: Power BI
- **Machine Learning**: Scikit-learn + XGBoost
- **Explainability**: SHAP
- **Application**: Streamlit
- **Testing**: Pytest
- **Version Control & CI**: Git, GitHub, GitHub Actions
- **Containerization**: Docker

## Database Design (Dimensional Model)

### Fact Tables
- `fact_matches`
- `fact_match_teams`
- `fact_deliveries`
- `fact_player_match_performance`

### Dimension Tables
- `dim_player`
- `dim_team`
- `dim_venue`
- `dim_date`
- `dim_season`

### Analytical Marts
- `mart_team_season`
- `mart_batting`
- `mart_bowling`
- `mart_venue`
- `mart_match_state`
