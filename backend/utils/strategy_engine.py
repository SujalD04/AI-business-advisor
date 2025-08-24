def generate_strategy(df):
    """
    Enhanced rule-based recommendations:
    - Uses predicted growth, cluster, churn_rate, marketing efficiency
    - Adds industry-specific insights
    - Suggests actionable next steps
    """
    strategies = []

    for _, row in df.iterrows():
        recs = []

        # Growth-based recommendations
        if row['predicted_growth'] < 0:
            recs.append("Focus on cost reduction, improve cash flow, and retain existing customers.")
        elif row['predicted_growth'] < 0.1 * row['revenue']:
            recs.append("Optimize marketing campaigns, refine sales funnels, and analyze customer behavior.")
        elif row['predicted_growth'] < 0.3 * row['revenue']:
            recs.append("Consider strategic partnerships or explore adjacent markets for moderate growth.")
        else:
            recs.append("High growth potential: expand product lines, scale team, and invest in R&D.")

        # Cluster-based recommendations
        if row['cluster'] == 0:
            recs.append("Early-stage archetype: validate product-market fit and prioritize MVP improvements.")
        elif row['cluster'] == 1:
            recs.append("Growth-stage archetype: invest in customer acquisition and optimize internal processes.")
        elif row['cluster'] == 2:
            recs.append("Mature archetype: focus on strategic expansion, operational efficiency, and diversification.")

        # Churn-based recommendation
        if row['churn_rate'] > 20:
            recs.append("High churn detected: implement customer retention programs, loyalty incentives, or feedback loops.")
        elif row['churn_rate'] > 10:
            recs.append("Moderate churn: monitor customer satisfaction and address pain points.")

        # Marketing efficiency
        if row['marketing_efficiency'] < 0.8:
            recs.append("Marketing spend is low efficiency: reallocate budget or test new channels.")
        elif row['marketing_efficiency'] < 1.2:
            recs.append("Moderate marketing efficiency: optimize campaigns for higher ROI.")

        # Industry-specific recommendations
        if row['industry'] == "SaaS":
            recs.append("SaaS-specific: prioritize customer onboarding, reduce churn, and monitor subscription metrics.")
        elif row['industry'] == "Retail":
            recs.append("Retail-specific: analyze inventory turnover, optimize pricing, and enhance customer experience.")
        elif row['industry'] == "Services":
            recs.append("Services-specific: improve service delivery, client satisfaction, and repeat business strategies.")

        strategies.append(recs)

    df['recommendations'] = strategies
    return df
