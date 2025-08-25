from jinja2 import Environment, FileSystemLoader
import pdfkit
from pathlib import Path
import streamlit as st
from utils.strategy_engine import generate_strategy

import base64
import matplotlib.pyplot as plt
import io

def ensure_required_columns(df, required_cols):
    """Ensure all required columns exist in the dataframe.
    If missing, create them with default values (zeros or NaN)."""
    for col in required_cols:
        if col not in df.columns:
            df[col] = np.nan  # or 0 if you prefer default 0
    return df

# ---------------- Utility ----------------
def fig_to_base64(fig):
    """Convert matplotlib figure to base64 string."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    plt.close(fig)
    return base64.b64encode(buf.read()).decode("utf-8")

def generate_startup_charts(startup):
    """Generate multiple charts for a single startup with new metrics."""
    charts = {}

    # 1. Financial Breakdown
    fig, ax = plt.subplots()
    ax.bar(
        ["Revenue", "Costs", "Marketing Spend", "Profit"], 
        [startup["revenue"], startup["costs"], startup["marketing_spend"], startup["profit"]],
        color=["#1a73e8", "#e74c3c", "#2ecc71", "#f1c40f"]
    )
    ax.set_title(f"Financial Overview - {startup['name']}")
    charts["financial"] = fig_to_base64(fig)

    # 2. Growth Projection
    fig, ax = plt.subplots()
    ax.bar(
        ["Current Revenue", "Predicted Growth"], 
        [startup["revenue"], startup["predicted_growth"]],
        color=["#1a73e8", "#f1c40f"]
    )
    ax.set_title("Growth Projection")
    charts["growth"] = fig_to_base64(fig)

    # 3. Marketing Efficiency vs Churn
    fig, ax = plt.subplots()
    ax.scatter([startup["marketing_efficiency"]], [startup["churn_rate"]], s=150, color="purple")
    ax.set_xlabel("Marketing Efficiency")
    ax.set_ylabel("Churn Rate (%)")
    ax.set_title("Marketing Efficiency vs Churn")
    charts["marketing_vs_churn"] = fig_to_base64(fig)

    # 4. Profit Margin vs Predicted Growth
    fig, ax = plt.subplots()
    ax.scatter([startup["profit_margin"]], [startup["predicted_growth"]], s=150, color="#ff7f0e")
    ax.set_xlabel("Profit Margin")
    ax.set_ylabel("Predicted Growth")
    ax.set_title("Profit Margin vs Growth")
    charts["profit_margin_vs_growth"] = fig_to_base64(fig)

    # 5. LTV/CAC vs Churn Rate
    fig, ax = plt.subplots()
    ax.scatter([startup["ltv_cac_ratio"]], [startup["churn_rate"]], s=150, color="#2ca02c")
    ax.set_xlabel("LTV/CAC Ratio")
    ax.set_ylabel("Churn Rate (%)")
    ax.set_title("LTV/CAC vs Churn")
    charts["ltv_cac_vs_churn"] = fig_to_base64(fig)

    # 6. Runway Months vs Predicted Growth
    fig, ax = plt.subplots()
    ax.bar(["Runway Months", "Predicted Growth"], [startup["runway_months"], startup["predicted_growth"]],
           color=["#9467bd", "#f1c40f"])
    ax.set_title("Runway vs Growth")
    charts["runway_vs_growth"] = fig_to_base64(fig)

    return charts

# ---------------- PDF Generator ----------------
def generate_pdf_report(df):
    """Generate a PDF report with charts and recommendations."""
    BASE_DIR = Path(__file__).resolve().parent  # backend/
    templates_dir = BASE_DIR / "templates"

    # Add charts per startup
    startups = df.to_dict(orient="records")
    for s in startups:
        charts = generate_startup_charts(s)
        s["charts"] = charts

    # Load template
    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template("report_template.html")
    html_content = template.render(startups=startups)

    # Generate PDF in memory
    pdf_bytes = pdfkit.from_string(html_content, False)
    return pdf_bytes

# ---------------- Streamlit Reports Page ----------------
def show_reports(regressor, classifier, clustering, cluster_features):
    """Reports page for Startup Growth Advisor"""

    st.title("📑 Generate Startup Reports")

    if "current_startup" not in st.session_state:
        st.warning("Please submit your startup details in the form first.")
        return

    df = st.session_state["current_startup"]
    # Rename DB/input columns to match model features
    df = df.rename(columns={
        "customer_acquisition_cost": "cac",
        "lifetime_value": "ltv"
    })

    # 🔹 Ensure regression features exist
    regression_features = ["revenue", "costs", "marketing_spend", "churn_rate",
                       "burn_rate", "cash_reserves", "cac", "ltv", 
                       "profit_margin", "marketing_efficiency", "ltv_cac_ratio"]
    
    df = ensure_required_columns(df, regression_features)

    # Enrich data
    df["predicted_growth"] = regressor.predict(df[regression_features])
    df["cluster"] = clustering.model.predict(df[cluster_features])

    df_with_strategies = generate_strategy(df)

    if st.button("Generate PDF Report"):
        pdf_bytes = generate_pdf_report(df_with_strategies)
        st.download_button(
            "📥 Download Report",
            pdf_bytes,
            file_name="startup_report.pdf",
            mime="application/pdf"
        )

