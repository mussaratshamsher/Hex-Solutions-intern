import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

st.title("Fraud Analytics")

@st.cache_data
def load_data():
    return pd.read_csv('data/transactions.csv')

df = load_data()

# KPI Tiles
col1, col2, col3 = st.columns(3)
col1.metric("Total Transactions", len(df))
col2.metric("Fraud Rate", f"{df['fraud_label'].mean():.2%}")
col3.metric("Active Alerts", len(df[df['fraud_label'] == 1]))

# Visualizations
st.markdown("### Fraud Distribution by City")
fig_city = px.bar(df[df['fraud_label'] == 1].groupby('city').size().reset_index(name='count'), x='city', y='count')
st.plotly_chart(fig_city)

st.markdown("### Fraud by Hour")
fig_hour = px.histogram(df[df['fraud_label'] == 1], x='hour', nbins=24)
st.plotly_chart(fig_hour)
