import pandas as pd
import joblib
import sys
from pathlib import Path
from utils.file_locator import find_file

class FraudMLService:
    def __init__(self):
        # Find model files using utility
        self.model_path = find_file('fraud_model.pkl')
        self.le_city_path = find_file('le_city.pkl')
        self.le_device_path = find_file('le_device.pkl')
        
        if not self.model_path or not self.le_city_path or not self.le_device_path:
            raise FileNotFoundError("One or more model/encoder files could not be located.")

        self.model = joblib.load(self.model_path)
        self.le_city = joblib.load(self.le_city_path)
        self.le_device = joblib.load(self.le_device_path)

    def predict(self, input_data):
        # input_data is a dict with:
        # amount, hour, account_age_days, transactions_today, failed_login_attempts, new_recipient, city, device_id
        
        # Preprocess input
        df = pd.DataFrame([input_data])
        
        # Reorder columns to match training data
        df = df[['amount', 'city', 'hour', 'device_id', 'account_age_days', 'transactions_today', 'failed_login_attempts', 'new_recipient']]
        
        # Encode
        try:
            df['city'] = self.le_city.transform(df['city'])
            df['device_id'] = self.le_device.transform(df['device_id'])
        except ValueError as e:
            # Handle unknown labels (for prototype, just default to 0 or raise)
            return {"error": f"Encoding error: {str(e)}"}
            
        # Predict
        probability = self.model.predict_proba(df)[0][1]
        
        return {
            "fraud_probability": float(probability),
            "is_fraud": bool(probability > 0.5)
        }
