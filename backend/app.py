import streamlit as st
import pandas as pd
from pathlib import Path
from sqlalchemy import text

# Local imports
from config import engine
from utils.preprocessing import preprocess_startup_data
from models.regression_model import GrowthPredictor
from models.clustering_model import StartupClustering
from utils.strategy_engine import generate_strategy
from utils.nlp_summarizer import summarize_insights
from utils.report_generator import show_reports
from dashboard import show_dashboard
from utils.gemini_helper import ask_gemini


# --- Paths ---
BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "models" / "startups_data.csv"

# --- Train models with synthetic dataset (keep untouched) ---
df_synthetic = pd.read_csv(CSV_PATH)
df_train = preprocess_startup_data(df_synthetic)

regressor = GrowthPredictor()
regressor.train(df_train)

clustering = StartupClustering(n_clusters=3)
cluster_features = [
    "revenue",
    "costs",
    "marketing_spend",
    "churn_rate",
    "profit_margin",
    "marketing_efficiency",
]
clustering.model.fit(df_train[cluster_features])

# --- Navigation Menu (Dashboard always visible, just locked until form is submitted) ---
menu = st.sidebar.radio(
    "Go to:", 
    ["Form Input", "Dashboard", "Reports", "Ask Gemini"]
)


# -------------------------
# FORM PAGE
# -------------------------
if menu == "Form Input":
    st.title("AI-powered Business Advisor (MVP)")
    st.header("Enter your startup data")

    # Initialize session state for form values if not set
    if "form_data" not in st.session_state:
        st.session_state.form_data = {
            "name": "",
            "industry": "SaaS",
            "stage": "Idea",
            "revenue": 0.0,
            "costs": 0.0,
            "churn_rate": 0.0,
            "marketing_spend": 0.0,
        }

    with st.form("startup_form"):
        name = st.text_input("Startup Name", value=st.session_state.form_data["name"])
        industry = st.selectbox(
            "Industry", ["SaaS", "Retail", "Services", "Other"], 
            index=["SaaS", "Retail", "Services", "Other"].index(st.session_state.form_data["industry"])
        )
        stage = st.selectbox(
            "Stage", ["Idea", "Early", "Growth", "Scale"], 
            index=["Idea", "Early", "Growth", "Scale"].index(st.session_state.form_data["stage"])
        )
        revenue = st.number_input(
            "Monthly Revenue", min_value=0.0, step=100.0, value=st.session_state.form_data["revenue"]
        )
        costs = st.number_input(
            "Monthly Costs", min_value=0.0, step=100.0, value=st.session_state.form_data["costs"]
        )
        churn_rate = st.number_input(
            "Churn Rate (%)", min_value=0.0, max_value=100.0, step=0.1, value=st.session_state.form_data["churn_rate"]
        )
        marketing_spend = st.number_input(
            "Monthly Marketing Spend", min_value=0.0, step=100.0, value=st.session_state.form_data["marketing_spend"]
        )

        submitted = st.form_submit_button("Submit")

    # --- Handle submission ---
    if submitted:
        # Save form data to session state
        st.session_state.form_data = {
            "name": name,
            "industry": industry,
            "stage": stage,
            "revenue": revenue,
            "costs": costs,
            "churn_rate": churn_rate,
            "marketing_spend": marketing_spend,
        }

        # Build DataFrame for new startup
        df_new = pd.DataFrame([st.session_state.form_data])

        with engine.begin() as conn:
            df_new.to_sql("startup_info", conn, if_exists="append", index=False)

        # Preprocess + predict
        df_new_processed = preprocess_startup_data(df_new)
        regression_features = ["revenue", "costs", "marketing_spend", "churn_rate"]
        df_new_processed["predicted_growth"] = regressor.predict(
            df_new_processed[regression_features]
        )
        df_new_processed["cluster"] = clustering.model.predict(
            df_new_processed[cluster_features]
        )

        # ✅ Save current startup + insights
        st.session_state["current_startup"] = df_new_processed
        st.session_state["insights"] = {
            "strategies": generate_strategy(df_new_processed),
            "summaries": {
                row["name"]: summarize_insights(row["name"], row)
                for _, row in df_new_processed.iterrows()
            },
        }

        # ✅ Load and process portfolio data from DB
        with engine.connect() as conn:
            df_db = pd.read_sql(text("SELECT * FROM startup_info"), conn)

        df_db_processed = preprocess_startup_data(df_db)
        df_db_processed["predicted_growth"] = regressor.predict(
            df_db_processed[regression_features]
        )
        df_db_processed["cluster"] = clustering.model.predict(
            df_db_processed[cluster_features]
        )
        st.session_state["all_startups"] = df_db_processed

        st.success("Startup data submitted successfully! ✅")

    # --- Show insights if they exist (persist across navigation) ---
    if "current_startup" in st.session_state:
        df_new_processed = st.session_state["current_startup"]

        st.subheader("Your Startup Insights")
        for _, row in df_new_processed.iterrows():
            st.markdown(f"### 🚀 {row['name']}")
            col1, col2 = st.columns(2)
            col1.metric("Predicted Growth", f"{row['predicted_growth']:.2f}")
            col2.metric("Cluster ID", f"{row['cluster']}")

        st.divider()
        st.header("Business Recommendations")
        for _, row in st.session_state["insights"]["strategies"].iterrows():
            st.subheader(f"Startup: {row['name']}")
            for rec in row["recommendations"]:
                st.write(f"- {rec}")

        st.header("Summarized Insights")
        for startup_name, summary in st.session_state["insights"]["summaries"].items():
            st.subheader(f"Startup: {startup_name}")
            st.text(summary)

        # --- Clear data button ---
        if st.button("🗑️ Clear Form & Insights"):
            for key in ["form_data", "current_startup", "all_startups", "insights"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()


# -------------------------
# DASHBOARD PAGE
# -------------------------
elif menu == "Dashboard":
    if "all_startups" not in st.session_state:
        st.warning("⚠️ Please submit your startup first using the Form Input page.")
    else:
        show_dashboard(st.session_state["all_startups"])


# -------------------------
# REPORTS PAGE
# -------------------------
elif menu == "Reports":
    show_reports(regressor, clustering, cluster_features)


# -------------------------
# ASK GEMINI
# -------------------------
elif menu == "Ask Gemini":
    st.title("🤖 Ask Gemini (AI Startup Advisor)")

    if "current_startup" not in st.session_state:
        st.warning("Please submit your startup first in the Form Input page.")
    else:
        # Get the latest startup data
        startup_df = st.session_state["current_startup"].iloc[0]
        startup_data = startup_df.to_dict()
        startup_data["recommendations"] = startup_df.get("recommendations", [])

        # Initialize conversation history
        if "gemini_chat" not in st.session_state:
            st.session_state["gemini_chat"] = []

        # Display previous chat history in nice chat bubbles
        for chat in st.session_state["gemini_chat"]:
            with st.chat_message("user"):
                st.write(chat["question"])
            with st.chat_message("assistant"):
                st.write(chat["answer"])

        # Input box
        question = st.text_input("Ask a question about your startup:")

        if st.button("Ask Gemini"):
            if question.strip():
                with st.chat_message("user"):
                    st.write(question)

                with st.spinner("Gemini is thinking..."):
                    answer = ask_gemini(
                        startup_data,
                        question,
                        st.session_state["gemini_chat"]
                    )

                with st.chat_message("assistant"):
                    st.write(answer)

                # Save history
                st.session_state["gemini_chat"].append(
                    {"question": question, "answer": answer}
                )
            else:
                st.warning("Please type a question first.")

