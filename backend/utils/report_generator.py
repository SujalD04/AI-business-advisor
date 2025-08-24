from jinja2 import Environment, FileSystemLoader
import pdfkit
from pathlib import Path
import streamlit as st
from utils.strategy_engine import generate_strategy

import base64
import matplotlib.pyplot as plt
import io

# ---------------- Utility ----------------
def fig_to_base64(fig):
    """Convert matplotlib figure to base64 string."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    plt.close(fig)
    return base64.b64encode(buf.read()).decode("utf-8")

def generate_startup_charts(startup):
    """Generate multiple charts for a single startup."""
    charts = {}

    # 1. Financial Breakdown
    fig, ax = plt.subplots()
    ax.bar(["Revenue", "Costs", "Marketing"], 
           [startup["revenue"], startup["costs"], startup["marketing_spend"]],
           color=["#1a73e8", "#e74c3c", "#2ecc71"])
    ax.set_title(f"Financial Breakdown - {startup['name']}")
    charts["financial"] = fig_to_base64(fig)

    # 2. Growth Projection
    fig, ax = plt.subplots()
    ax.bar(["Current Revenue", "Predicted Growth"], 
           [startup["revenue"], startup["predicted_growth"]],
           color=["#1a73e8", "#f1c40f"])
    ax.set_title("Growth Projection")
    charts["growth"] = fig_to_base64(fig)

    # 3. Marketing vs Churn
    fig, ax = plt.subplots()
    ax.scatter([startup["marketing_efficiency"]], [startup["churn_rate"]],
               s=150, color="purple")
    ax.set_xlabel("Marketing Efficiency")
    ax.set_ylabel("Churn Rate (%)")
    ax.set_title("Marketing Efficiency vs Churn")
    charts["marketing_vs_churn"] = fig_to_base64(fig)

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
def show_reports(regressor, clustering, cluster_features):
    """Reports page for Startup Growth Advisor"""

    st.title("📑 Generate Startup Reports")

    if "current_startup" not in st.session_state:
        st.warning("Please submit your startup details in the form first.")
        return

    df = st.session_state["current_startup"]

    # Enrich data
    regression_features = ["revenue", "costs", "marketing_spend", "churn_rate"]
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
