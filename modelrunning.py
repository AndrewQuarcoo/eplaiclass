#model
#modelrunning.py
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay, classification_report, precision_score
import matplotlib.pyplot as plt
import seaborn as sns
import re
import joblib
import os

# Read the historical data Excel file
try:
    epl_schedule = pd.read_excel('epl_historical_data_1980_2023.xlsx')
    print("Successfully loaded historical data")
    print(f"Initial number of rows: {len(epl_schedule)}")
except FileNotFoundError:
    print("Error: Could not find 'epl_historical_data_1980_2023.xlsx'. Please run historical_data.py first.")
    exit()

# Print column names and data types
print("\nColumns in the dataset:")
print(epl_schedule.dtypes)

# Function to split score safely
def split_score(score_str):
    if pd.isna(score_str):
        return pd.Series([None, None])
    try:
        # Handle different types of dashes and spaces
        score_str = str(score_str).strip()
        # Replace different types of dashes with a standard hyphen
        score_str = re.sub(r'[–—]', '-', score_str)
        scores = score_str.split('-')
        if len(scores) == 2:
            home_score = scores[0].strip()
            away_score = scores[1].strip()
            # Ensure both scores are numeric
            if home_score.isdigit() and away_score.isdigit():
                return pd.Series([int(home_score), int(away_score)])
        return pd.Series([None, None])
    except:
        return pd.Series([None, None])

# Split score into home_score and away_score
score_split = epl_schedule['score'].apply(split_score)
epl_schedule['home_score'] = score_split[0]
epl_schedule['away_score'] = score_split[1]

# Print sample of scores
print("\nSample of scores:")
print(epl_schedule[['score', 'home_score', 'away_score']].head())

# Drop rows with missing values
print("\nNumber of missing values in each column:")
print(epl_schedule[['home_score', 'away_score', 'winning_team', 'venue']].isnull().sum())

epl_clean = epl_schedule.dropna(subset=["home_score", "away_score", "winning_team", "venue"])
print(f"\nNumber of rows after cleaning: {len(epl_clean)}")

if len(epl_clean) == 0:
    print("Error: No valid rows after cleaning. Please check the data.")
    exit()

# Define result
def get_result(home_score, away_score):
    if home_score > away_score:
        return "Home"
    elif home_score < away_score:
        return "Away"
    else:
        return "Draw"

epl_clean["match_result"] = epl_clean.apply(lambda row: get_result(row["home_score"], row["away_score"]), axis=1)

# Encode venue
le_venue = LabelEncoder()
epl_clean["venue_encoded"] = le_venue.fit_transform(epl_clean["venue"])

# Define features
features = ["week", "time", "venue_encoded", "home_score", "away_score"]
X = epl_clean[features]
y = epl_clean["match_result"]

print("\nSample of features:")
print(X.head())

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
rf = RandomForestClassifier(n_estimators=100, min_samples_split=10, random_state=1)
rf.fit(X_train, y_train)
predictions = rf.predict(X_test)

# Accuracy
print("Accuracy:", accuracy_score(y_test, predictions))

# Precision Score
precision = precision_score(y_test, predictions, average='weighted')
print("\nWeighted Precision Score:", precision)

# Classification Report
print("\nClassification Report:")
print(classification_report(y_test, predictions))

# Confusion matrix
labels = ["Home", "Away", "Draw"]
cm = confusion_matrix(y_test, predictions, labels=labels)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
disp.plot(cmap=plt.cm.Blues)
plt.title("Confusion Matrix: Match Outcome Prediction")
plt.show()

# Pairplot visualization
plt.figure(figsize=(12, 8))
sns.pairplot(epl_clean[features + ["match_result"]], hue="match_result", palette="husl")
plt.suptitle("Feature Relationships by Match Result", y=1.02)
plt.tight_layout()
plt.show()

# Print feature importance
feature_importance = pd.DataFrame({
    'feature': features,
    'importance': rf.feature_importances_
}).sort_values('importance', ascending=False)
print("\nFeature Importance:")
print(feature_importance)

# After training the model, save it
joblib.dump(rf, 'epl_model.joblib')
joblib.dump(le_venue, 'venue_encoder.joblib')

