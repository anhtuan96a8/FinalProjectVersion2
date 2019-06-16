
import pandas as pd

def change():
    links = []
    names = []
    socot = []
    linkthua =[]
    namethua =[]
    name_one = pd.read_csv('./database-lazada.csv')
    name_two = pd.read_csv('./link-database-tgdt.csv')
    for a,b,c in zip(name_one['Link'],name_one['Name'],name_one['socot']) :
        print(a)
        print(b)
        print(c)
        for d,e,f in zip(name_two['Link'],name_two['Name'],name_two['socot']):
            if(a==d) :
                print(d)
                print(e)
                links.append(a)
                names.append(e)
                socot.append(c)
    save_database_csv(links,names,socot,'./change-data.csv')
def change2():
    links = []
    names = []
    name_one = pd.read_csv('./database-lazada.csv')
    name_two = pd.read_csv('./link-database-tgdt.csv')
    for i in name_one['Link'] :
        for j,q in zip(name_two['Link'],name_two['Name']):
            if(i==j) :
                print(i)
                print(j)
                print(q)
                links.append(j)
                names.append(q)
    save_database_csv(links,names,'./change-data.csv')
def save_database_csv(links, names,socot, filename):
    try:
        datalist = pd.read_csv(filename)
    except:
        datalist = pd.DataFrame(columns=['Link','Name','socot'])
    # add data to data list
    new_datalist = pd.DataFrame(columns=['Link','Name','socot'])
    new_datalist['Link'] = links
    new_datalist['Name'] = names
    new_datalist['socot'] = socot
    datalist = datalist.append(new_datalist, ignore_index=True, sort=False)
    # save file
    datalist[['Link','Name','socot']].to_csv(filename, encoding='utf-8-sig')
    return

if __name__ == '__main__':
    change()