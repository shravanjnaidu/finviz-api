import pandas as pd

data = pd.read_csv("screener_data.csv")
data.drop_duplicates(subset="Ticker", keep='first', inplace=True)
data.to_csv("screener_data.csv")
