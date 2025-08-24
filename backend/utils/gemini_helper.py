# utils/gemini_helper.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Load API key from environment variable
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize model
model = genai.GenerativeModel("gemini-2.5-flash-lite")


def ask_gemini(startup_data, question, history=[]):
    """
    Sends startup-specific context + user question + history to Gemini
    and returns a natural language response.
    """

    base_context = f"""
    You are an AI startup advisor with expertise across multiple industries
    (SaaS, Retail, Services, and others). Provide insights that are both
    strategic and tactical.

    Startup details:
    - Name: {startup_data['name']}
    - Industry: {startup_data.get('industry', 'Unknown')}
    - Revenue: {startup_data['revenue']}
    - Profit: {startup_data['profit']}
    - Churn Rate: {startup_data['churn_rate']}
    - Cluster: {startup_data['cluster']}
    - Recommendations: {', '.join(startup_data['recommendations'])}

    Use industry-specific knowledge when possible.
    If it's SaaS, emphasize metrics like MRR, CAC, LTV.
    If Retail, emphasize margins, inventory, foot traffic.
    If Services, emphasize client retention and scalability.

    Keep responses simple, actionable, and easy to implement.
    """

    # Build conversation with history
    messages = [base_context]
    for h in history:
        messages.append(f"User: {h['question']}\nAI: {h['answer']}")
    messages.append(f"User: {question}\nAI:")

    response = model.generate_content("\n".join(messages))
    return response.text
