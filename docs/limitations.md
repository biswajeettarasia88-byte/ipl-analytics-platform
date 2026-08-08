# Project Limitations & Future Scope

## Current Limitations

1. **Static Data Strategy**: The pipeline currently operates in batch mode. While reproducible, it lacks a live streaming component (e.g., Kafka) to ingest ball-by-ball updates directly from APIs during a live match.
2. **Feature Engineering Depth**: The ML feature `team_recent_win_rate` uses a simplified window approach. Advanced ELO-style ratings for teams and players would significantly improve the baseline prediction accuracy.
3. **Database Environment**: For testing portability, PostgreSQL emulation was achieved using in-memory SQLite and Pandas mapping. A dedicated PostgreSQL 15 server is required to unlock the full potential of Window Functions utilized in `sql/analysis/queries.sql`.
4. **Impact Player Rule**: The 2023+ season introduced the Impact Player rule, fundamentally altering pacing strategies and required run rate dynamics. The XGBoost model learns this implicitly through the 2023/2024 splits, but does not yet feature an explicit `impact_player_available` boolean flag in the schema.

## Future Roadmap
- **Phase 14**: Implement PySpark for distributed Silver-layer transformations on scale.
- **Phase 15**: Deploy model via FastAPI microservice rather than directly inside Streamlit.
- **Phase 16**: Kafka + Redis architecture for live broadcast latency (< 500ms).
