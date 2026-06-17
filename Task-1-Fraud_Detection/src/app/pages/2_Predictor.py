import streamlit as st
import sys
import os
from pathlib import Path

# Robust path setup for imports
def get_src_dir():
    curr = Path(__file__).resolve()
    for parent in curr.parents:
        if parent.name == 'src':
            return parent
    return curr.parents[3] / "src"

SRC_DIR = get_src_dir()
if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

from services.ml_service import FraudMLService
from services.groq_client import GroqFraudInvestigator

st.set_page_config(page_title="Fraud Predictor", layout="wide")
st.title("🔍 Transaction Fraud Predictor")
st.markdown("Evaluate fraud risk via manual entry or batch CSV upload.")

tab1, tab2 = st.tabs(["👤 Single Prediction", "📂 Batch Upload (CSV)"])

with tab1:
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

    if st.button("🚀 Run Fraud Risk Analysis", key="single_btn", width='stretch'):
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
                else:
                    st.success("✅ LOW RISK")
            
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

with tab2:
    st.subheader("📤 Batch Processing")
    st.write("Upload a CSV file to process multiple transactions at once.")
    
    # Template download
    template_data = "amount,city,hour,device_id,account_age_days,transactions_today,failed_login_attempts,new_recipient\n5000,Karachi,14,dev_1,30,2,0,0"
    st.download_button("📥 Download CSV Template", template_data, "fraud_template.csv", "text/csv")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        df_upload = pd.read_csv(uploaded_file)
        st.write("### Preview of Uploaded Data")
        st.dataframe(df_upload.head())
        
        if st.button("🚀 Process Batch", key="batch_btn"):
            with st.spinner("Scoring batch transactions..."):
                try:
                    ml_service = FraudMLService()
                    results = []
                    
                    # Process each row
                    for _, row in df_upload.iterrows():
                        row_dict = row.to_dict()
                        # Ensure correct types
                        row_dict['new_recipient'] = int(row_dict['new_recipient'])
                        res = ml_service.predict(row_dict)
                        results.append({
                            'Fraud_Probability': f"{res['fraud_probability']:.2%}",
                            'Risk_Level': "HIGH" if res['is_fraud'] else "LOW"
                        })
                    
                    # Combine and show
                    res_df = pd.concat([df_upload, pd.DataFrame(results)], axis=1)
                    st.success("Batch Processing Complete!")
                    st.dataframe(res_df)
                    
                    # Download results
                    csv_res = res_df.to_csv(index=False).encode('utf-8')
                    st.download_button("💾 Download Scored Results", csv_res, "fraud_results.csv", "text/csv")
                except Exception as e:
                    st.error(f"Error processing batch: {str(e)}")
