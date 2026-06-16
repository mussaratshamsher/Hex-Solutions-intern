import streamlit as st

st.set_page_config(page_title="App Info", layout="wide")

st.title("ℹ️ About Fraud Investigator")
st.markdown("---")

st.header("🎯 Purpose")
st.write("""
The **AI-Powered Digital Wallet Fraud Investigator** was developed to address the growing challenge of financial fraud in Pakistan's digital payment ecosystem. 
As platforms like EasyPaisa and JazzCash become ubiquitous, the volume of transactions makes manual monitoring impossible. 
This tool provides a hybrid approach: **Machine Learning** for instant detection and **Generative AI** for automated investigation reporting.
""")

st.header("🛠️ How It Works")

st.subheader("1. Data Layer")
st.write("""
The app uses a synthetic dataset of 10,000+ transactions tailored to Pakistani user behavior (cities, transaction amounts in PKR, time-of-day patterns).
Key indicators tracked include:
- **Velocity**: How many transactions were made today?
- **Behavior**: Is this a new recipient?
- **Security**: Have there been failed login attempts?
- **Context**: Transaction hour, city, and device consistency.
""")

st.subheader("2. Machine Learning (XGBoost)")
st.write("""
We use a high-performance **XGBoost** model to calculate a fraud probability score. 
The model was trained to recognize complex patterns that distinguish normal behavior from fraudulent spikes, 
such as high-value transactions from new devices at unusual hours.
""")

st.subheader("3. AI Investigator (Llama 3 via Groq)")
st.write("""
When a transaction is flagged as high-risk, the data is passed to **Llama 3.3 (70B)**. 
The AI acts as a Senior Fraud Investigator, analyzing the raw data and ML score to produce a narrative report. 
This helps human agents understand the 'Why' behind the flag and take immediate action.
""")

st.header("📖 User Guide")
st.markdown("""
- **Analytics**: Explore overall trends. Look for cities with high fraud rates or 'hot' hours of activity.
- **Predictor**: This is the core tool. Enter transaction details to see if our model flags it. If flagged, read the AI report for a deep dive.
- **Model Metrics**: For technical users. This page shows the model's 'report card', including Accuracy, F1-Score, and which features (like 'Amount' or 'Transactions Today') are most important for detection.
""")

st.header("💻 Technical Stack")
st.code("""
- Frontend: Streamlit
- Data Science: Pandas, NumPy, Scikit-Learn
- ML Model: XGBoost
- Generative AI: Groq Cloud (Llama-3.3-70b-versatile)
- Visualizations: Plotly Express
""")

st.markdown("---")
st.caption("Developed by Hex Solutions for the Agentic Hackathon.")
