
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy import create_engine
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import os

def get_data_from_database():
    print("Fetching data from the database...")

    # Connecting to database using SQLAlchemy for better compatibility
    engine = create_engine("mysql+mysqlconnector://Admin:newpassword123@localhost/cfms")
    query = "SELECT timestamp, cashew_type, `change` FROM stock_changes"

    # Fetch data into a DataFrame
    df = pd.read_sql(query, engine)

    print(f"Data fetched successfully. Number of records: {len(df)}")
    return df

def preprocess_data(df):
    print("Preprocessing data...")

    df['change'] = df['change'].astype(str)

    # Convert 'change' column to numeric values
    def clean_change_column(value):
        try:
            # Remove unwanted characters and safely evaluate expression
            cleaned_value = eval(value.replace('->', '+').replace('-', '+').replace(' ', ''))
            return float(cleaned_value)
        except:
            return np.nan  # Return NaN if conversion fails

    df['change'] = df['change'].apply(clean_change_column)

    # Remove rows where 'change' is NaN
    num_nans = df['change'].isna().sum()
    print(f"Number of NaN values in 'change' column before removal: {num_nans}")
    df = df.dropna(subset=['change'])

    # Extract 'year' and 'month' from timestamp
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['year'] = df['timestamp'].dt.year
    df['month'] = df['timestamp'].dt.month

    print(f"Data preprocessed successfully. Remaining records: {len(df)}")
    return df

def train_model(df):
    print("Training model and predicting demand...")

    # Checking if the dataset is empty after preprocessing
    if df.empty:
        print("No predictions were made due to insufficient data.")
        return {}

    predictions = {}
    cashew_types = df['cashew_type'].unique()

    # Training a separate model for each month
    for month in range(1, 13):  # Iterate through all 12 months
        print(f"\nTraining model for month {month}...")

        # Filter data for the current month
        month_data = df[df['month'] == month]

        if month_data.empty:
            print(f"No data available for month {month}. Skipping...")
            continue

        # Train a model for each cashew type
        for cashew in cashew_types:
            cashew_data = month_data[month_data['cashew_type'] == cashew]

            if len(cashew_data) < 2:  # Require at least 2 records for training
                print(f"Skipping cashew type {cashew} for month {month} due to insufficient data (less than 2 records).")
                continue

            # Define features (X) and target variable (y)
            X = cashew_data[['year']]
            y = cashew_data['change']

            # Train model
            model = LinearRegression()
            model.fit(X, y)

            # Predict demand for the next year (e.g., 2025)
            future_year = 2025
            future_demand = model.predict([[future_year]])

            # Store the prediction
            if cashew not in predictions:
                predictions[cashew] = {}
            predictions[cashew][month] = future_demand[0]

    if predictions:
        print(f"\nPredictions: {predictions}")
    else:
        print("No predictions were made due to insufficient data.")

    return predictions

def plot_demand(predictions):
    print("Plotting demand prediction...")

    if not predictions:
        print("No predictions to display!")
        return

    # Prepare data for plotting
    cashew_types = list(predictions.keys())
    months = list(range(1, 13))  # All 12 months
    demands = {cashew: [predictions[cashew].get(month, 0) for month in months] for cashew in cashew_types}

    # Sort cashew types based on their maximum predicted demand
    cashew_types_sorted = sorted(cashew_types, key=lambda x: max(demands[x]), reverse=True)

    # Plot the predictions
    plt.figure(figsize=(6, 4))  # Reducing the figure size further
    for cashew in cashew_types_sorted:
        plt.plot(months, demands[cashew], label=cashew)

    plt.xlabel('Month')
    plt.ylabel('Predicted Demand')
    plt.title('Predicted Demand for Cashews (2025)')
    plt.xticks(months)
    plt.legend()
    plt.grid(True)

    # Saving the plot as an image file
    output_file_path = os.path.join(os.path.dirname(__file__), "demand_prediction_output.png")
    plt.savefig(output_file_path, dpi=80, bbox_inches='tight')  # Reducing DPI and adjust bounding box
    plt.close()  # Close the plot to free up memory

    print(f"Plot saved to {output_file_path}")

def show_demand_prediction():
    df = get_data_from_database()

    # Displaying data distribution
    print("Checking data distribution for each cashew type...")
    print(df['cashew_type'].value_counts())

    # Preprocessing data
    df = preprocess_data(df)

    # Training the model and get predictions
    predictions = train_model(df)

    # Plotting the predictions
    plot_demand(predictions)

    print("Demand prediction process completed.")

# Run the demand prediction
show_demand_prediction()