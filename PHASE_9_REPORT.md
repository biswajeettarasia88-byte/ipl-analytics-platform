# Phase 9 Report: Model Explainability

## Objective
Implement global and local explainability for the XGBoost Win Predictor using SHAP (SHapley Additive exPlanations), ensuring predictions are transparent, interpretable, and devoid of hallucinations.

## Implementation Details

### 1. SHAP Integration
- Installed the `shap` library and integrated it into a dedicated explainability script (`src/analytics/explain_model.py`).
- Extracted the trained XGBoost model and its pre-processing pipeline from Phase 8.
- Computed exact SHAP values using `shap.TreeExplainer` over a representative sample of the 2024+ test set.

### 2. Global Interpretability
- Generated a SHAP Summary Plot to identify the macroeconomic drivers of win probability across thousands of deliveries.
- **Insights**: The model heavily relies on `Required Run Rate` and `Wickets Lost` as primary negative indicators (higher values decrease win probability), while `Current Run Rate` and `Balls Remaining` dynamically shift outcomes based on match context.

### 3. Local Explainability (Individual Delivery)
- Generated a SHAP Waterfall Plot for a specific individual delivery prediction, dissecting exactly how the model arrived at its probabilistic conclusion.
- The output successfully decomposed the prediction into specific positive feature contributions (factors helping the chasing team) and negative feature contributions (factors hurting the chasing team).
- Example documented in `docs/model_explainability.md`.

## Artifacts Generated
- `src/analytics/explain_model.py` (Script to generate SHAP visualizations)
- `reports/figures/shap_summary.png` (Global feature importance plot)
- `reports/figures/shap_waterfall_individual.png` (Individual delivery breakdown plot)
- `docs/model_explainability.md` (Detailed Markdown documentation with the quantitative breakdown)

## Next Recommended Phase
**Phase 10: Final Dashboard & Application Integration** (Optional/Suggested depending on user scope) OR **Phase 11: Testing & CI/CD**
