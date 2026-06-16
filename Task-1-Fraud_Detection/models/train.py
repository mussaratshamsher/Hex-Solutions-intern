import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, f1_score
import joblib
import os

# Load Data
data_path = 'data/transactions.csv'
if not os.path.exists(data_path):
    print(f"File not found: {data_path}")
    exit(1)

df = pd.read_csv(data_path)

# Feature Engineering
le_city = LabelEncoder()
le_device = LabelEncoder()
df['city'] = le_city.fit_transform(df['city'])
df['device_id'] = le_device.fit_transform(df['device_id'])

# Drop columns not needed for training
X = df.drop(['transaction_id', 'sender_id', 'receiver_id', 'transaction_time', 'fraud_label'], axis=1)
y = df['fraud_label']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Handle Class Imbalance
# Calculate scale_pos_weight: count(negative) / count(positive)
scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()

# Train Model
model = xgb.XGBClassifier(
    objective='binary:logistic',
    scale_pos_weight=scale_pos_weight,
    n_estimators=100,
    learning_rate=0.1,
    max_depth=5,
    random_state=42
)

print("Training XGBoost model...")
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save Model and Encoders
model_dir = 'models'
os.makedirs(model_dir, exist_ok=True)
joblib.dump(model, os.path.join(model_dir, 'fraud_model.pkl'))
joblib.dump(le_city, os.path.join(model_dir, 'le_city.pkl'))
joblib.dump(le_device, os.path.join(model_dir, 'le_device.pkl'))
print(f"Model and encoders saved to {model_dir}")
