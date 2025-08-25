def summarize_insights(startup_name, df_row, style="founder"):
    """
    Summarizes startup metrics with two modes:
      - 'founder': plain, motivational, actionable
      - 'investor': analytical, risk/opportunity framing
    """

    # Extract metrics
    revenue = df_row["revenue"]
    costs = df_row["costs"]
    profit = df_row["profit"]
    margin = df_row["profit_margin"]
    churn = df_row["churn_rate"]
    burn = df_row["burn_rate"]
    runway = df_row["runway_months"]
    ltv_cac = df_row["ltv_cac_ratio"]
    growth = df_row["predicted_growth"]
    cluster = df_row["cluster"]
    category = df_row["growth_category"]
    m_eff = df_row.get("marketing_efficiency", None)

    recs = df_row.get("recommendations", [])
    rec_text = "; ".join(recs) if recs else "No specific recommendations."

    # Quick health signals
    strengths, risks = [], []
    if margin > 0.2: strengths.append("healthy profit margins")
    if margin < 0.05: risks.append("weak margins")
    if ltv_cac > 3: strengths.append("strong customer economics (high LTV/CAC)")
    if ltv_cac < 1: risks.append("unsustainable acquisition costs")
    if churn < 5: strengths.append("excellent customer retention")
    if churn > 10: risks.append("high churn risk")
    if runway < 6: risks.append("limited cash runway")
    if runway > 12: strengths.append("solid financial stability")

    # ========================
    # Founder-Friendly Summary
    # ========================
    if style == "founder":
        summary = (
            f"🚀 {startup_name} is currently in the {df_row['stage']} stage "
            f"within the {df_row['industry']} industry.\n\n"
            f"You’re generating about ${revenue:,.0f} in monthly revenue with costs of ${costs:,.0f}, "
            f"leaving a profit of ${profit:,.0f} (margin: {margin*100:.1f}%). "
        )

        if m_eff is not None:
            summary += f"Marketing spend is ${df_row['marketing_spend']:,.0f}, with an efficiency of {m_eff:.2f}.\n\n"

        summary += (
            f"Your LTV/CAC ratio is {ltv_cac:.2f}, which shows "
            f"{'efficient customer acquisition' if ltv_cac >= 3 else 'room to optimize customer acquisition costs'}. "
            f"Churn is at {churn:.1f}%, and with a burn of ${burn:,.0f}/month, "
            f"you’ve got about {runway:.1f} months of runway.\n\n"
        )

        summary += (
            f"Growth-wise, you’re placed in cluster {cluster} and categorized as '{category}'. "
            f"Predicted growth is ${growth:,.0f} in the upcoming period.\n\n"
        )

        if strengths: summary += f"💡 What’s going well: {', '.join(strengths)}.\n\n"
        if risks: summary += f"⚠️ Watch out for: {', '.join(risks)}.\n\n"

        summary += f"✅ Next steps: {rec_text}"
        return summary

    # ========================
    # Investor-Style Summary
    # ========================
    elif style == "investor":
        summary = (
            f"📊 {startup_name} – {df_row['industry']} ({df_row['stage']} stage)\n\n"
            f"- Financials: ${revenue:,.0f} MRR, ${costs:,.0f} costs, ${profit:,.0f} net "
            f"({margin*100:.1f}% margin).\n"
        )
        if m_eff is not None:
            summary += f"- Marketing Efficiency: {m_eff:.2f} (spend: ${df_row['marketing_spend']:,.0f}).\n"

        summary += (
            f"- Unit Economics: LTV/CAC = {ltv_cac:.2f} "
            f"({'strong' if ltv_cac >= 3 else 'weak'})\n"
            f"- Churn: {churn:.1f}% | Runway: {runway:.1f} months (burn ${burn:,.0f}/mo)\n"
            f"- Cluster: {cluster} | Growth Category: {category}\n"
            f"- Predicted Growth: ${growth:,.0f}\n\n"
        )

        if strengths:
            summary += f"✅ Strengths: {', '.join(strengths)}.\n"
        if risks:
            summary += f"⚠️ Risks: {', '.join(risks)}.\n"

        summary += f"\n📌 Strategic Recommendations: {rec_text}"
        return summary

    else:
        raise ValueError("Style must be 'founder' or 'investor'.")
