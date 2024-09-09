from flask import Flask, jsonify
import joblib
import pandas as pd
from flask_cors import CORS
import logging
import os
import numpy as np

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)

# Verify that all necessary files exist
if not os.path.exists('random_forest_model.pkl'):
    logging.error("File 'random_forest_model.pkl' not found.")
if not os.path.exists('random_service_dataset.csv'):
    logging.error("File 'random_service_dataset.csv' not found.")
if not os.path.exists('model_features.pkl'):
    logging.error("File 'model_features.pkl' not found.")

# Load the trained Random Forest model
try:
    rf_model = joblib.load('random_forest_model.pkl')
    logging.debug("Random Forest model loaded successfully.")
except Exception as e:
    logging.error(f"Error loading model: {str(e)}")
    rf_model = None

# Load the dataset
try:
    df = pd.read_csv('random_service_dataset.csv')
    logging.debug("Dataset loaded successfully.")
except Exception as e:
    logging.error(f"Error loading dataset: {str(e)}")
    df = None

df_encoded = None  # Initialize df_encoded globally

# Check if both model and dataset are loaded successfully
if rf_model and df is not None:
    # Feature engineering
    df['price_per_review'] = df['Base Price'] / (df['Total Reviews'] + 1)
    df['price_star_ratio'] = df['Base Price'] / (df['Average Stars'] + 1)
    df['availability_numeric'] = df['Availability'].astype(int)

    # One-hot encode categorical variables to match the trained model
    df_encoded = pd.get_dummies(df, columns=['Title', 'Description', 'Owner'])

    # Load the list of model features used during training
    try:
        model_features = joblib.load('model_features.pkl')  # Ensure this contains the exact feature list
        logging.debug("Model features loaded successfully.")
    except Exception as e:
        logging.error(f"Error loading model features: {str(e)}")
        model_features = None

    if model_features is not None and not model_features.empty:
        # Reorder columns to match the model's features
        df_encoded = df_encoded.reindex(columns=model_features, fill_value=0)

        # Remove any columns that shouldn't be present (such as ID and Plus Achetés)
        df_encoded = df_encoded.drop(columns=['ID', 'Plus Achetés'], errors='ignore')
    else:
        logging.error("Model features are not properly loaded or empty.")
else:
    logging.error("Model or dataset not properly loaded. Aborting further processing.")

def convert_types(data):
    if isinstance(data, (pd.Series, pd.DataFrame)):
        data = data.applymap(lambda x: x.item() if hasattr(x, 'item') else x)
    elif isinstance(data, dict):
        for key in data:
            value = data[key]
            if isinstance(value, (pd.Series, pd.DataFrame)):
                data[key] = value.applymap(lambda x: x.item() if hasattr(x, 'item') else x)
            elif isinstance(value, (np.bool_, np.int64, np.float64)):
                # Convert numpy types to native Python types
                data[key] = value.item()
            elif hasattr(value, 'item'):
                data[key] = value.item()
    return data

@app.route('/')
def home():
    return "Welcome to the Service Purchase Prediction API"

@app.route('/most_purchased_services', methods=['GET'])
def most_purchased_services():
    global df_encoded  # Ensure we are using the global df_encoded

    try:
        # Ensure the model and data are loaded
        if not rf_model or df is None or df_encoded is None:
            raise ValueError("Model or data not properly loaded.")

        # Log the shape of the encoded DataFrame
        logging.debug(f"DataFrame encoded shape: {df_encoded.shape}")

        # Make sure to remove the 'Predicted_Purchases' column if it exists
        if 'Predicted_Purchases' in df_encoded.columns:
            df_encoded = df_encoded.drop(columns=['Predicted_Purchases'])

        # Predict purchases for each service using the Random Forest model
        predictions = rf_model.predict(df_encoded)
        logging.debug("Prediction successful.")

        # Add the predictions to the DataFrame
        df_encoded['Predicted_Purchases'] = predictions

        # Find the top 5 services with the highest predicted purchases
        top_5_idx = df_encoded['Predicted_Purchases'].nlargest(5).index
        logging.debug(f"Top 5 predicted indices: {top_5_idx}")

        top_5_services = df.iloc[top_5_idx]
        logging.debug(f"Top 5 purchased services data: {top_5_services.to_dict(orient='records')}")

        # Extract key characteristics of the top 5 services
        services_info = []
        for index in top_5_idx:
            service = top_5_services.loc[index]
            service_info = {
                'Service ID': int(service['ID']),
                'Title': service['Title'],
                'Description': service['Description'],
                'Base Price': float(service['Base Price']),
                'Total Reviews': int(service['Total Reviews']),
                'Average Stars': float(service['Average Stars']),
                'Availability': service['Availability'],
                'Predicted Purchases': float(df_encoded.loc[index, 'Predicted_Purchases'])
            }
            # Convert types to ensure JSON serialization
            service_info = convert_types(service_info)
            services_info.append(service_info)

        # Return the top 5 service details as a JSON response
        return jsonify(services_info)
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}", exc_info=True)  # Log the error
        # Handle exceptions and return a meaningful error message
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
