import pandas as pd
import numpy as np
import os

# Create data directory
data_dir = 'Task-1-Fraud_Detection/data'
os.makedirs(data_dir, exist_ok=True)

# Generate 100 rows of mock data
np.random.seed(42)
n = 100
data = {
    'transaction_id': [f't_{i}' for i in range(n)],
    'sender_id': [f's_{i}' for i in range(n)],
    'receiver_id': [f'r_{i}' for i in range(n)],
    'transaction_time': pd.date_range(start='2026-01-01', periods=n, freq='h'),
    'amount': np.random.uniform(10, 50000, n),
    'city': np.random.choice(['Karachi', 'Lahore', 'Islamabad'], n),
    'hour': np.random.randint(0, 24, n),
    'device_id': np.random.choice(['dev_123', 'dev_456', 'dev_789'], n),
    'account_age_days': np.random.randint(1, 1000, n),
    'transactions_today': np.random.randint(0, 10, n),
    'failed_login_attempts': np.random.randint(0, 5, n),
    'new_recipient': np.random.choice([0, 1], n),
    'fraud_label': np.random.choice([0, 1], n, p=[0.9, 0.1]) # 10% fraud rate
}

df = pd.DataFrame(data)
df.to_csv(os.path.join(data_dir, 'transactions.csv'), index=False)
print(f"Mock transactions saved to {os.path.join(data_dir, 'transactions.csv')}")
