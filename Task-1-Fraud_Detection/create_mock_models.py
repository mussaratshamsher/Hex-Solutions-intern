import joblib
import os
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
import numpy as np

# Create directory
model_dir = 'Task-1-Fraud_Detection/models'
os.makedirs(model_dir, exist_ok=True)

# 1. Create Mock Encoders
le_city = LabelEncoder()
le_city.fit(['Karachi', 'Lahore', 'Islamabad'])
joblib.dump(le_city, os.path.join(model_dir, 'le_city.pkl'))

le_device = LabelEncoder()
le_device.fit(['dev_123', 'dev_456', 'dev_789'])
joblib.dump(le_device, os.path.join(model_dir, 'le_device.pkl'))

# 2. Create Mock Model (LogisticRegression supports predict_proba)
# We need a dummy model that has the right interface for the ml_service
model = LogisticRegression()
# Dummy data to fit the model interface
X = np.array([[100, 0, 10, 0, 30, 1, 0, 0]]) # Matches feature count
y = np.array([0])
model.fit(X, y)

joblib.dump(model, os.path.join(model_dir, 'fraud_model.pkl'))

print(f"Mock model and encoders created in {model_dir}")
