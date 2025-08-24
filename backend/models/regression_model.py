import pandas as pd
from sklearn.linear_model import LinearRegression

class GrowthPredictor:
    def __init__(self):
        self.model = LinearRegression()

    def train(self, df: pd.DataFrame):
        X = df[['revenue', 'costs', 'marketing_spend', 'churn_rate']]
        y = df['profit']
        self.model.fit(X, y)

    def predict(self, df: pd.DataFrame):
        X = df[['revenue', 'costs', 'marketing_spend', 'churn_rate']]
        return self.model.predict(X)
