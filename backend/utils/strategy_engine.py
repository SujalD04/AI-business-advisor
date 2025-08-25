def generate_strategy(df):
    """
    Enhanced rule-based recommendations incorporating new metrics:
    - Uses predicted growth, cluster, churn_rate, marketing efficiency
    - Adds financial health, LTV/CAC, runway insights
    - Industry-specific actionable next steps
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
            recs.append("Marketing efficiency is low: reallocate budget or test new channels.")
        elif row['marketing_efficiency'] < 1.2:
            recs.append("Moderate marketing efficiency: optimize campaigns for higher ROI.")

        # Profit margin check
        if row['profit_margin'] < 0.1:
            recs.append("Profit margin is low: review pricing strategy and reduce unnecessary expenses.")
        elif row['profit_margin'] > 0.25:
            recs.append("Healthy profit margin: consider reinvesting for growth or product development.")

        # LTV/CAC ratio
        if row['ltv_cac_ratio'] < 1:
            recs.append("Customer acquisition is expensive relative to value: improve retention or optimize acquisition costs.")
        elif row['ltv_cac_ratio'] > 3:
            recs.append("Strong LTV/CAC ratio: scaling customer acquisition could be profitable.")

        # Runway and cash reserves
        if row['runway_months'] < 3:
            recs.append("Low runway: secure funding or cut non-essential costs to extend runway.")
        elif row['runway_months'] > 12:
            recs.append("Healthy cash reserves: opportunity to invest in growth initiatives.")

        # Industry-specific recommendations
        if row['industry'] == "SaaS":
            recs.append("SaaS-specific: prioritize onboarding, reduce churn, and monitor subscription metrics.")
        elif row['industry'] == "Retail":
            recs.append("Retail-specific: analyze inventory turnover, optimize pricing, and enhance customer experience.")
        elif row['industry'] == "Services":
            recs.append("Services-specific: improve service delivery, client satisfaction, and repeat business strategies.")

        strategies.append(recs)

    df['recommendations'] = strategies
    return df
