import pandas as pd
import joblib
import os
from pathlib import Path

class FraudMLService:
    def __init__(self):
        # Robust path setup relative to this file
        current_file = Path(__file__).resolve()
        # Find Task-1-Fraud_Detection/
        def find_root():
            for parent in current_file.parents:
                if parent.name == "Task-1-Fraud_Detection":
                    return parent
                if (parent / "Task-1-Fraud_Detection").exists():
                    return parent / "Task-1-Fraud_Detection"
            return current_file.parents[2]
        
        BASE_DIR = find_root()
        model_dir = BASE_DIR / "models"
        
        self.model = joblib.load(model_dir / 'fraud_model.pkl')
        self.le_city = joblib.load(model_dir / 'le_city.pkl')
        self.le_device = joblib.load(model_dir / 'le_device.pkl')

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