def predict_match(home_team, away_team, week=20, time=1500):
    try:
        # Check if model files exist
        if not os.path.exists('epl_model.joblib') or not os.path.exists('venue_encoder.joblib'):
            print("Error: Model files not found. Please train the model first.")
            return None
            
        # Check if data file exists
        if not os.path.exists('epl_historical_data_1980_2023.xlsx'):
            print("Error: Historical data file not found. Please ensure 'epl_historical_data_1980_2023.xlsx' is in the same directory.")
            return None
        
        # Load the saved model and encoder
        try:
            model = joblib.load('epl_model.joblib')
            venue_encoder = joblib.load('venue_encoder.joblib')
        except Exception as e:
            print(f"Error loading model files: {str(e)}")
            return None
        
        # Load historical data
        try:
            epl_schedule = pd.read_excel('epl_historical_data_1980_2023.xlsx')
        except Exception as e:
            print(f"Error reading historical data: {str(e)}")
            return None
        
        # Verify team exists in data
        if home_team not in epl_schedule['home_team'].unique():
            print(f"Error: {home_team} not found in historical data")
            return None
        if away_team not in epl_schedule['away_team'].unique():
            print(f"Error: {away_team} not found in historical data")
            return None
            
        # Get the venue
        try:
            venue_data = epl_schedule[epl_schedule['home_team'] == home_team]
            if len(venue_data) == 0:
                print(f"Error: No venue found for {home_team}")
                return None
            venue = venue_data['venue'].iloc[0]
        except Exception as e:
            print(f"Error getting venue: {str(e)}")
            return None

        # Encode venue
        try:
            venue_encoded = venue_encoder.transform([venue])[0]
        except Exception as e:
            print(f"Error encoding venue: {str(e)}")
            return None
        
        # Get all historical matches for both teams
        home_team_matches = epl_schedule[epl_schedule['home_team'] == home_team]
        away_team_matches = epl_schedule[epl_schedule['away_team'] == away_team]
        
        # Calculate historical scoring averages
        avg_home_score = home_team_matches['home_score'].mean()
        avg_away_score = away_team_matches['away_score'].mean()
        
        # Get head-to-head history
        h2h_matches = epl_schedule[
            ((epl_schedule['home_team'] == home_team) & (epl_schedule['away_team'] == away_team)) |
            ((epl_schedule['home_team'] == away_team) & (epl_schedule['away_team'] == home_team))
        ]
        
        # Calculate head-to-head stats
        home_wins = len(h2h_matches[h2h_matches['winning_team'] == home_team])
        away_wins = len(h2h_matches[h2h_matches['winning_team'] == away_team])
        draws = len(h2h_matches[h2h_matches['winning_team'] == 'Draw'])
        
        # Calculate head-to-head scoring averages when teams met
        h2h_home_scores = h2h_matches[h2h_matches['home_team'] == home_team]['home_score'].mean()
        h2h_away_scores = h2h_matches[h2h_matches['away_team'] == away_team]['away_score'].mean()
        
        # Use head-to-head averages if available, otherwise use overall averages
        initial_home_score = h2h_home_scores if not pd.isna(h2h_home_scores) else avg_home_score
        initial_away_score = h2h_away_scores if not pd.isna(h2h_away_scores) else avg_away_score
        
        # Create feature array for prediction with historical averages
        X_pred = pd.DataFrame([[week, time, venue_encoded, initial_home_score, initial_away_score]], 
                            columns=["week", "time", "venue_encoded", "home_score", "away_score"])
        
        # Get model predictions
        try:
            predicted_result = model.predict(X_pred)[0]  # Get the predicted outcome
            probs = model.predict_proba(X_pred)[0]      # Get the probabilities
            
            # Map class labels
            classes = ["Home", "Away", "Draw"]
            
            # Create probability dictionary with team names
            prob_dict = {
                f"{home_team}_prob": float(probs[classes.index("Home")]),
                f"{away_team}_prob": float(probs[classes.index("Away")]),
                "draw_prob": float(probs[classes.index("Draw")])
            }
            
            # Map the predicted result to team names
            if predicted_result == "Home":
                predicted_result = home_team
            elif predicted_result == "Away":
                predicted_result = away_team
            
            # Determine final scores based on model probabilities and historical data
            highest_prob = max(prob_dict.values())
            if prob_dict[f"{home_team}_prob"] == highest_prob:
                # Home win prediction
                if pd.isna(h2h_home_scores):
                    # Use overall averages if no head-to-head history
                    home_score = round(max(2, avg_home_score))
                    away_score = round(max(0, avg_away_score - 1))
                else:
                    # Use head-to-head history
                    home_score = round(max(2, h2h_home_scores))
                    away_score = round(max(0, h2h_away_scores - 1))
            elif prob_dict[f"{away_team}_prob"] == highest_prob:
                # Away win prediction
                if pd.isna(h2h_away_scores):
                    # Use overall averages if no head-to-head history
                    home_score = round(max(0, avg_home_score - 1))
                    away_score = round(max(2, avg_away_score))
                else:
                    # Use head-to-head history
                    home_score = round(max(0, h2h_home_scores - 1))
                    away_score = round(max(2, h2h_away_scores))
            else:
                # Draw prediction
                if pd.isna(h2h_home_scores):
                    # Use overall averages if no head-to-head history
                    score = round((avg_home_score + avg_away_score) / 2)
                else:
                    # Use head-to-head history
                    score = round((h2h_home_scores + h2h_away_scores) / 2)
                home_score = away_score = score
                
        except Exception as e:
            print(f"Error making prediction: {str(e)}")
            return None
        
        return {
            "home_score": home_score,
            "away_score": away_score,
            "probabilities": prob_dict,
            "predicted_result": predicted_result,
            "stats": {
                "head_to_head": {
                    "home_wins": int(home_wins),
                    "away_wins": int(away_wins),
                    "draws": int(draws)
                },
                "expected_goals": {
                    "home_xg": float(initial_home_score),
                    "away_xg": float(initial_away_score)
                }
            }
        }
        
    except Exception as e:
        print(f"Unexpected error in prediction: {str(e)}")
        return None