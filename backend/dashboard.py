import streamlit as st
import plotly.express as px
import pandas as pd
from utils.strategy_engine import generate_strategy

def show_dashboard(df):
    """Simplified, clean dashboard for Startup Growth Advisor."""

    st.title("📊 AI-Powered Startup Growth Dashboard")

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

        st.subheader("📊 Portfolio Overview")

        # Sidebar filters (no default selections)
        industry_options = filtered_df["industry"].dropna().unique().tolist()
        industry_filter = st.sidebar.multiselect("Select Industry", industry_options)

        cluster_options = filtered_df["cluster"].dropna().unique().tolist()
        cluster_filter = st.sidebar.multiselect("Select Cluster", cluster_options)

        growth_options = filtered_df["growth_category"].dropna().unique().tolist()
        growth_filter = st.sidebar.multiselect("Select Growth Category", growth_options)

        if industry_filter:
            filtered_df = filtered_df[filtered_df["industry"].isin(industry_filter)]
        if cluster_filter:
            filtered_df = filtered_df[filtered_df["cluster"].isin(cluster_filter)]
        if growth_filter:
            filtered_df = filtered_df[filtered_df["growth_category"].isin(growth_filter)]

    # --- Generate strategies (for visuals only) ---
    df_with_strategies = generate_strategy(filtered_df)

    # --- Visualizations ---
    if not df_with_strategies.empty:
        st.header("📈 Visual Analytics")

        # Growth vs Revenue (scatter)
        fig1 = px.scatter(
            df_with_strategies,
            x="revenue",
            y="predicted_growth",
            color="growth_category",
            symbol="source",
            hover_name="name",
            size_max=6,  # fixed max size
            size=[5]*len(df_with_strategies),  # uniform point size
            title="Predicted Growth vs Revenue"
        )
        st.plotly_chart(fig1, use_container_width=True)

        # Churn Distribution by Industry (boxplot)
        fig2 = px.box(
            df_with_strategies,
            x="industry",
            y="churn_rate",
            color="growth_category",
            hover_data=["name"],
            title="Churn Rate Distribution by Industry"
        )
        st.plotly_chart(fig2, use_container_width=True)

        # Marketing Efficiency vs Growth (scatter)
        fig3 = px.scatter(
            df_with_strategies,
            x="marketing_efficiency",
            y="predicted_growth",
            color="growth_category",
            symbol="source",
            hover_name="name",
            size=[5]*len(df_with_strategies),  # uniform size
            size_max=6,
            title="Marketing Efficiency vs Predicted Growth"
        )
        st.plotly_chart(fig3, use_container_width=True)

        # Profit Margin vs Runway (scatter)
        fig4 = px.scatter(
            df_with_strategies,
            x="profit_margin",
            y="runway_months",
            color="growth_category",
            symbol="source",
            hover_name="name",
            size=[5]*len(df_with_strategies),
            size_max=6,
            title="Profit Margin vs Runway (Months)"
        )
        st.plotly_chart(fig4, use_container_width=True)
