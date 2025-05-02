#app.py
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import base64
import random
import os
from modelrunning import predict_match

# Set page configuration
st.set_page_config(
    page_title="EPL Game Prediction",
    page_icon="⚽",
    layout="wide"
)

# EPL Colors
EPL_PURPLE = "#3D195B"
EPL_WHITE = "#FFFFFF"
EPL_PINK = "#FF2882"
EPL_GREEN = "#00FF85"
EPL_BLACK = "#000000"
EPL_BLUE = "#8EBAE5"  # For progress bars

# Team logos dictionary mapping team names to logo URLs
team_logos = {
    "Arsenal": "https://resources.premierleague.com/premierleague/badges/t3.png",
    "Aston Villa": "https://resources.premierleague.com/premierleague/badges/t7.png",
    "Bournemouth": "https://resources.premierleague.com/premierleague/badges/t91.png",
    "Brentford": "https://resources.premierleague.com/premierleague/badges/t94.png",
    "Brighton": "https://resources.premierleague.com/premierleague/badges/t36.png",
    "Burnley": "https://resources.premierleague.com/premierleague/badges/t90.png",
    "Chelsea": "https://resources.premierleague.com/premierleague/badges/t8.png",
    "Crystal Palace": "https://resources.premierleague.com/premierleague/badges/t31.png",
    "Everton": "https://resources.premierleague.com/premierleague/badges/t11.png",
    "Fulham": "https://resources.premierleague.com/premierleague/badges/t54.png",
    "Leicester City": "https://resources.premierleague.com/premierleague/badges/t13.png",
    "Liverpool": "https://resources.premierleague.com/premierleague/badges/t14.png",
    "Manchester City": "https://resources.premierleague.com/premierleague/badges/t43.png",
    "Manchester United": "https://resources.premierleague.com/premierleague/badges/t1.png",
    "Newcastle United": "https://resources.premierleague.com/premierleague/badges/t4.png",
    "Nottingham Forest": "https://resources.premierleague.com/premierleague/badges/t17.png",
    "Sheffield United": "https://resources.premierleague.com/premierleague/badges/t49.png",
    "Tottenham Hotspur": "https://resources.premierleague.com/premierleague/badges/t6.png",
    "West Ham United": "https://resources.premierleague.com/premierleague/badges/t21.png",
    "Wolverhampton": "https://resources.premierleague.com/premierleague/badges/t39.png"
}

