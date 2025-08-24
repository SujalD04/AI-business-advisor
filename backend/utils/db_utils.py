import pandas as pd
from config import engine

def fetch_startup_data():
    query = "SELECT * FROM startup_info"
    df = pd.read_sql(query, con=engine)
    return df
