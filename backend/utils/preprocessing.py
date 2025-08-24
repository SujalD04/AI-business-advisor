import pandas as pd

def preprocess_startup_data(df: pd.DataFrame) -> pd.DataFrame:
    # Fill missing values
    df['revenue'] = df['revenue'].fillna(0)
    df['costs'] = df['costs'].fillna(0)
    df['churn_rate'] = df['churn_rate'].fillna(df['churn_rate'].mean())
    df['marketing_spend'] = df['marketing_spend'].fillna(0)

    # Feature engineering
    df['profit'] = df['revenue'] - df['costs']
    df['profit_margin'] = df['profit'] / df['revenue'].replace(0, 1)
    df['marketing_efficiency'] = df['revenue'] / df['marketing_spend'].replace(0, 1)

    return df