# CSS for styling
def get_custom_css():
    return f"""
    <style>
        .main {{
            background-color: {EPL_PURPLE};
            color: {EPL_WHITE};
        }}
        .stButton>button {{
            background-color: {EPL_PINK};
            color: {EPL_WHITE};
            font-weight: bold;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 4px;
        }}
        .stButton>button:hover {{
            background-color: {EPL_GREEN};
            color: {EPL_PURPLE};
        }}
        h1, h2, h3 {{
            color: {EPL_WHITE};
        }}
        .stSelectbox label, .stRadio label {{
            color: {EPL_WHITE};
        }}
        
        /* Selector background and text color */
        .stSelectbox div[data-baseweb="select"] div {{
            background-color: {EPL_BLACK};
            color: {EPL_WHITE};
            border: 1px solid {EPL_WHITE};
            border-radius: 4px;
        }}
        
        /* Dropdown options background and text color */
        div[data-baseweb="popover"] {{
            background-color: {EPL_BLACK} !important;
            color: {EPL_WHITE} !important;
        }}
        
        div[data-baseweb="popover"] ul li {{
            background-color: {EPL_BLACK} !important;
            color: {EPL_WHITE} !important;
        }}
        
        div[data-baseweb="popover"] ul li:hover {{
            background-color: {EPL_PURPLE} !important;
        }}
        
        .css-1d391kg {{
            background-color: {EPL_PURPLE};
        }}
        .st-bn {{
            background-color: {EPL_WHITE};
        }}
        .st-cd {{
            background-color: {EPL_WHITE};
        }}
        .css-1544g2n.e1fqkh3o4 {{
            padding-top: 2rem;
        }}
        .team-vs-container {{
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 1rem 0;
        }}
        .vs-text {{
            font-size: 32px;
            font-weight: bold;
            color: {EPL_WHITE};
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100%;
        }}
        .output-section {{
            background-color: rgba(255, 255, 255, 0.1);
            padding: 2rem;
            border-radius: 8px;
            margin-top: 2rem;
        }}
        .title-container {{
            text-align: center;
            margin-bottom: 1rem;
        }}
        .logo-container {{
            display: flex;
            justify-content: center;
            margin-bottom: 2rem;
        }}
        .team-logo {{
            width: 40px;
            height: 40px;
            margin-right: 10px;
            vertical-align: middle;
        }}
        .team-container {{
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }}
        .prediction-container {{
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 20px 0;
        }}
        .prediction-team {{
            display: flex;
            align-items: center;
            margin: 0 15px;
        }}
        .prediction-score {{
            font-size: 32px;
            font-weight: bold;
            margin: 0 10px;
        }}
        .team-with-logo {{
            display: flex;
            align-items: center;
        }}
        .team-name {{
            margin-left: 10px;
        }}
        .win-probability-container {{
            margin-top: 1.5rem;
        }}
        .win-probability-header {{
            text-align: center;
            margin-bottom: 1rem;
            font-size: 20px;
            color: {EPL_WHITE};
            font-weight: bold;
            text-transform: uppercase;
        }}
        .win-probability-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 5px;
        }}
        .win-probability-team {{
            flex-basis: 33%;
            text-align: left;
            font-weight: bold;
            color: {EPL_WHITE};
            font-size: 18px;
        }}
        .win-probability-draw {{
            flex-basis: 33%;
            text-align: center;
            font-weight: bold;
            color: {EPL_WHITE};
            font-size: 18px;
        }}
        .win-probability-value {{
            color: {EPL_BLUE};
            font-weight: bold;
            font-size: 18px;
        }}
        .stProgress > div > div > div > div {{
            background-color: {EPL_BLUE};
        }}
    </style>
    """

# Apply custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Title and Logo
st.markdown("""
    <div class="title-container">
        <h1>EPL Game Prediction</h1>
    </div>
    <div class="logo-container">
        <img src="https://upload.wikimedia.org/wikipedia/en/f/f2/Premier_League_Logo.svg" 
        style="width: 200px; height: auto; filter: invert(1);">
    </div>
""", unsafe_allow_html=True)

# EPL Teams
epl_teams = [
    "Arsenal", "Aston Villa", "Bournemouth", "Brentford", "Brighton", 
    "Burnley", "Chelsea", "Crystal Palace", "Everton", "Fulham", 
    "Leicester City", "Liverpool", "Manchester City", "Manchester United", 
    "Newcastle United", "Nottingham Forest", "Sheffield United", 
    "Tottenham Hotspur", "West Ham United", "Wolverhampton"
]

# Create columns for the team selectors with VS in the middle
col1, col2, col3 = st.columns([2, 1, 2])

# Team selectors
with col1:
    st.markdown("### Home Team")
    home_team = st.selectbox("", epl_teams, index=0, label_visibility="collapsed")
    st.markdown(f"""
    <div class="team-with-logo">
        <img src="{team_logos[home_team]}" class="team-logo">
        <span class="team-name">{home_team}</span>
    </div>
    """, unsafe_allow_html=True)

# Centered VS text
with col2:
    # Use a container with centered content and vertical alignment
    st.markdown('<div class="vs-text">VS</div>', unsafe_allow_html=True)

with col3:
    st.markdown("### Away Team")
    away_team = st.selectbox(" ", epl_teams, index=12, label_visibility="collapsed")  # Default to Man City as away team
    st.markdown(f"""
    <div class="team-with-logo">
        <img src="{team_logos[away_team]}" class="team-logo">
        <span class="team-name">{away_team}</span>
    </div>
    """, unsafe_allow_html=True)

# Analysis type selector
analysis_type = st.radio(
    "Select Analysis Type",
    ["Only match prediction", "Matches, players and other variables"],
    horizontal=True
)

