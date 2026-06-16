import streamlit as st
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path

# Fix import path for utils
SRC_DIR = Path(__file__).parents[2]
if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))
from utils.file_locator import find_file

DATA_PATH = find_file("transactions.csv")

st.set_page_config(page_title="Fraud Analytics", layout="wide")
st.title("📊 Fraud Analytics Dashboard")

@st.cache_data
def load_data():
    if not DATA_PATH.exists():
        st.error(f"Data file not found at {DATA_PATH}")
        return pd.DataFrame()
    return pd.read_csv(DATA_PATH)

df = load_data()

if not df.empty:
    # KPI Tiles
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Transactions", f"{len(df):,}")
    col2.metric("Fraud Rate", f"{df['fraud_label'].mean():.2%}")
    col3.metric("Active Alerts", len(df[df['fraud_label'] == 1]))
    col4.metric("Avg Transaction", f"PKR {df['amount'].mean():.0f}")

    st.markdown("---")

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("### 🌆 Fraud Distribution by City")
        fraud_by_city = df[df['fraud_label'] == 1].groupby('city').size().reset_index(name='count').sort_values('count', ascending=False)
        fig_city = px.bar(fraud_by_city, x='city', y='count', color='count', color_continuous_scale='Reds')
        st.plotly_chart(fig_city, width='stretch')

    with col_right:
        st.markdown("### ⏰ Fraud by Hour of Day")
        fig_hour = px.histogram(df[df['fraud_label'] == 1], x='hour', nbins=24, color_discrete_sequence=['#FF4B4B'])
        st.plotly_chart(fig_hour, width='stretch')

    col_bottom1, col_bottom2 = st.columns(2)

    with col_bottom1:
        st.markdown("### 💰 Fraud by Amount Range")
        df['amount_range'] = pd.cut(df['amount'], bins=[0, 1000, 5000, 10000, 50000, 100000, 500000], labels=['0-1k', '1k-5k', '5k-10k', '10k-50k', '50k-100k', '100k+'])
        fraud_by_amount = df[df['fraud_label'] == 1].groupby('amount_range').size().reset_index(name='count')
        fig_amount = px.pie(fraud_by_amount, values='count', names='amount_range', hole=0.4, color_discrete_sequence=px.colors.sequential.Reds_r)
        st.plotly_chart(fig_amount, width='stretch')

    with col_bottom2:
        st.markdown("### 👤 Account Age vs Fraud")
        fig_age = px.box(df, x='fraud_label', y='account_age_days', color='fraud_label', labels={'fraud_label': 'Is Fraud?'})
        st.plotly_chart(fig_age, width='stretch')

else:
    st.warning("No data available to display analytics.")
