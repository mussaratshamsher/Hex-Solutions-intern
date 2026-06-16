import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class GroqFraudInvestigator:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.3-70b-versatile"

    def analyze(self, transaction_data, ml_result):
        indicators = []
        if ml_result['fraud_probability'] > 0.7:
            indicators.append("High ML Risk Score")
        if transaction_data.get('failed_login_attempts', 0) > 0:
            indicators.append("Failed Login Attempts")
        if transaction_data.get('transactions_today', 0) > 4:
            indicators.append("Velocity Spike")
            
        prompt = f"""
System: You are a Senior Fraud Investigator at a leading Pakistani Fintech. 
Analyze the following transaction data and ML risk score.

Context:
- Transaction Amount: {transaction_data['amount']} PKR
- ML Fraud Probability: {ml_result['fraud_probability']:.2f}%
- Flagged Indicators: {', '.join(indicators)}
- Location: {transaction_data['city']}
- Device: {transaction_data['device_id']}

Task:
1. Explain why the ML model flagged this (Human-readable).
2. Assess the risk level (Low/Medium/High/Critical).
3. Recommend 3 immediate actions (e.g., Block account, Call customer, Request biometric).
4. Provide a 2-sentence summary for the management report.

Output Format: Professional Markdown.
"""
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model,
        )
        return response.choices[0].message.content
