import csv

path = 'dailyreports/screener_data.csv'
with open(path) as f:
  data = list(csv.reader(f))
  new_data = [a for i, a in enumerate(data) if a not in data[:i]]
  with open(path, 'w') as t:
     write = csv.writer(t)
     write.writerows(new_data)