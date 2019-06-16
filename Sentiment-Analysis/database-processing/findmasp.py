
import pandas as pd

def change():
    masps =[]
    links = []
    names = []
    socot = []
    linkthua =[]
    namethua =[]
    name_one = pd.read_csv('./database-lazada.csv')
    name_two = pd.read_csv('./abc.csv')
    for a,b,c,d,e in zip(name_one['Name'],name_one['Brand'],name_one['LoaiSP'],name_one['Price'],name_one['socot']) :
        print(a)
        print(b)
        print(c)
        print(d)
        print(e)
        for f,g,h,i,k in zip(name_two['MaSP'],name_two['TenSP'],name_two['LoaiSP'],name_two['GiaGoc'],name_two['HangSX']):
            if(a==g and b==k and c==h and d==i) :
                print(f)
                print(g)
                print(h)
                print(i)
                print(k)
                masps.append(f)
                names.append(a)
                socot.append(e)
    save_database_csv(masps,names,socot,'./findmasp.csv')
def change2():
    name_one = pd.read_csv('./findmasp.csv')
    for i in name_one['MaSP'] :
                print(i)
def save_database_csv(masps, names,socot, filename):
    try:
        datalist = pd.read_csv(filename)
    except:
        datalist = pd.DataFrame(columns=['MaSP','Name','socot'])
    # add data to data list
    new_datalist = pd.DataFrame(columns=['MaSP','Name','socot'])
    new_datalist['MaSP'] = masps
    new_datalist['Name'] = names
    new_datalist['socot'] = socot
    datalist = datalist.append(new_datalist, ignore_index=True, sort=False)
    # save file
    datalist[['MaSP','Name','socot']].to_csv(filename, encoding='utf-8-sig')
    return

if __name__ == '__main__':
    change2()
