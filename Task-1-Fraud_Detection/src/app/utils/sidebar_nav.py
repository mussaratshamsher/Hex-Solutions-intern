import streamlit as st

def show_sidebar():
    st.sidebar.title("🛡️ Investigator Panel")
    st.sidebar.markdown("---")
    st.sidebar.info("""
    **Welcome, Agent.** 
    Use this dashboard to monitor and analyze fraudulent activities in real-time.
    """)

    st.sidebar.markdown("### 🛠️ Navigation")
    # Note: Using absolute paths relative to the project root or the app directory
    # Depending on how streamlit runs, this might need adjustment. 
    # Based on main.py, these are relative to main.py's location.
    st.sidebar.page_link("main.py", label="Home", icon="🏠")
    st.sidebar.page_link("pages/1_Analytics.py", label="Market Analytics", icon="📊")
    st.sidebar.page_link("pages/2_Predictor.py", label="Fraud Predictor", icon="🔍")
    st.sidebar.page_link("pages/3_Model_Metrics.py", label="Model Health", icon="📈")
    st.sidebar.page_link("pages/4_Info.py", label="System Info", icon="ℹ️")
