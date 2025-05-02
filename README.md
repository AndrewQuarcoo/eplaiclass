# EPL Match Prediction App 🏆⚽

A machine learning application that predicts English Premier League (EPL) match outcomes using historical data from 1980-2023. The app provides win probabilities and predicted scores for matches between any two EPL teams.

## Features 🌟

- **Match Outcome Prediction**: Predicts the result (Home win, Away win, or Draw) for any EPL match
- **Score Prediction**: Estimates the likely scoreline based on historical performance
- **Win Probabilities**: Calculates probability percentages for each possible match outcome
- **Interactive UI**: User-friendly Streamlit interface with team logos and EPL styling
- **Historical Data**: Uses over 40 years of EPL match data for accurate predictions
- **Real-time Updates**: Predictions are generated instantly when teams are selected

## Technology Stack 💻

- **Python 3.12**
- **Streamlit**: Web application framework
- **Scikit-learn**: Machine learning library for prediction model
- **Pandas**: Data manipulation and analysis
- **Joblib**: Model persistence
- **NumPy**: Numerical computations
- **PIL**: Image processing

## Installation 🛠️

1. Clone the repository:
   ```bash
   git clone https://github.com/AndrewQuarcoo/eplaiclass.git
   cd eplaiclass
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage 🎮

1. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Open your web browser and navigate to the provided local URL (typically http://localhost:8501)

3. Select the home and away teams from the dropdown menus

4. Click the "Predict Match" button to see the prediction results

## Model Details 📊

The prediction model uses a Random Forest Classifier trained on the following features:
- Match week
- Kick-off time
- Venue
- Historical scoring patterns
- Head-to-head records

Model performance metrics:
- Accuracy: 99.7%
- Weighted Precision Score: 99.7%

## Project Structure 📁

```
eplaiclass/
├── app.py                 # Streamlit web application
├── modelrunning.py        # Model training and prediction logic
├── run.py                 # Script to run the application
├── requirements.txt       # Python dependencies
├── epl_model.joblib      # Trained model file
├── venue_encoder.joblib   # Venue encoding file
└── epl_historical_data_1980_2023.xlsx  # Historical match data
```

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📝

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments 🙏

- Premier League for team logos and branding
- Historical data contributors
- Open-source community for libraries and tools


##
```bash 
python3 -m streamlit run app.py
```

or

```bash 
source venv/bin/activate && streamlit run app.py

```


```bash
python3 modelrunning.py
```
