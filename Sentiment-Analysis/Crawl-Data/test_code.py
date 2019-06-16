import pandas as pd

data = pd.read_csv("./tgdd-raw-oversampling.csv")
y = [0, 0, 0, 0, 0]
for i in range(5):
    y[i] = len(data[data["Rate"] == i+1])
print(y)
print(len(data))