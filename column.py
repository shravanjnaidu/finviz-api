import pandas as pd
path = "dailyreports/screener_data.csv"
f=pd.read_csv(path)
keep_col = ['Ticker']
new_f = f[keep_col]
new_f.to_csv(path, index=False)