import pandas as pd
import joblib
import os
from pathlib import Path

class FraudMLService:
    def __init__(self):
        # Robust path setup with smart search
        def find_path(rel_path):
            curr = Path(__file__).resolve()
            anchors = [
                curr.parent,
                Path.cwd(),
                curr.parents[2],
                curr.parents[1]
            ]
            for anchor in anchors:
                target = (anchor / rel_path).resolve()
                if target.exists():
                    return target
                target = (anchor / "Task-1-Fraud_Detection" / rel_path).resolve()
                if target.exists():
                    return target
            return curr.parents[2] / rel_path

        model_path = find_path("models/fraud_model.pkl")
        model_dir = model_path.parent
        
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
