# Project Plan

The project is divided into clearly separated phases. Each phase must be completed, tested, and documented before proceeding.

## Phase 0: Preparation (Current)
- Inspect workspace.
- Create folder structure and base documentation.

## Phase 1: Data Acquisition & Ingestion
- Download authentic IPL match and ball-by-ball data from Cricsheet.
- Save to Bronze layer (`data/raw`).
- Establish source metadata.

## Phase 2: Data Quality & Validation
- Validate Bronze data (schema, nulls, duplicates, referential integrity).
- Generate data quality reports.

## Phase 3: Data Cleaning & Silver Layer
- Clean and standardize the data.
- Save to Silver layer (`data/staging`).

## Phase 4: Database Setup & Gold Layer
- Setup PostgreSQL database/schema.
- Design and create Fact and Dimension tables (DDL).
- Load transformed data into the Gold layer.

## Phase 5: SQL Analytics & Marts
- Create analytical marts and views.
- Write advanced SQL for insights (CTEs, window functions).

## Phase 6: Machine Learning Preparation
- Feature engineering for Match Win Probability.
- Create analytical datasets avoiding target leakage.

## Phase 7: Machine Learning Modeling
- Train baseline Logistic Regression model.
- Train advanced XGBoost model using chronological splitting.
- Evaluate and save model metrics.

## Phase 8: Model Explainability
- Implement SHAP to explain global and local feature importance.

## Phase 9: Application Development
- Build the Streamlit application for EDA and Model prediction/explanation.

## Phase 10: BI Dashboard
- Develop Power BI data model and dashboard.

## Phase 11: Testing & QA
- Write and execute unit, integration, and data tests using Pytest.

## Phase 12: DevOps & Deployment
- Containerize with Docker.
- Setup GitHub Actions CI.
- Prepare deployment configuration.

## Phase 13: Final Review & Documentation
- Complete all documentation (Data Dictionary, Lineage, Final Report).
- Final review by Agent 14.
