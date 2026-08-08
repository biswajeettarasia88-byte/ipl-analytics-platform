# Power BI Data Sources

This document outlines the connection and data flow architecture from the Data Warehouse to the Power BI Dashboard.

## Primary Data Source
- **Database Engine**: PostgreSQL 15+
- **Connection Type**: DirectQuery (recommended for near-real-time analytical scale) or Import Mode (if performance on standard hardware is preferred given the dataset size).
- **Authentication**: Database Credentials (via `.env` properties: `POSTGRES_USER`, `POSTGRES_PASSWORD`).

## Tables & Views Imported
The Power BI semantic model connects to the following Gold Layer components (Star Schema):

### 1. Dimension Tables
- `dim_team`: Serves as the primary filter for team-based analytics (Slicers, tooltips).
- `dim_player`: Serves as the primary filter for batter/bowler/fielder analyses.
- `dim_venue`: Maps to geographic or stadium-level visual drill-downs.
- `dim_season`: Enables temporal slicing across different IPL years.
- `dim_date`: Supports time-intelligence functions (YTD, MTD, Rolling calculations).

### 2. Fact Tables
- `fact_matches`: Core fact table for match-level outcomes (win margins, toss impacts, chasing success).
- `fact_deliveries`: Extremely granular ball-by-ball fact table. Used for strike rates, economies, boundaries, dot ball percentages.
- `fact_player_match_performance`: Pre-aggregated player performance at the match level to optimize rendering of Player Analytics pages.

### 3. Pre-calculated SQL Marts (Views)
To improve dashboard rendering performance, Power BI can directly query the materialized views created in Phase 5 & 6:
- `mart_team_season`: Powers "Team Performance Trends".
- `mart_batting` & `mart_bowling`: Powers the "Player Analytics" leaderboards.
- `mart_venue`: Powers the "Venue Analytics" summary matrices.

## Data Refresh Strategy
- Currently configured for static load (Import).
- Can be scheduled via Power BI Service Gateway to refresh daily post-match via the ELT pipeline.
