import streamlit as st
import sys
import os
from pathlib import Path

# Path setup for imports
BASE_DIR = Path(__file__).parents[3]
SRC_DIR = BASE_DIR / "Task-1-Fraud_Detection" / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

from services.ml_service import FraudMLService
from services.groq_client import GroqFraudInvestigator

st.set_page_config(page_title="Fraud Predictor", layout="wide")
st.title("🔍 Transaction Fraud Predictor")
st.markdown("Enter transaction details below to evaluate fraud risk and generate an AI-powered investigation report.")

# Layout for inputs
col1, col2 = st.columns(2)

with col1:
    st.subheader("💳 Transaction Details")
    amount = st.number_input("Amount (PKR)", min_value=10, max_value=500000, value=5000, help="Total transaction value in PKR")
    hour = st.slider("Hour of Day", 0, 23, 14, help="Time when the transaction occurred")
    new_recipient = st.selectbox("New Recipient", [False, True], help="Is this the first time sending to this person?")
    city = st.selectbox("City", ["Karachi", "Lahore", "Islamabad", "Faisalabad", "Rawalpindi", "Multan", "Peshawar", "Quetta"], index=0)

with col2:
    st.subheader("📱 User & Device Context")
    account_age_days = st.number_input("Account Age (Days)", min_value=0, value=30)
    transactions_today = st.number_input("Transactions Today", min_value=0, value=2)
    failed_login_attempts = st.number_input("Failed Login Attempts Today", min_value=0, value=0)
    device_id = st.text_input("Device ID", "dev_1234")

st.markdown("---")

if st.button("🚀 Run Fraud Risk Analysis", use_container_width=True):
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
    
    with st.spinner("Analyzing transaction patterns..."):
        ml_service = FraudMLService()
        result = ml_service.predict(data)
    
    if "error" in result:
        st.error(f"Prediction Error: {result['error']}")
    else:
        # Results Display
        res_col1, res_col2 = st.columns([1, 2])
        
        with res_col1:
            st.metric("Fraud Probability", f"{result['fraud_probability']:.2%}")
            
            if result['is_fraud']:
                st.error("🚨 HIGH RISK DETECTED")
                st.warning("This transaction matches known fraudulent patterns.")
            else:
                st.success("✅ LOW RISK")
                st.info("Transaction appears consistent with normal behavior.")
        
        with res_col2:
            if result['is_fraud'] or result['fraud_probability'] > 0.3:
                st.markdown("### 🤖 AI Investigation Report")
                with st.spinner("Generating detailed AI report..."):
                    try:
                        investigator = GroqFraudInvestigator()
                        report = investigator.analyze(data, result)
                        st.markdown(report)
                    except Exception as e:
                        st.error(f"AI Service Error: {str(e)}")
            else:
                st.write("No deep investigation required for low-risk transactions.")
