# Project Walkthrough

## How to navigate this repository

Welcome to the IPL Analytics & Decision Intelligence Platform. This walkthrough explains how the project components interact.

### 1. Start at the Data (Bronze Layer)
Look inside `data/raw/`. This is where `src/ingestion/download_cricsheet.py` dumps the pristine Cricsheet JSON files.

### 2. Move to the Transformations (Silver Layer)
Explore `src/transformation/clean_data.py`. This script is the heavy lifter. It parses the JSON, normalizes team names to their modern equivalents, maps stadiums to specific cities to prevent nulls, and flattens the ball-by-ball metadata into manageable CSVs stored in `data/processed/`.

### 3. Observe the Database (Gold Layer)
Open `sql/ddl/schema.sql`. You'll see a pristine Star Schema. We enforce strict foreign keys to ensure referential integrity. The `src/database/loader.py` script acts as the bridge that pumps the Silver CSVs into this SQL warehouse.

### 4. Machine Learning Engineering
Navigate to `src/analytics/feature_engineering.py`. This is the most crucial file for the ML model. It iterates over the deliveries and computes the "Match State" (runs required, wickets lost, required run rate) for every single ball.
*Crucially*, it uses `shift()` functions to ensure that at Ball $N$, the model only sees the score as it was at Ball $N-1$, aggressively preventing Target Leakage.

### 5. Training and Explainability
Check `src/analytics/train_models.py` to see the XGBoost implementation. Then look at `src/analytics/explain_model.py` to see how SHAP values are extracted to understand *why* the model makes its decisions. The outputs are saved as visuals in `reports/figures/`.

### 6. The User Interface
Finally, open `streamlit/app.py`. This is where it all comes together. The UI loads the `.joblib` model from the `models/` directory, accepts live user input, validates it, and generates a dynamic win probability progress bar alongside historical BI placeholders.

### 7. Deployment
The entire stack is containerized. Check `docker-compose.yml` to see how the PostgreSQL database and the Streamlit app are networked together. 
Check `.github/workflows/tests.yml` to see the CI pipeline running our 22 `pytest` cases on every commit.
