def summarize_insights(startup_name, df_row):
    recs = df_row.get('recommendations', [])
    rec_text = "; ".join(recs) if recs else "No specific recommendations"
    return (
        f"🚀 Startup {startup_name} is projected to grow by ${df_row['predicted_growth']:.2f}. "
        f"Profit: ${df_row['profit']:.2f}, Churn rate: {df_row['churn_rate']:.2f}%, "
        f"Cluster type: {df_row['cluster']}. Recommended actions: {rec_text}."
    )
