import sys
import time
import re
import os
import string
import re

import pandas as pd
from selenium import webdriver

# add path that containing chromedriver.exe
sys.path.append('../chromedriver.exe')


# Hide Chrome browser open new window

def download_data_lazada():
    links = []
    brands = []
    prices = []
    #details = []
    images1 = []
    images2 = []
    images3 = []
    options = webdriver.ChromeOptions()
    browser = webdriver.Chrome(options=options)

    with open('./linkmany.txt') as f:
        for line in f:
            x = 0
            line = line.rstrip()
            print(line)
            browser.get(line)
            browser.implicitly_wait(10)

            element_brand_product = browser.find_element_by_css_selector("#module_product_detail > div > div > div.pdp-mod-specification > div.pdp-general-features > ul > li:nth-child(1) > div")
            element_price_product = browser.find_element_by_css_selector("#module_product_price_1 > div > div > span")
            #element_detail_product = browser.find_element_by_css_selector("#module_product_detail > div > div > div.html-content.detail-content > p")
            # module_item_gallery_1 > div > div.gallery-preview-panel > div > img:nth-child(2)
            try:
                element_image1_product = browser.find_element_by_css_selector("#module_item_gallery_1 > div > div.gallery-preview-panel > div > img:nth-child(2)")
                image1_product = element_image1_product.get_attribute("src")
                print(image1_product)
                images1.append(image1_product)
            except:
                element_image1_product = browser.find_element_by_css_selector("#module_item_gallery_1 > div > div.gallery-preview-panel > div > img")
                image1_product = element_image1_product.get_attribute("src")
                print(image1_product)
                images1.append(image1_product)
            try:
                find_element_image2 = browser.find_element_by_css_selector("#module_item_gallery_1 > div > div.next-slick.next-slick-outer.next-slick-horizontal > div > div.next-slick-list > div > div:nth-child(2)")
                find_element_image2.click()
                time.sleep(0.5)
                element_image2_product = browser.find_element_by_css_selector("#module_item_gallery_1 > div > div.gallery-preview-panel > div > img")
                image2_product = element_image2_product.get_attribute("src")
                images2.append(image2_product)
                print(image2_product)
            except:
                images2.append(image1_product)
            try:
                find_element_image3 = browser.find_element_by_css_selector("#module_item_gallery_1 > div > div.next-slick.next-slick-outer.next-slick-horizontal > div > div.next-slick-list > div > div:nth-child(3)")
                find_element_image3.click()
                time.sleep(0.5)
                element_image3_product = browser.find_element_by_css_selector("#module_item_gallery_1 > div > div.gallery-preview-panel > div > img")
                image3_product = element_image3_product.get_attribute("src")
                images3.append(image3_product)
                print(image3_product)
            except:
                images3.append(image1_product)
            links.append(line)
            brand_product = element_brand_product.text
            brands.append(brand_product)
            print(brand_product)
            #detail_product = element_detail_product.text
            #details.append(detail_product)
            #print(detail_product)
            price_product = element_price_product.text
            prices.append(re.sub("\D","",price_product))
            print(re.sub("\D","",price_product))

    save_database_csv(links,brands,prices,images1,images2,images3,'./database-lazada.csv')



def save_database_csv(links, brands, prices, images1 , images2, images3, filename):
    try:
        datalist = pd.read_csv(filename)
    except:
        datalist = pd.DataFrame(columns=['Link', 'Brand', 'Price', 'Image1', 'Image2', 'Image3'])
    # add data to data list
    new_datalist = pd.DataFrame(columns=['Link', 'Brand', 'Price', 'Image1', 'Image2', 'Image3'])
    new_datalist['Link'] = links
    new_datalist['Brand'] = brands
    new_datalist['Price'] = prices
    #new_datalist['Detail'] = details
    new_datalist['Image1'] = images1
    new_datalist['Image2'] = images2
    new_datalist['Image3'] = images3

    datalist = datalist.append(new_datalist, ignore_index=True, sort=False)
    # save file
    datalist[['Link', 'Brand', 'Price', 'Image1', 'Image2', 'Image3']].to_csv(filename, encoding='utf-8-sig')
    return



def get_file_name( path):
    return os.path.basename(path).split(".")[0].strip().lower()
def test ():
    with open('./test.txt') as f:
        for line in f:
            print(line)

def extractMax(input): 
    numbers = re.findall('\d+',input)
    numbers = map(int,numbers)
    x = max(numbers)
    print (max(numbers))
def test2():
    x ='VND 200,000'
    b = re.sub("\D","","VND 20,00")
    print(b)
if __name__ == '__main__':
    download_data_lazada()
