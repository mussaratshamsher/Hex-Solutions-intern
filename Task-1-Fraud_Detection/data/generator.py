import pandas as pd
import numpy as np
import uuid
import random
from datetime import datetime, timedelta

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_synthetic_data(num_records=30000):
    cities = ['Karachi', 'Lahore', 'Faisalabad', 'Rawalpindi', 'Gujranwala', 
              'Peshawar', 'Multan', 'Saidu Sharif', 'Hyderabad', 'Islamabad', 
              'Quetta', 'Bahawalpur', 'Sargodha', 'Sialkot', 'Sukkur', 
              'Larkana', 'Sheikhupura', 'Rahim Yar Khan', 'Jhang', 'Dera Ghazi Khan']
    
    data = []
    
    for i in range(num_records):
        # Basic fields
        transaction_id = str(uuid.uuid4())
        sender_id = f"03{random.randint(0, 4)}{random.randint(1000000, 9999999)}"
        receiver_id = f"03{random.randint(0, 4)}{random.randint(1000000, 9999999)}"
        amount = round(random.uniform(10, 50000), 2)
        city = random.choice(cities)
        
        # Time distribution (more during day, less at night)
        hour = np.random.choice(range(24), p=[0.02, 0.01, 0.01, 0.01, 0.01, 0.02, 
                                             0.03, 0.05, 0.07, 0.08, 0.08, 0.08, 
                                             0.08, 0.07, 0.07, 0.06, 0.05, 0.04, 
                                             0.04, 0.03, 0.03, 0.02, 0.02, 0.02])
        minute = random.randint(0, 59)
        transaction_time = f"{hour:02d}:{minute:02d}"
        
        device_id = f"dev_{random.randint(1000, 9999)}"
        account_age_days = random.randint(1, 1000)
        transactions_today = random.randint(0, 5)
        failed_login_attempts = random.randint(0, 1)
        new_recipient = random.choice([True, False])
        
        fraud_label = 0 # Default to Legit
        
        # Inject Fraud Patterns
        
        # 1. Velocity Attack
        if transactions_today > 4 and random.random() < 0.3:
            fraud_label = 1
            
        # 2. Night-Owl Fraud
        if 2 <= hour <= 5 and amount > 20000 and random.random() < 0.4:
            fraud_label = 1
            
        # 3. New Recipient Spike
        if new_recipient and amount > 40000 and account_age_days > 365 and random.random() < 0.5:
            fraud_label = 1
            
        # 4. Device Switching + Failed Logins
        if failed_login_attempts > 0 and random.random() < 0.6:
            # Often associated with fraudulent login attempts
            if random.random() < 0.4:
                fraud_label = 1

        data.append({
            'transaction_id': transaction_id,
            'sender_id': sender_id,
            'receiver_id': receiver_id,
            'amount': amount,
            'city': city,
            'transaction_time': transaction_time,
            'hour': hour, # Helper for ML
            'device_id': device_id,
            'account_age_days': account_age_days,
            'transactions_today': transactions_today,
            'failed_login_attempts': failed_login_attempts,
            'new_recipient': int(new_recipient),
            'fraud_label': fraud_label
        })
    
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    print("Generating synthetic data...")
    df = generate_synthetic_data(30000)
    output_path = "data/transactions.csv"
    df.to_csv(output_path, index=False)
    print(f"Data saved to {output_path}")
    print(f"Fraud distribution:\n{df['fraud_label'].value_counts(normalize=True)}")
