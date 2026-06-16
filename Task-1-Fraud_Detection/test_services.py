import sys
import os
# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from services.ml_service import FraudMLService
from services.groq_client import GroqFraudInvestigator

# Test data
test_data = {
    'amount': 45000.0,
    'hour': 3,
    'account_age_days': 500,
    'transactions_today': 5,
    'failed_login_attempts': 1,
    'new_recipient': 1,
    'city': 'Karachi',
    'device_id': 'dev_1234'
}

print("--- Testing ML Service ---")
ml = FraudMLService()
result = ml.predict(test_data)
print(f"Prediction result: {result}")

if result.get('is_fraud'):
    print("\n--- Testing Groq Client (AI Investigator) ---")
    investigator = GroqFraudInvestigator()
    report = investigator.analyze(test_data, result)
    print(f"AI Report:\n{report}")
else:
    print("\nTransaction not flagged as fraud, skipping AI investigation.")
