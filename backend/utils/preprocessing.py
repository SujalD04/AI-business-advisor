import pandas as pd

def preprocess_startup_data(df: pd.DataFrame) -> pd.DataFrame:
    # --- Normalize column names ---
    df.columns = df.columns.str.strip().str.lower()
    df = df.rename(columns={
        "customer_acquisition_cost": "cac",
        "lifetime_value": "ltv"
    })

    # --- Ensure required columns exist (if missing, add with 0) ---
    required_cols = [
        'revenue', 'costs', 'burn_rate', 'cash_reserves',
        'cac', 'ltv',
        'marketing_spend', 'monthly_growth_rate', 'market_share', 'churn_rate'
    ]
    for col in required_cols:
        if col not in df.columns:
            df[col] = 0

    # --- Fill missing financials ---
    for col in required_cols:
        df[col] = df[col].fillna(0)

    # --- Feature engineering ---
    df['profit'] = df['revenue'] - df['costs']
    df['profit_margin'] = df['profit'] / df['revenue'].replace(0, 1)
    df['marketing_efficiency'] = df['revenue'] / df['marketing_spend'].replace(0, 1)
    df['ltv_cac_ratio'] = df['ltv'] / df['cac'].replace(0, 1)
    df['runway_months'] = df['cash_reserves'] / df['burn_rate'].replace(0, 1)
    df['monthly_growth_rate'] = df['revenue'].pct_change().fillna(0)

    # --- Growth Category label (for classifier) ---
    def growth_category(row):
        if row['monthly_growth_rate'] > 0.15 and row['profit_margin'] > 0.1:
            return "High"
        elif row['monthly_growth_rate'] > 0.05:
            return "Medium"
        else:
            return "Low"

    df['growth_category'] = df.apply(growth_category, axis=1)

    return df
