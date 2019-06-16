
import pandas as pd
import csv


def Split_data():
    cmt = []
    type_cmt = []
    # with open('./data/lazada-dongho-raw.csv', 'r') as csvFile:
    #     reader = csv.reader(csvFile)
    #     for row in reader:
    #         print(row['Comment'])
    with open(('./comment_rate.json'),'r', encoding="utf8") as f:
        for line in f:
            line = line.rstrip('\n')
            split_cmt = line.split('.')
            for i in range(len(split_cmt)):
                if(len(split_cmt[i]) > 5 ) :
                    cmt.append(split_cmt[i])
    print(len(cmt))
    for i in range(len(cmt)):
        type_value = 0
        type_cmt.append(type_value)
    try:
        datalist = pd.read_csv('./comment_rate.csv')
    except:
        datalist = pd.DataFrame(columns=['Comment', 'Type'])
    # add data to data list
    new_datalist = pd.DataFrame(columns=['Comment', 'Type'])
    new_datalist['Comment'] = cmt
    new_datalist['Type'] = type_cmt

    datalist = datalist.append(new_datalist, ignore_index=True, sort=False)
    # save file
    datalist[['Comment', 'Type']].to_csv('./comment_rate.csv', encoding='utf-8-sig')

if __name__ == '__main__':
    Split_data()
