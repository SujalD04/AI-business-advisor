def summarize_insights(startup_name, df_row):
    """
    Summarizes startup metrics in plain language with actionable insights.
    """
    recs = df_row.get('recommendations', [])
    rec_text = "; ".join(recs) if recs else "No specific recommendations"

    summary = (
        f"🚀 {startup_name} is currently in the {df_row['stage']} stage within the {df_row['industry']} industry. "
        f"It has a monthly revenue of ${df_row['revenue']:.2f} and costs of ${df_row['costs']:.2f}, "
        f"resulting in a profit of ${df_row['profit']:.2f} (profit margin: {df_row['profit_margin']*100:.1f}%). "
        f"Marketing spend is ${df_row['marketing_spend']:.2f}, achieving a marketing efficiency of {df_row['marketing_efficiency']:.2f}. "
        f"The LTV/CAC ratio is {df_row['ltv_cac_ratio']:.2f}, indicating how efficiently the startup acquires and retains customers. "
        f"Churn rate stands at {df_row['churn_rate']:.1f}%, and the startup has enough cash to last {df_row['runway_months']:.1f} months at the current burn rate. "
        f"Based on patterns, it belongs to cluster {df_row['cluster']} and is categorized as '{df_row['growth_category']}' in growth potential. "
        f"Predicted growth for the upcoming period is ${df_row['predicted_growth']:.2f}. "
        f"Recommended actions: {rec_text}."
    )
    
    return summary
