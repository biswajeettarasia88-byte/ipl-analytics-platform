# Streamlit Application Architecture

## Objective
To provide an interactive frontend for the IPL Analytics & Decision Intelligence platform, enabling users to consume analytical dashboards and execute live Machine Learning predictions without writing code.

## File Structure
- `streamlit/app.py`: The main multi-page Streamlit application.

## Application Modules

### 1. Business Intelligence Views (Pages 1-5)
- **Overview, Teams, Players, Venues, Match Analytics**: These pages serve as the presentation layer for the BI metrics derived in Phase 5 and 7. Currently, they display static placeholders and structured layouts, mimicking the architecture that would be deployed to Power BI.

### 2. Live Win Predictor (Page 6)
- **Engine**: XGBoost classification pipeline.
- **Functionality**: Accepts real-time match state parameters (Teams, Venue, Target, Current Score, Overs, Wickets).
- **Derived Real-Time Features**: The application dynamically computes `Runs Remaining`, `Balls Remaining`, `Current Run Rate (CRR)`, and `Required Run Rate (RRR)` on the fly so the user doesn't have to input them manually.
- **Validation**: Strict boundary constraints prevent nonsensical inputs (e.g., scoring more runs than the target, losing more than 10 wickets, identical batting and bowling teams).
- **Output**: Renders an interactive probability progress bar showing the live win percentage for both the batting and bowling teams.

### 3. Model Explainability (Page 7)
- Displays the static SHAP (SHapley Additive exPlanations) visual artifacts (`shap_summary.png` and `shap_waterfall_individual.png`) generated in Phase 9.
- This ensures full transparency for stakeholders, visually proving *why* the XGBoost algorithm generates specific probabilities.

## Running Locally
To launch the dashboard, execute the following from the project root:
```bash
# Activate the virtual environment
.\venv\Scripts\activate

# Run the Streamlit server
streamlit run streamlit/app.py
```
