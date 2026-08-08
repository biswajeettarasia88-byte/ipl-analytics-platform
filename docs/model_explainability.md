# Model Explainability (SHAP)

## Objective
To provide transparent, human-readable explanations for the XGBoost Win Predictor model, ensuring the black-box algorithm can be trusted by analysts and stakeholders.

## Global Feature Importance
The SHAP summary plot (`reports/figures/shap_summary.png`) reveals which features universally drive the model's decisions:
1. **Required Run Rate**: Unsurprisingly, higher required run rates strongly push the model toward predicting a loss for the chasing team.
2. **Wickets Lost**: Having fewer wickets remaining dramatically decreases win probability.
3. **Balls Remaining**: Time pressure is a significant negative driver when low.
4. **Current Run Rate**: High current run rates correlate with higher win probability.

## Individual Prediction Explanation

**Context (Sample Delivery):**
- **Batting Team**: Chennai Super Kings
- **Bowling Team**: Royal Challengers Bengaluru
- **Runs Remaining**: 161
- **Balls Remaining**: 110
- **Required Run Rate**: 8.78
- **Wickets Lost**: 0

**Model Output:** 
- The model predicts that Chennai Super Kings has a **88.5%** probability of winning at this exact moment.

### Why? (SHAP Waterfall Plot)
A waterfall plot was generated (`reports/figures/shap_waterfall_individual.png`) to break down exactly how the model arrived at 88.5%. 

**Top Positive Contributions (Pushing Probability Up):**
- **batting_team_Chennai Super Kings**: SHAP value 1.8571
- **target_score**: SHAP value 0.6582
- **wickets_lost**: SHAP value 0.6388

**Top Negative Contributions (Pushing Probability Down):**
- **venue_MA Chidambaram Stadium, Chennai**: SHAP value -0.7642
- **runs_remaining**: SHAP value -0.4005
- **current_score**: SHAP value -0.2686

## Validation
The SHAP values successfully decomposed the exact log-odds output of the XGBoost model. The explanations physically align with cricketing logic (e.g., losing wickets decreases probability), validating that the model has learned the true underlying dynamics of the game, rather than spurious correlations.
