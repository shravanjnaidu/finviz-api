import pandas as pd

path = "dailyreports/screener_data.csv"
data = pd.read_csv(path)
data.drop_duplicates(subset="Ticker", keep='first', inplace=True)
data.to_csv(path)
