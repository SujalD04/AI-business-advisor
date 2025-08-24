import streamlit as st
import plotly.express as px
import pandas as pd
from utils.strategy_engine import generate_strategy


def show_dashboard(df):
    """Dashboard page for Startup Growth Advisor"""

    st.title("📊 AI-Powered Startup Growth Dashboard")

    # Check if user submitted their startup
    has_current_startup = "current_startup" in st.session_state

    # --- View mode selection ---
    view_options = ["Portfolio Mode"]
    if has_current_startup:
        view_options.append("Startup Mode")

    view_mode = st.sidebar.radio("Select View", view_options)

    # --- Startup Mode ---
    if view_mode == "Startup Mode" and has_current_startup:
        filtered_df = st.session_state["current_startup"].copy()
        filtered_df["source"] = "Your Startup"
        st.subheader(f"🚀 Visuals for {filtered_df.iloc[0]['name']}")

    # --- Portfolio Mode ---
    else:
        filtered_df = df.copy()
        filtered_df["source"] = "Portfolio"

        # Add user's startup into portfolio for comparison
        if has_current_startup:
            user_df = st.session_state["current_startup"].copy()
            user_df["source"] = "Your Startup"
            filtered_df = pd.concat([filtered_df, user_df], ignore_index=True)

        # Define fixed category orders
        industry_order = ["Retail", "SaaS", "Services", "Other"]
        cluster_order = [0, 1, 2]

        # Sidebar filters with fixed ordering
        industry_filter = st.sidebar.multiselect(
            "Select Industry",
            [i for i in industry_order if i in filtered_df["industry"].dropna().unique()]
        )
        cluster_filter = st.sidebar.multiselect(
            "Select Cluster",
            [c for c in cluster_order if c in filtered_df["cluster"].dropna().unique()]
        )

        if industry_filter:
            filtered_df = filtered_df[filtered_df["industry"].isin(industry_filter)]
        if cluster_filter:
            filtered_df = filtered_df[filtered_df["cluster"].isin(cluster_filter)]

        # Ensure plotting respects the same category order
        filtered_df["industry"] = pd.Categorical(
            filtered_df["industry"], categories=industry_order, ordered=True
        )
        filtered_df["cluster"] = pd.Categorical(
            filtered_df["cluster"], categories=cluster_order, ordered=True
        )


    # --- Generate strategies (for visuals only) ---
    df_with_strategies = generate_strategy(filtered_df)

    # --- Visualizations ---
    if not df_with_strategies.empty:
        st.header("📈 Visual Analytics")

        # Growth vs Revenue (simple scatter)
        fig1 = px.scatter(
            df_with_strategies,
            x="revenue",
            y="predicted_growth",
            color="source",  # Just Portfolio vs Your Startup
            hover_name="name",
        )
        st.plotly_chart(fig1, use_container_width=True)

        # Churn Distribution (simple boxplot)
        fig2 = px.box(
            df_with_strategies,
            x="industry",
            y="churn_rate",
            color="source",  # Highlights your startup if added
        )
        st.plotly_chart(fig2, use_container_width=True)

        # Marketing Efficiency vs Growth (clean scatter)
        fig3 = px.scatter(
            df_with_strategies,
            x="marketing_efficiency",
            y="predicted_growth",
            color="source",  # Again, Portfolio vs Your Startup
            hover_name="name",
        )
        st.plotly_chart(fig3, use_container_width=True)
