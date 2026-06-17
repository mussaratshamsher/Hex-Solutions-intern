import streamlit as st
from pathlib import Path

# Fix import path for utils
SRC_DIR = Path(__file__).parents[2]

# Load Custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.set_page_config(page_title="App Info", layout="wide")

# Apply CSS
css_path = SRC_DIR / "app" / "style.css"
if css_path.exists():
    local_css(str(css_path))

st.title("ℹ️ About Fraud Investigator")
st.markdown("Detailed breakdown of the system architecture and mission.")
st.markdown("---")

col_main, col_side = st.columns([2, 1])

with col_main:
    st.header("🎯 Purpose")
    st.markdown("""
    <div class="custom-card" style="border-left-color: #FF4B4B;">
        <p>The <b>AI-Powered Digital Wallet Fraud Investigator</b> was developed to address the growing challenge of financial fraud in Pakistan's digital payment ecosystem.</p>
        <p>As platforms like EasyPaisa and JazzCash become ubiquitous, the volume of transactions makes manual monitoring impossible. This tool provides a hybrid approach: <b>Machine Learning</b> for instant detection and <b>Generative AI</b> for automated investigation reporting.</p>
    </div>
    """, unsafe_allow_html=True)

    st.header("🛠️ How It Works")

    tab1, tab2, tab3 = st.tabs(["📊 Data Layer", "🧠 ML Engine", "🤖 AI Investigator"])

    with tab1:
        st.subheader("Synthetic Behavior Modeling")
        st.write("""
        The app uses a synthetic dataset of 10,000+ transactions tailored to Pakistani user behavior (cities, transaction amounts in PKR, time-of-day patterns).
        Key indicators tracked include:
        - **Velocity**: How many transactions were made today?
        - **Behavior**: Is this a new recipient?
        - **Security**: Have there been failed login attempts?
        - **Context**: Transaction hour, city, and device consistency.
        """)

    with tab2:
        st.subheader("XGBoost Classification")
        st.write("""
        We use a high-performance **XGBoost** model to calculate a fraud probability score. 
        The model was trained to recognize complex patterns that distinguish normal behavior from fraudulent spikes, 
        such as high-value transactions from new devices at unusual hours.
        """)

    with tab3:
        st.subheader("Llama 3.3 (70B) via Groq")
        st.write("""
        When a transaction is flagged as high-risk, the data is passed to **Llama 3.3**. 
        The AI acts as a Senior Fraud Investigator, analyzing the raw data and ML score to produce a narrative report. 
        This helps human agents understand the 'Why' behind the flag and take immediate action.
        """)

with col_side:
    st.header("💻 Tech Stack")
    st.markdown("""
    - **Frontend**: Streamlit
    - **Brain**: XGBoost (ML)
    - **Voice**: Llama 3 via Groq (GenAI)
    - **Data**: Pandas / NumPy
    - **Visuals**: Plotly / CSS3
    """)
    
    st.info("System Version: **v1.0.2**")
    st.success("Deployment: **Stable**")

st.markdown("---")
st.header("📖 User Guide")
col_g1, col_g2, col_g3 = st.columns(3)

with col_g1:
    st.markdown("### 📊 Analytics")
    st.write("Explore overall trends. Look for cities with high fraud rates or 'hot' hours of activity.")

with col_g2:
    st.markdown("### 🔍 Predictor")
    st.write("The core tool. Enter transaction details to see if our model flags it and read the AI report.")

with col_g3:
    st.markdown("### 📈 Metrics")
    st.write("For technical users. View Accuracy, F1-Score, and feature importance.")

st.markdown("---")
st.caption("Developed by Hex Solutions for the Agentic Hackathon | 2026")
