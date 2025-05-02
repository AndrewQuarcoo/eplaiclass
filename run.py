import os
import subprocess
import threading
import time
import sys

def check_dependencies():
    """Check and install required dependencies."""
    try:
        import pandas as pd
        import streamlit as st
        import sklearn
        import joblib
        print("✅ All required packages are installed")
    except ImportError as e:
        print(f"Installing missing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def train_model():
    """Train the model if necessary."""
    if not os.path.exists('epl_model.joblib') or not os.path.exists('venue_encoder.joblib'):
        print("Training model...")
        import modelrunning
        print("✅ Model training complete")
    else:
        print("✅ Model files found")

def check_data():
    """Check if historical data exists."""
    if not os.path.exists('epl_historical_data_1980_2023.xlsx'):
        print("❌ Error: Historical data file (epl_historical_data_1980_2023.xlsx) not found")
        print("Please ensure the file is in the same directory")
        return False
    print("✅ Historical data found")
    return True

def run_streamlit():
    """Run the Streamlit app."""
    print("Starting Streamlit app...")
    subprocess.run(["streamlit", "run", "app.py"])

def main():
    print("🚀 Starting EPL Prediction System")
    print("\n1. Checking dependencies...")
    check_dependencies()
    
    print("\n2. Checking data...")
    if not check_data():
        return
    
    print("\n3. Checking model...")
    train_model()
    
    print("\n4. Starting application...")
    # Run the Streamlit app
    run_streamlit()

if __name__ == "__main__":
    main() 