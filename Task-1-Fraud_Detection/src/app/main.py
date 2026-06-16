import streamlit as st

st.set_page_config(page_title="Fraud Investigator", layout="wide")
st.title("AI-Powered Digital Wallet Fraud Investigator")
st.markdown("""
### Welcome to the Fraud Investigator Dashboard
This platform provides real-time fraud detection and automated investigation reporting for Pakistani Digital Wallets.
- **Analytics**: View trends and patterns in transactions.
- **Predictor**: Run a fraud check on a specific transaction.
- **Model Metrics**: View performance metrics of the underlying XGBoost model.
""")
