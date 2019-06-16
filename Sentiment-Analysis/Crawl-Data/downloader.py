import sys
from selenium import webdriver
import pandas as pd

import time
sys.path.append('../chromedriver.exe')

driver=webdriver.Chrome()
options = webdriver.ChromeOptions()
options.add_argument("headless")
driver.get('https://www.youtube.com/watch?v=bOn6_cno28E')
page = 500
for i in range(70) :
    driver.execute_script('window.scrollTo(1, {0});'.format(page))
    time.sleep(3)
    page = page + 1500
browser = webdriver.Chrome(options=options)
#now wait let load the comments
for x in range(6):
    a = x*500
    print("dang load")
    time.sleep(2)

comment_youtube = []

print("oke")

comment_div=driver.find_element_by_xpath('//*[@id="contents"]')
comments=comment_div.find_elements_by_xpath('//*[@id="content-text"]')
for comment in comments:
    print(comment.text)
    comment_youtube.append(comment.text)
    
try:
    datalist = pd.read_csv('./comment_youtube.csv')
except:
    datalist = pd.DataFrame(columns=['Comment'])
    
new_datalist = pd.DataFrame(columns=['Comment'])
new_datalist['Comment'] = comment_youtube
datalist = datalist.append(new_datalist, ignore_index=True, sort=False)
datalist[['Comment']].to_csv('./comment_youtube.csv', encoding='utf-8-sig')
