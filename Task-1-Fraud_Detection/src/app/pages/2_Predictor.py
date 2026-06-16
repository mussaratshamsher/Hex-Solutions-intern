import streamlit as st
import sys
import os

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from services.ml_service import FraudMLService
from services.groq_client import GroqFraudInvestigator

st.title("Transaction Predictor")

# Inputs
amount = st.number_input("Amount (PKR)", min_value=10, max_value=500000)
hour = st.slider("Hour of Day", 0, 23)
account_age_days = st.number_input("Account Age (Days)", min_value=0)
transactions_today = st.number_input("Transactions Today", min_value=0)
failed_login_attempts = st.number_input("Failed Login Attempts", min_value=0)
new_recipient = st.selectbox("New Recipient", [False, True])
city = st.text_input("City", "Karachi")
device_id = st.text_input("Device ID", "dev_1234")

if st.button("Run Fraud Check"):
    data = {
        'amount': amount,
        'hour': hour,
        'account_age_days': account_age_days,
        'transactions_today': transactions_today,
        'failed_login_attempts': failed_login_attempts,
        'new_recipient': int(new_recipient),
        'city': city,
        'device_id': device_id
    }
    
    ml_service = FraudMLService()
    result = ml_service.predict(data)
    
    if "error" in result:
        st.error(result["error"])
    else:
        st.write(f"Fraud Probability: {result['fraud_probability']:.2%}")
        if result['is_fraud']:
            st.warning("Transaction Flagged as FRAUD")
            
            # AI Investigation
            st.markdown("### AI Investigation Report")
            with st.spinner("Generating AI report..."):
                investigator = GroqFraudInvestigator()
                report = investigator.analyze(data, result)
                st.markdown(report)
        else:
            st.success("Transaction Approved")
