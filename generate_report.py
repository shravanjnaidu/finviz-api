import csv
import pandas as pd
import os

def main():
  os.system('python scrap_finviz.py')
  path = "finviz-api/dailyreports/screener_data.csv"
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

  #creates a list of all runners
  with open('finviz-api/dailyreports/screener_data.csv', 'r') as file:
    data = file.read().replace('\n', ',')
    li = list(data.split(",,"))
    li = li[1:-1]
    print(li)
    return li


if __name__ == "__main__":
    main()