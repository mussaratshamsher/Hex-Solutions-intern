import streamlit as st
import pandas as pd
import xgboost as xgb
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report, f1_score, precision_score, recall_score
import plotly.express as px
import os
from pathlib import Path

# Robust path setup
def get_project_root():
    curr = Path(__file__).resolve()
    for parent in curr.parents:
        if parent.name == 'src':
            return parent.parent
    return curr.parents[3]

PROJECT_ROOT = get_project_root()
DATA_PATH = PROJECT_ROOT / "data" / "transactions.csv"
MODEL_PATH = PROJECT_ROOT / "models" / "fraud_model.pkl"

st.set_page_config(page_title="Model Metrics", layout="wide")
st.title("📈 Model Performance Metrics")

@st.cache_resource
def load_model():
    if not MODEL_PATH.exists():
        st.error(f"Model file not found at {MODEL_PATH}")
        return None
    return joblib.load(MODEL_PATH)

@st.cache_data
def get_data():
    if not DATA_PATH.exists():
        st.error(f"Data file not found at {DATA_PATH}")
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
    m1.metric("Accuracy", f"{(y_test == y_pred).mean():.2%}")
    m2.metric("F1-Score", f"{f1_score(y_test, y_pred):.2f}")
    m3.metric("Precision", f"{precision_score(y_test, y_pred):.2f}")
    m4.metric("Recall", f"{recall_score(y_test, y_pred):.2f}")

    st.markdown("---")

    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown("### 📊 Classification Report")
        report = classification_report(y_test, y_pred, output_dict=True)
        report_df = pd.DataFrame(report).transpose()
        st.dataframe(report_df.style.background_gradient(cmap='Reds'))

    with col_r:
        st.markdown("### 🔍 Confusion Matrix")
        cm = confusion_matrix(y_test, y_pred)
        fig = px.imshow(cm, text_auto=True, 
                        labels=dict(x="Predicted", y="Actual"),
                        x=['Not Fraud', 'Fraud'],
                        y=['Not Fraud', 'Fraud'],
                        color_continuous_scale='Reds')
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 🏆 Feature Importance")
    importance = pd.DataFrame({'Feature': X.columns, 'Importance': model.feature_importances_}).sort_values('Importance', ascending=True)
    fig_imp = px.bar(importance, x='Importance', y='Feature', orientation='h', color='Importance', color_continuous_scale='Viridis')
    st.plotly_chart(fig_imp, use_container_width=True)
else:
    st.warning("Data or Model could not be loaded.")