# Run analysis button
if st.button("Run Analysis"):
    st.markdown("<div class='output-section'>", unsafe_allow_html=True)
    
    # Check for required files
    if not os.path.exists('epl_model.joblib'):
        st.error("Error: Model file (epl_model.joblib) not found. Please train the model first.")
    elif not os.path.exists('venue_encoder.joblib'):
        st.error("Error: Venue encoder file (venue_encoder.joblib) not found. Please train the model first.")
    elif not os.path.exists('epl_historical_data_1980_2023.xlsx'):
        st.error("Error: Historical data file (epl_historical_data_1980_2023.xlsx) not found. Please ensure the file is in the same directory.")
    else:
        st.subheader(f"Prediction: {home_team} vs {away_team}")
        
        # Get prediction from the model
        with st.spinner('Making prediction...'):
            prediction = predict_match(home_team, away_team)
        
        if prediction:
            home_score = prediction["home_score"]
            away_score = prediction["away_score"]
            probabilities = prediction["probabilities"]
            predicted_result = prediction["predicted_result"]
            
            # Display the prediction results with team logos
            st.markdown("### Model Prediction")
            st.markdown(f"""
            <div style="text-align: center; margin-bottom: 20px;">
                <span style="font-size: 20px; color: {EPL_GREEN};">Predicted Result: {predicted_result}</span>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="prediction-container">
                <div class="prediction-team">
                    <img src="{team_logos[home_team]}" class="team-logo">
                    <span>{home_team}</span>
                </div>
                <div class="prediction-score">{home_score} - {away_score}</div>
                <div class="prediction-team">
                    <img src="{team_logos[away_team]}" class="team-logo">
                    <span>{away_team}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Win probability from model
            st.markdown("""
            <div class="win-probability-header">
                MODEL CONFIDENCE
            </div>
            """, unsafe_allow_html=True)
            
            # Display team names and percentages above the progress bars
            st.markdown(f"""
            <div class="win-probability-row">
                <div class="win-probability-team">
                    {home_team}<br>
                    <span class="win-probability-value">{int(probabilities[f"{home_team}_prob"] * 100)}%</span>
                </div>
                <div class="win-probability-draw">
                    Draw<br>
                    <span class="win-probability-value">{int(probabilities['draw_prob'] * 100)}%</span>
                </div>
                <div class="win-probability-team" style="text-align: right;">
                    {away_team}<br>
                    <span class="win-probability-value">{int(probabilities[f"{away_team}_prob"] * 100)}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Create a single row of progress bars
            col1, col2, col3 = st.columns(3)
            with col1:
                st.progress(probabilities[f"{home_team}_prob"])
            with col2:
                st.progress(probabilities['draw_prob'])
            with col3:
                st.progress(probabilities[f"{away_team}_prob"])
            
            # Display Expected Goals
            st.markdown("### Expected Goals (xG)")
            xg_cols = st.columns(2)
            with xg_cols[0]:
                st.metric(
                    f"{home_team} xG", 
                    f"{prediction['stats']['expected_goals']['home_xg']:.2f}"
                )
            with xg_cols[1]:
                st.metric(
                    f"{away_team} xG", 
                    f"{prediction['stats']['expected_goals']['away_xg']:.2f}"
                )
            
            # Head-to-head history
            h2h = prediction['stats']['head_to_head']
            st.markdown("### Historical Head-to-Head")
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; margin: 20px 0;">
                <div style="text-align: center;">
                    <img src="{team_logos[home_team]}" style="width: 60px; height: 60px;"><br>
                    <span>{home_team}</span><br>
                    <span style="font-size: 24px; font-weight: bold;">{h2h['home_wins']}</span>
                </div>
                <div style="text-align: center;">
                    <span style="font-size: 18px; font-weight: bold;">WINS</span>
                </div>
                <div style="text-align: center;">
                    <img src="{team_logos[away_team]}" style="width: 60px; height: 60px;"><br>
                    <span>{away_team}</span><br>
                    <span style="font-size: 24px; font-weight: bold;">{h2h['away_wins']}</span>
                </div>
            </div>
            <div style="text-align: center; margin: 10px 0;">
                <span style="font-size: 18px; font-weight: bold;">DRAWS: {h2h['draws']}</span>
            </div>
            """, unsafe_allow_html=True)
            
        else:
            st.error("Error making prediction. Check the console for detailed error messages.")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 3rem; font-size: 0.8rem;">
    ©️ 2025 EPL Game Prediction | Created with Streamlit | Data from EPL
</div>
""", unsafe_allow_html=True)