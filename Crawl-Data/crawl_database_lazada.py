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
    names = []
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

            element_name_product = browser.find_element_by_css_selector("#module_product_title_1 > div > div > span")
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
            name_product = element_name_product.text
            names.append(name_product)
            print(name_product)
            brand_product = element_brand_product.text
            brands.append(brand_product)
            print(brand_product)
            #detail_product = element_detail_product.text
            #details.append(detail_product)
            #print(detail_product)
            price_product = element_price_product.text
            prices.append(re.sub("\D","",price_product))
            print(re.sub("\D","",price_product))

    save_database_csv(links,names,brands,prices,images1,images2,images3,'./database-lazada2.csv')



def save_database_csv(links, names, brands, prices, images1 , images2, images3, filename):
    try:
        datalist = pd.read_csv(filename)
    except:
        datalist = pd.DataFrame(columns=['Link', 'Name', 'Brand', 'Price', 'Image1', 'Image2', 'Image3'])
    # add data to data list
    new_datalist = pd.DataFrame(columns=['Link', 'Name', 'Brand', 'Price', 'Image1', 'Image2', 'Image3'])
    new_datalist['Link'] = links
    new_datalist['Name'] = names
    new_datalist['Brand'] = brands
    new_datalist['Price'] = prices
    #new_datalist['Detail'] = details
    new_datalist['Image1'] = images1
    new_datalist['Image2'] = images2
    new_datalist['Image3'] = images3

    datalist = datalist.append(new_datalist, ignore_index=True, sort=False)
    # save file
    datalist[['Link', 'Name', 'Brand', 'Price', 'Image1', 'Image2', 'Image3']].to_csv(filename, encoding='utf-8-sig')
    return

    
                  
def crawl_comment_of_item(link_of_item):
    print("Crawl questions answers in {0}".format(link_of_item))
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    # Create a driver to perform actions in website as: crawl,event
    browser = webdriver.Chrome(options=options)
    #
    browser.get(link_of_item)
    browser.implicitly_wait(10)

    # init variables
    name_of_item = ""
    # find in html element that containing comment and get text
    questions = []
    answers = []
    page = 1
    try:
        # find in html element that containing name of item
        name_element = browser.find_element_by_xpath("//div[@class='pdp-product-title']/div/span")
        name_of_item = name_element.text

        while (1):
            qna_elements = browser.find_elements_by_xpath("//ul[@class = 'qna-list']/li[@class = 'qna-item']")

            for qna in qna_elements:
                time.sleep(0.4)
                ques_element = qna.find_element_by_xpath("./div[1]//div[@class='qna-content']")
                ans_element = qna.find_element_by_xpath("./div[2]//div[@class='qna-content']")
                ques = ques_element.text
                ans = ans_element.text
                # add to list
                questions.append(ques)
                answers.append(ans)
                print("{0} : {1}".format(ques, ans))
                pass
            # find next button
            elms = browser.find_elements_by_xpath("//button[@class = 'next-btn next-btn-normal next-btn-medium next-pagination-item next' and @disabled = '']")
            if(len(elms) == 1):
                break
            # click next page
            xpath = "//div[@id='module_product_qna']//div[@class = 'next-pagination-list']/button[contains(text(),'{0}')]".format(page + 1)
            elm = browser.find_element_by_xpath(xpath)
            elm.click()
            time.sleep(1)
            page = page + 1
            pass
    except BaseException:
        print(BaseException)
        pass
    # close browser
    browser.quit()
    return name_of_item, questions, answers


def save_to_csv(link, name, questions, answers, filename):
    try:
        datalist = pd.read_csv(filename)
    except:
        datalist = pd.DataFrame(columns=['Link', 'Name', 'Question', 'Answer'])
    # add data to data list
    new_datalist = pd.DataFrame(columns=['Link', 'Name', 'Question', 'Answer'])
    new_datalist['Link'] = [link for i in range(len(questions))]
    new_datalist['Name'] = [name for i in range(len(questions))]
    new_datalist['Question'] = questions
    new_datalist['Answer'] = answers

    datalist = datalist.append(new_datalist, ignore_index=True, sort=False)
    # save file
    datalist[['Link', 'Name', 'Question', 'Answer']].to_csv(filename, encoding='utf-8-sig')
    return


def crawl_link_of_items(link):
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    # Create a driver to perform actions in website as: crawl,event
    browser = webdriver.Chrome(options=options)
    #
    browser.get(link)
    browser.implicitly_wait(10)

# get link of item in page
    links = []
    link_elements = browser.find_elements_by_xpath("//div[@data-spm = 'list']/div[@data-tracking = 'product-card']/div/div/div[1]/div/a")
    for element in link_elements:
        link = element.get_attribute("href")
        links.append(link)
    print("Total link: {0}".format(len(links)))
    # close browser
    browser.quit()
    return links

def crawl(link, filename, continued_link=None):
    links = crawl_link_of_items(link)
    if continued_link is None:
        for lik, i in zip(links, range(len(links))):
            print("{}/{}".format(i, len(links)))
            name, questions, answers = crawl_comment_of_item(lik)
            save_to_csv(lik, name, questions, answers, filename)
    else:
        isFound = False
        for lik, i in zip(links, range(len(links))):
            if lik.endswith(continued_link):
                isFound = True
                print("Found")
            if isFound:
                print("{}/{}".format(i, len(links)))
                name, questions, answers = crawl_comment_of_item(lik)
                save_to_csv(lik, name, questions, answers, filename)
def crawl_singer_item(link,filename):
    name, questions, answers = crawl_comment_of_item(link)
    save_to_csv(link, name, questions, answers, filename)

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
