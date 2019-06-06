import csv
import pandas as pd

path = "2019-06-06_1608.csv"
f=pd.read_csv(path)
keep_col = ['Ticker']
new_f = f[keep_col]
new_f.to_csv(path, index=False)

#deletes duplicates
with open(path) as f:
  data = list(csv.reader(f))
  new_data = [a for i, a in enumerate(data) if a not in data[:i]]
  with open(path, 'w') as t:
     write = csv.writer(t)
     write.writerows(new_data)
