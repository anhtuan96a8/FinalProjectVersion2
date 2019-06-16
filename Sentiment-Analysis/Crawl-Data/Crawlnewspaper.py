import sys
import time

import pandas as pd
from selenium import webdriver

# add path that containing chromedriver.exe
sys.path.append('../chromedriver.exe')


# Hide Chrome browser open new window


def crawl_comment_of_item(link_of_item):
    print("Crawl comments in {0}".format(link_of_item))
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    # Create a driver to perform actions in website as: crawl,event
    browser = webdriver.Chrome(options=options)
    #
    browser.get(link_of_item)
    browser.implicitly_wait(0)
    time.sleep(5)
    # init variables
    comments = []
    types = []
    try:
        element_cmts = browser.find_elements_by_xpath('/html/body/section[2]/section/section/section[3]/article/p')
        for cmt in element_cmts:
            time.sleep(0.4)
            comment = cmt.text
            length_comment = len(comment)
            if (length_comment > 20):
                loai = 0
                comments.append(comment)
                types.append(loai)
                print("{0} : {1}".format(loai, comment))
                pass
            else:
                pass
    except:
        pass

    # close browser
    browser.quit()
    return comments,types


def save_to_csv(comments, types, filename):
    try:
        datalist = pd.read_csv(filename)
    except:
        datalist = pd.DataFrame(columns=['Comment', 'Type'])
    # add data to data list
    new_datalist = pd.DataFrame(columns=['Comment', 'Type'])
    new_datalist['Comment'] = comments
    new_datalist['Type'] = types

    datalist = datalist.append(new_datalist, ignore_index=True, sort=False)
    # save file
    datalist[['Comment', 'Type']].to_csv(filename, encoding='utf-8-sig')
    return


def crawl_link_of_items(link):
    print(link)
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    # Create a driver to perform actions in website as: crawl,event
    browser = webdriver.Chrome(options=options)
    #
    browser.get(link)
    browser.implicitly_wait(5)
    #for i in range (20) :
        #load_more = browser.find_elements_by_css_selector('//*[@id="btnViewMore"]')
        #load_more.click()
        #time.sleep(2)
# get link of item in page
    links = []
    link_elements = browser.find_elements_by_xpath('/html/body/section[2]/section/section/section[4]/section[1]/article/a')
    for element in link_elements:
        link = element.get_attribute("href")
        #link = "https://shopee.vn" + link
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
            comments, comments_type = crawl_comment_of_item(lik)
            save_to_csv(comments, comments_type, filename)
    else:
        isFound = False
        for lik, i in zip(links, range(len(links))):
            if lik.endswith(continued_link):
                isFound = True
                print("Found")
            if isFound:
                print("{}/{}".format(i, len(links)))
                comments, comments_type = crawl_comment_of_item(lik)
                save_to_csv(comments, comments_type, filename)
def crawl_singer_item(link,filename):
    comments, comments_type = crawl_comment_of_item(link)
    save_to_csv(comments, comments_type, filename)
if __name__ == '__main__':
    #page = 4
    #for page in range(4,30):
     #   crawl("http://docbao.vn/giai-tri/p{0}".format(page), filename='./express.csv')

    crawl("https://www.nguoiduatin.vn/c/doi-song", filename='./foody.csv')
    #crawl_singer_item("https://www.baodanang.vn/channel/5404/201905/thuc-hien-dong-bo-cac-giai-phap-phong-chong-dich-ta-heo-chau-phi-3202305/", filename='./foody.csv')
