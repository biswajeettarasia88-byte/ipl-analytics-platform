import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
from pathlib import Path
import shap
import matplotlib.pyplot as plt

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="IPL Analytics & Decision Intelligence", page_icon="🏏", layout="wide")

# --- LOAD MODELS & DATA ---
@st.cache_resource
def load_ml_assets():
    models_dir = Path('models')
    try:
        pipeline = joblib.load(models_dir / 'xgboost.joblib')
        with open(models_dir / 'features.json', 'r') as f:
            features = json.load(f)
        return pipeline, features
    except Exception as e:
        st.error(f"Failed to load ML models. Are you running from the project root? Error: {e}")
        return None, None

@st.cache_data
def load_dropdown_data():
    try:
        # Load unique teams and venues from the dim tables
        processed_dir = Path('data/processed')
        teams_df = pd.read_csv(processed_dir / 'teams.csv')
        matches_df = pd.read_csv(processed_dir / 'matches.csv')
        
        teams = sorted(teams_df['team1'].dropna().unique().tolist())
        venues = sorted(matches_df['venue'].dropna().unique().tolist())
        return teams, venues
    except Exception as e:
        # Fallback to hardcoded if not found
        st.error(f"Failed to load dimension data. Error: {e}")
        return ['Chennai Super Kings', 'Mumbai Indians', 'Royal Challengers Bengaluru', 'Kolkata Knight Riders'], ['Wankhede Stadium', 'M Chinnaswamy Stadium']

pipeline, ml_features = load_ml_assets()
teams_list, venues_list = load_dropdown_data()

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "Overview", 
    "Teams", 
    "Players", 
    "Venues", 
    "Match Analytics", 
    "Match Win Predictor", 
    "Model Explanation"
])

# --- HELPER FUNCTIONS ---
def get_prediction(batting_team, bowling_team, venue, target, current_score, overs_completed, wickets_lost):
    if not pipeline: return None
    
    # Validation
    if current_score > target:
        st.error("Current score cannot be greater than target.")
        return None
    if wickets_lost > 10:
        st.error("Wickets lost cannot be greater than 10.")
        return None
    if overs_completed > 20:
        st.error("Overs completed cannot be greater than 20.")
        return None
    if batting_team == bowling_team:
        st.error("Batting team cannot be the same as bowling team.")
        return None
        
    runs_remaining = target - current_score
    balls_remaining = 120 - (overs_completed * 6)
    
    current_run_rate = (current_score / (overs_completed * 6)) * 6 if overs_completed > 0 else 0
    required_run_rate = (runs_remaining / balls_remaining) * 6 if balls_remaining > 0 else 0
    
    # Construct input dataframe matching `features.json`
    input_data = {
        'batting_team': batting_team,
        'bowling_team': bowling_team,
        'venue': venue,
        'target_score': target,
        'current_score': current_score,
        'overs_completed': overs_completed,
        'wickets_lost': wickets_lost,
        'runs_remaining': runs_remaining,
        'balls_remaining': balls_remaining,
        'current_run_rate': current_run_rate,
        'required_run_rate': required_run_rate,
        'recent_run_rate': current_run_rate, # Approximation for live UI
        'team_recent_win_rate': 0.5, # Static fallback
        'venue_chase_success_rate': 0.5 # Static fallback
    }
    
    df = pd.DataFrame([input_data])
    df = df[ml_features] # Ensure order
    
    with st.spinner("Calculating probability..."):
        prob = pipeline.predict_proba(df)[0][1] # Probability of Class 1 (Batting team win)
        
    return prob, df, current_run_rate, required_run_rate, runs_remaining, balls_remaining

# --- PAGES ---

if page == "Overview":
    st.title("IPL Overview Dashboard")
    st.info("Power BI integration active. Showing top-level KPI placeholders.")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Matches", "1,243")
    col2.metric("Total Seasons", "19")
    col3.metric("Total Runs", "401,738")
    col4.metric("Total Wickets", "14,705")
    
elif page == "Teams":
    st.title("Team Analytics")
    st.write("View historical performance, powerplay metrics, and win rates.")
    team = st.selectbox("Select Team", teams_list)
    st.image("https://upload.wikimedia.org/wikipedia/en/thumb/8/8db/Indian_Premier_League_Official_Logo.svg/1200px-Indian_Premier_League_Official_Logo.svg.png", width=200)

elif page == "Players":
    st.title("Player Analytics")
    st.write("Analyze individual player performances (Runs, SR, Economy).")

elif page == "Venues":
    st.title("Venue Analytics")
    st.write("Understand pitch conditions and toss advantages.")

elif page == "Match Analytics":
    st.title("Match Analytics")
    st.write("Deep dive into historical match margins, toss impacts, and close games.")

elif page == "Match Win Predictor":
    st.title("Live Match Win Predictor")
    st.markdown("Predict the probability of the **chasing team** winning the match in real-time.")
    
    with st.form("predictor_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            batting_team = st.selectbox("Batting Team (Chasing)", teams_list)
        with col2:
            bowling_team = st.selectbox("Bowling Team (Defending)", teams_list, index=1 if len(teams_list)>1 else 0)
        with col3:
            venue = st.selectbox("Venue", venues_list)
            
        col4, col5, col6, col7 = st.columns(4)
        with col4:
            target = st.number_input("Target Score", min_value=1, max_value=300, value=180)
        with col5:
            current_score = st.number_input("Current Score", min_value=0, max_value=300, value=75)
        with col6:
            overs_completed = st.number_input("Overs Completed", min_value=0, max_value=20, value=10)
        with col7:
            wickets_lost = st.number_input("Wickets Lost", min_value=0, max_value=10, value=2)
            
        submit = st.form_submit_button("Predict Probability")
        
    if submit:
        result = get_prediction(batting_team, bowling_team, venue, target, current_score, overs_completed, wickets_lost)
        if result:
            prob, df, crr, rrr, runs_rem, balls_rem = result
            
            st.markdown("---")
            st.subheader("Match State")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Runs Required", f"{runs_rem} from {balls_rem} balls")
            c2.metric("Current Run Rate (CRR)", f"{crr:.2f}")
            c3.metric("Required Run Rate (RRR)", f"{rrr:.2f}")
            c4.metric("Wickets in Hand", f"{10 - wickets_lost}")
            
            st.markdown("---")
            st.subheader("Win Probability")
            
            p1, p2 = st.columns(2)
            with p1:
                st.metric(f"{batting_team} (Batting)", f"{prob * 100:.1f}%")
                st.progress(float(prob))
            with p2:
                st.metric(f"{bowling_team} (Bowling)", f"{(1 - prob) * 100:.1f}%")
                st.progress(float(1 - prob))

elif page == "Model Explanation":
    st.title("Model Explanation (SHAP)")
    st.markdown("Understand the driving factors behind the XGBoost Win Predictor.")
    
    st.subheader("Global Feature Importance")
    st.write("This plot shows the overall impact of each feature on the model's predictions across all matches.")
    
    try:
        st.image("reports/figures/shap_summary.png", use_container_width=True)
    except Exception:
        st.warning("SHAP summary plot not found. Run the explainability script first.")
        
    st.subheader("Local Explanation Example")
    st.write("How the model decomposes an individual prediction:")
    try:
        st.image("reports/figures/shap_waterfall_individual.png", use_container_width=True)
    except Exception:
        st.warning("SHAP waterfall plot not found.")
