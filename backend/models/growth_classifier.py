from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pandas as pd

class GrowthClassifier:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=200, random_state=42)

    def train(self, df: pd.DataFrame):
        features = ['revenue', 'costs', 'marketing_spend', 'churn_rate',
                    'burn_rate', 'cash_reserves', 'cac',
                    'ltv', 'profit_margin', 'marketing_efficiency', 'ltv_cac_ratio']
        X = df[features]
        y = df['growth_category']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)
        print(classification_report(y_test, y_pred))

    def predict(self, df: pd.DataFrame):
        features = ['revenue', 'costs', 'marketing_spend', 'churn_rate',
                    'burn_rate', 'cash_reserves', 'cac',
                    'ltv', 'profit_margin', 'marketing_efficiency', 'ltv_cac_ratio']
        return self.model.predict(df[features])
