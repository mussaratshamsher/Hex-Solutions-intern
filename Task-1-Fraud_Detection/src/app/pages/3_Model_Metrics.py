import streamlit as st
import pandas as pd
import xgboost as xgb
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report, f1_score, precision_score, recall_score
import plotly.express as px
import sys
from pathlib import Path

# Fix import path for utils
SRC_DIR = Path(__file__).parents[2]
if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))
from utils.file_locator import find_file

# Load Custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

MODEL_PATH = find_file("fraud_model.pkl")
DATA_PATH = find_file("transactions.csv")

st.set_page_config(page_title="Model Metrics", layout="wide")

# Apply CSS
css_path = SRC_DIR / "app" / "style.css"
if css_path.exists():
    local_css(str(css_path))

st.title("📈 Model Performance Metrics")
st.markdown("Technical breakdown of the XGBoost fraud detection model.")

@st.cache_resource
def load_model():
    if MODEL_PATH is None:
        st.error("Model path not found (find_file returned None)")
        return None
    if not MODEL_PATH.exists():
        st.error(f"Model file does not exist at {MODEL_PATH}")
        return None
    return joblib.load(MODEL_PATH)

@st.cache_data
def get_data():
    if DATA_PATH is None:
        st.error("Data path not found (find_file returned None)")
        return pd.DataFrame()
    if not DATA_PATH.exists():
        st.error(f"Data file does not exist at {DATA_PATH}")
        return pd.DataFrame()
    df = pd.read_csv(DATA_PATH)
    # Simple re-encoding for metrics calculation
    from sklearn.preprocessing import LabelEncoder
    le_city = LabelEncoder()
    le_device = LabelEncoder()
    df['city'] = le_city.fit_transform(df['city'])
    df['device_id'] = le_device.fit_transform(df['device_id'])
    return df

df = get_data()
model = load_model()

if not df.empty and model:
    X = df.drop(['transaction_id', 'sender_id', 'receiver_id', 'transaction_time', 'fraud_label'], axis=1)
    y = df['fraud_label']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    y_pred = model.predict(X_test)

    # Top level metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Accuracy", f"{(y_test == y_pred).mean():.2%}", help="Overall correctly predicted transactions.")
    with m2:
        st.metric("F1-Score", f"{f1_score(y_test, y_pred):.2f}", help="Balance between Precision and Recall.")
    with m3:
        st.metric("Precision", f"{precision_score(y_test, y_pred):.2f}", help="Of all predicted fraud, how much was actually fraud?")
    with m4:
        st.metric("Recall", f"{recall_score(y_test, y_pred):.2f}", help="Of all actual fraud, how much did we catch?")

    st.markdown("---")

    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown("### 📊 Classification Report")
        report = classification_report(y_test, y_pred, output_dict=True)
        report_df = pd.DataFrame(report).transpose()
        st.dataframe(report_df, use_container_width=True)

    with col_r:
        st.markdown("### 🔍 Confusion Matrix")
        cm = confusion_matrix(y_test, y_pred)
        fig = px.imshow(cm, text_auto=True, 
                        labels=dict(x="Predicted", y="Actual"),
                        x=['Not Fraud', 'Fraud'],
                        y=['Not Fraud', 'Fraud'],
                        color_continuous_scale='Reds',
                        template="plotly_dark")
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 🏆 Feature Importance")
    importance = pd.DataFrame({'Feature': X.columns, 'Importance': model.feature_importances_}).sort_values('Importance', ascending=True)
    fig_imp = px.bar(
        importance, 
        x='Importance', 
        y='Feature', 
        orientation='h', 
        color='Importance', 
        color_continuous_scale='Viridis',
        template="plotly_dark"
    )
    fig_imp.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_imp, use_container_width=True)
else:
    st.warning("Data or Model could not be loaded. Please ensure mock models are created.")
    if st.button("Generate Mock Models"):
        # Placeholder for functionality if we wanted to add it
        st.info("Run 'python create_mock_models.py' in the terminal.")
