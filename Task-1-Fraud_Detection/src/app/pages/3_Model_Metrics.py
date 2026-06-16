import streamlit as st
import pandas as pd
import xgboost as xgb
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report
import plotly.express as px
import os

st.title("Model Metrics")

@st.cache_resource
def load_model():
    model = joblib.load('models/fraud_model.pkl')
    return model

@st.cache_data
def get_data():
    df = pd.read_csv('data/transactions.csv')
    # Simple re-encoding for metrics calculation
    from sklearn.preprocessing import LabelEncoder
    le_city = LabelEncoder()
    le_device = LabelEncoder()
    df['city'] = le_city.fit_transform(df['city'])
    df['device_id'] = le_device.fit_transform(df['device_id'])
    return df

df = get_data()
model = load_model()

X = df.drop(['transaction_id', 'sender_id', 'receiver_id', 'transaction_time', 'fraud_label'], axis=1)
y = df['fraud_label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

y_pred = model.predict(X_test)

st.markdown("### Classification Report")
report = classification_report(y_test, y_pred, output_dict=True)
st.dataframe(pd.DataFrame(report).transpose())

st.markdown("### Confusion Matrix")
fig = px.imshow(confusion_matrix(y_test, y_pred), text_auto=True, labels=dict(x="Predicted", y="Actual"))
st.plotly_chart(fig)

st.markdown("### Feature Importance")
importance = pd.DataFrame({'Feature': X.columns, 'Importance': model.feature_importances_}).sort_values('Importance', ascending=False)
fig_imp = px.bar(importance, x='Importance', y='Feature', orientation='h')
st.plotly_chart(fig_imp)
