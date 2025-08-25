import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

class GrowthPredictor:
    def __init__(self):
        self.features = [
            'revenue', 'costs', 'marketing_spend', 'churn_rate',
            'burn_rate', 'cash_reserves', 'cac',
            'ltv', 'profit_margin', 'marketing_efficiency', 'ltv_cac_ratio'
        ]
        self.models = {
            'LinearRegression': LinearRegression(),
            'RandomForest': RandomForestRegressor(n_estimators=200, random_state=42),
            'XGBoost': xgb.XGBRegressor(n_estimators=200, learning_rate=0.05, random_state=42)
        }
        self.trained_models = {}

    def train(self, df: pd.DataFrame):
        X = df[self.features]
        y = df['profit']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        for name, model in self.models.items():
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            r2 = r2_score(y_test, y_pred)
            print(f"{name} RMSE: {rmse:.2f}, R2: {r2:.2f}")
            self.trained_models[name] = model

    def predict(self, df: pd.DataFrame, model_name='RandomForest'):
        return self.trained_models[model_name].predict(df[self.features])
