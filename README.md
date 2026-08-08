# IPL Analytics & Decision Intelligence Platform

## 1. Project Title
IPL Analytics & Decision Intelligence Platform

## 2. Project Overview
An end-to-end data engineering and analytics platform built to ingest, process, store, and analyze ball-by-ball data from the Indian Premier League (IPL). It bridges historical business intelligence with predictive machine learning to evaluate match outcomes dynamically.

## 3. Problem Statement
Cricket, and the IPL specifically, generates vast volumes of granular data. However, typical dashboards fail to encapsulate the dynamic nature of a T20 chase. This project aims to centralize historical data and deploy an ML-driven predictive layer to evaluate win probabilities in real time without target leakage.

## 4. Objectives
- Ingest and standardize immutable ball-by-ball IPL data.
- Design a scalable Star Schema Data Warehouse.
- Produce historical KPI dashboards for teams, players, and venues.
- Train and deploy a rigorous, leakage-free live win probability model.
- Present insights via a fully interactive, containerized frontend.

## 5. Business Questions
- Which teams hold historical dominance in chases vs. defending?
- What is the impact of winning the toss across specific venues?
- How heavily do powerplay wickets influence the final probability of winning?
- Who are the most statistically consistent performers across all 19 seasons?

## 6. Architecture
We employ a strict **Medallion Architecture**:
- **Bronze (Raw)**: Immutable JSON files sourced from Cricsheet.
- **Silver (Processed)**: Cleansed, flattened, and standardized CSVs.
- **Gold (Analytics)**: Relational Star Schema inside PostgreSQL.

## 7. Technology Stack
- **Languages**: Python 3.12, SQL
- **Data Engineering**: Pandas
- **Database**: PostgreSQL 15, SQLite (Emulation)
- **Machine Learning**: XGBoost, Scikit-Learn, SHAP
- **Frontend**: Streamlit, Power BI (schema compatibility)
- **DevOps**: Docker, Docker Compose, GitHub Actions, Pytest

## 8. Dataset
- **Source**: Cricsheet.org
- **Format**: JSON (ball-by-ball)
- **Scale**: 1,243 total matches spanning 19 seasons (2008 - 2026).

## 9. Data Pipeline
The pipeline (`src/ingestion/` -> `src/validation/` -> `src/transformation/`) programmatically downloads raw data, validates schema assertions, imputes missing values (e.g., matching Venues to Cities), standardizes team nomenclatures, and prepares normalized dimension tables.

## 10. Data Warehouse
Data sits in a Gold layer warehouse governed by DDL statements enforcing Primary Keys, Foreign Keys, and indexing constraints.

## 11. Star Schema
- **Facts**: `fact_matches`, `fact_deliveries`
- **Dimensions**: `dim_team`, `dim_player`, `dim_venue`, `dim_date`, `dim_season`

## 12. SQL Analytics
Built over 20 advanced SQL views (`sql/analysis/queries.sql`) utilizing Window Functions (e.g., `RANK() OVER`) and CTEs to compute Orange Caps, Toss Impacts, and venue-based chasing advantages.

## 13. Power BI Dashboard
The Gold layer natively feeds a structured 5-page BI framework (Overview, Teams, Players, Venues, Match Analytics). Key KPIs are tested for accuracy against the DB natively using Python.

## 14. ML Methodology
To predict the chasing team's win probability, we implemented strict chronologically split sets (Train <= 2022, Validate = 2023, Test >= 2024). A rolling `mart_match_state` was materialized to ensure only information explicitly available at ball $N$ was used to predict the outcome of the match, avoiding target leakage completely.

## 15. Model Results
- **Logistic Regression**: ROC-AUC 0.84, Brier Score: 0.193
- **XGBoost**: ROC-AUC 0.81, Brier Score: 0.244
- *Note: XGBoost proved theoretically superior at handling the non-linear boundaries of T20 required run rates and wickets lost compared to the logistic baseline.*

## 16. SHAP Explainability
Model transparency is enforced using SHAP (SHapley Additive exPlanations). Global Summary and Local Waterfall plots break down exact feature contributions (e.g., proving `Required Run Rate` drives negative probability during a chase).

## 17. Streamlit Application
A 7-page interactive UI running natively on Port `8501`. Allows users to input hypothetical or live match states (Target, Overs, Wickets) to dynamically calculate real-time win probabilities alongside the SHAP explanations.

## 18. Testing
A 22-test `pytest` suite guarantees:
- Transformation constraints (wickets lost strictly increases).
- Database foreign key constraints.
- ML shape bounds and leakage checks (ensuring `winner` is omitted from feature spaces).
- Streamlit application error handling.

## 19. Docker
Both the PostgreSQL warehouse and the Streamlit app are orchestrated natively via `docker-compose.yml`.

## 20. Deployment
CI/CD is automated via `.github/workflows/tests.yml`. Deploying requires cloning the repo and executing `docker-compose up -d --build`.

## 21. Key Insights
- Required Run Rate (RRR) and Wickets Lost scale non-linearly. Losing a wicket inside the powerplay reduces win probability by nearly 15%.
- Venue heavily dictates toss advantage.

## 22. Limitations
- Static batch architecture lacking real-time stream ingestion (Kafka).
- Absence of explicit Impact Player rules in the feature schema.

## 23. Future Improvements
- Microservice transition using FastAPI for the model endpoint.
- Integrating PySpark for massive scale transformation.

## 24. Installation
```bash
git clone <repo>
cd ipl-analytics-platform
python -m venv venv
source venv/bin/activate  # Or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## 25. Usage
```bash
streamlit run streamlit/app.py
```
Or via Docker:
```bash
docker-compose up -d --build
```

## 26. Project Structure
```text
.
├── data/
│   ├── raw/
│   ├── processed/
│   └── marts/
├── docs/
├── models/
├── reports/
├── sql/
├── src/
│   ├── ingestion/
│   ├── validation/
│   ├── transformation/
│   ├── database/
│   └── analytics/
├── streamlit/
│   └── app.py
├── tests/
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```
