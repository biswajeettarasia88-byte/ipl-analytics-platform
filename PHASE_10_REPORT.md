# Phase 10 Report: Streamlit Application

## Objective
To develop a multi-page interactive frontend interface using Streamlit, providing users with live access to historical data analytics, real-time Machine Learning win predictions, and model transparency via SHAP.

## Implementation Details

### 1. Application Architecture
Constructed `streamlit/app.py`, which is deployed as a 7-page analytical hub:
- **Overview, Teams, Players, Venues, Match Analytics**: Acting as the presentation tier for historical insights.
- **Match Win Predictor**: The core ML interface linking the XGBoost model to user inputs.
- **Model Explanation**: Visualizes the SHAP outputs generated in Phase 9 to guarantee model interpretability.

### 2. Live Win Predictor Features
- **Dynamic Derivation**: The user inputs raw match state (current score, target, overs, wickets). The application dynamically computes contextual variables in the background (`Required Run Rate`, `Balls Remaining`, `Current Run Rate`).
- **Data Validation & Error Handling**: Built-in strict logic checks to ensure inputs are physically possible (e.g., stopping users from inputting > 10 wickets, > 20 overs, or selecting identical batting/bowling teams).
- **Probability Output**: Displays a live, opposing progress-bar metric reflecting the exact probability of Team A vs. Team B winning.

### 3. Local Deployment
The application has been tested locally and runs successfully on the `8501` port via:
```bash
streamlit run streamlit/app.py
```

## Artifacts Generated
- `streamlit/app.py` (Source code for the frontend application)
- `docs/streamlit.md` (Detailed application architecture documentation)

## Next Recommended Phase
**Phase 11: Testing & QA**
- Developing pytest suites for the Streamlit backend logic, ML predictions, and ensuring continuous integration readiness.
