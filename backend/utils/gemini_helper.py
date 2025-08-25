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
    strategic and tactical, and keep responses simple and actionable.

    Startup details:
    - Name: {startup_data['name']}
    - Industry: {startup_data.get('industry', 'Unknown')}
    - Stage: {startup_data.get('stage', 'Unknown')}
    - Revenue: {startup_data['revenue']}
    - Costs: {startup_data['costs']}
    - Profit: {startup_data['profit']}
    - Profit Margin: {startup_data['profit_margin']:.2f}
    - Churn Rate: {startup_data['churn_rate']:.2f}%
    - Marketing Spend: {startup_data['marketing_spend']}
    - Marketing Efficiency: {startup_data.get('marketing_efficiency', 0):.2f}
    - Lifetime Value (LTV): {startup_data.get('lifetime_value', 0)}
    - Customer Acquisition Cost (CAC): {startup_data.get('customer_acquisition_cost', 0)}
    - LTV/CAC Ratio: {startup_data.get('ltv_cac_ratio', 0):.2f}
    - Cash Reserves: {startup_data.get('cash_reserves', 0)}
    - Burn Rate: {startup_data.get('burn_rate', 0)}
    - Runway (months): {startup_data.get('runway_months', 0):.2f}
    - Monthly Growth Rate: {startup_data.get('monthly_growth_rate', 0):.2f}
    - Cluster: {startup_data['cluster']}
    - Recommendations: {', '.join(startup_data.get('recommendations', []))}

    Use industry-specific knowledge when possible:
    - SaaS: emphasize MRR, CAC, LTV, churn reduction, and onboarding.
    - Retail: emphasize margins, inventory, pricing, foot traffic, and growth levers.
    - Services: emphasize client retention, service scalability, and repeat business.

    Keep responses practical, plain-language, and easy to implement.
    """

    # Build conversation with history
    messages = [base_context]
    for h in history:
        messages.append(f"User: {h['question']}\nAI: {h['answer']}")
    messages.append(f"User: {question}\nAI:")

    response = model.generate_content("\n".join(messages))
    return response.text

