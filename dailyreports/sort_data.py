import pandas as pd

data = pd.read_csv("SalesJan2009.csv")
data.drop_duplicates(subset="Product", keep='first', inplace=True)
data.to_csv("SalesSorted.csv")
