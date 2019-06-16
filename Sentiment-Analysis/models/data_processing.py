import gensim
import numpy as np
import pandas as pd
from pyvi import ViTokenizer
import random


pathModelBin='./data/vnw2v.bin'


def undersampling_data(filepath):
    data = pd.read_csv(filepath)
    data_standardized = pd.DataFrame()
    y = [0, 0, 0, 0, 0]
    for rate, i in zip(data["Rate"], range(len(data))):
        if y[rate - 1] < (y[0] + y[1] + y[2] + y[3] + y[4]) / 5 + 10:
            data_standardized = data_standardized.append(data[i:i + 1])
            y[rate - 1] = y[rate - 1] + 1
    data_standardized[['Link', 'Name', 'Comment', 'Rate']].to_csv("./data/lazada-dongho-raw-undersampling.csv",
                                                                  encoding="utf-8-sig")
    print(y)


def oversampling_data(filepath):
    data = pd.read_csv(filepath)
    data_oversampling = pd.DataFrame()
    y = []
    for i in range(5):
        y.append(data[data["Rate"] == i + 1])
    for i in range(4):
        times = int(len(y[4]) / len(y[i]))
        for j in range(times):
            data_oversampling = data_oversampling.append(y[i])
    data_oversampling = data_oversampling.append(y[4]).sample(frac=1)
    data_oversampling[['Link', 'Name', 'Comment', 'Rate']].to_csv("./data/lazada-dongho-raw-oversampling.csv",
                                                                  encoding="utf-8-sig")

if __name__ == '__main__':
    oversampling_data("./data/lazada-dongho-raw.csv")
    #undersampling_data("./data/lazada-dongho-raw.csv")
