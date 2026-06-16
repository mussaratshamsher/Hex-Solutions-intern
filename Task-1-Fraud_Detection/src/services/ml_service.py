import pandas as pd
import joblib
import sys
from pathlib import Path

# Fix import path for utils
SRC_DIR = Path(__file__).parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))
from utils.file_locator import find_file

class FraudMLService:
    def __init__(self):
        # Find model files using utility
        self.model = joblib.load(find_file('fraud_model.pkl'))
        self.le_city = joblib.load(find_file('le_city.pkl'))
        self.le_device = joblib.load(find_file('le_device.pkl'))

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
