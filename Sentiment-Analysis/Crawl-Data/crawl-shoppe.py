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
    browser.implicitly_wait(7)

    # init variables
    name_of_item = ""
    # find in html element that containing comment and get text
    comments = []
    rates = []
    page = 1
    try:
        # find in html element that containing name of item
        name_element = browser.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[2]/div[2]/div[1]/span')
        name_of_item = name_element.text
        element_rate = browser.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[2]/div[2]/div[1]')
        element_rate.click()
        time.sleep(2)
        element_rate_have_cmt = browser.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[2]/div[2]/div[3]/div[2]/div[1]/div[2]/div/div[2]/div[2]/div[7]')
        element_rate_have_cmt.click()
        time.sleep(5)

        while (1):

            element_cmts = browser.find_elements_by_css_selector("div.shopee-product-rating__content")
            try:
                element_spans = browser.find_elements_by_xpath('//*[@id="main"]/div/div[2]/div[2]/div[2]/div[3]/div[2]/div[1]/div[2]/div/div[3]/div/div/div[2]/div[2]')
                for cmt, sp in zip(element_cmts, element_spans):
                    time.sleep(0.4)
                    comment = cmt.text
                    if (comment != ""):
                        # get star rate
                        elements_stars = sp.find_elements_by_xpath("./*[@class = 'shopee-svg-icon icon-rating-solid--active icon-rating-solid']")
                        stars = len(elements_stars)
                        # add to list
                        if(stars == 5):
                            comments.append(comment)
                            rates.append(stars)
                            print("{0} Star: {1}".format(stars, comment))
                            pass
                    else:
                        pass
                try:
                    xpath = "//*[@id='main']/div/div[2]/div[2]/div[2]/div[3]/div[2]/div[1]/div[2]/div/div[3]/div[2]/button[contains(text(),'{0}')]".format(page + 1)
                    #selector = "#main > div > div.shopee-page-wrapper > div.page-product > div.container > div:nth-child(3) > div.page-product__content > div.page-product__content--left > div:nth-child(2) > div > div.product-ratings__list > div.shopee-page-controller.product-ratings__page-controller > button.shopee-icon-button.shopee-icon-button--right"
                    #elm = browser.find_element_by_css_selector(selector)
                    elm = browser.find_element_by_xpath(xpath)
                    elm.click()
                    time.sleep(1)
                    page = page + 1
                    pass
                except:
                    break
            except:
                break
    except:
        pass
    # close browser
    browser.quit()
    return name_of_item, comments, rates


def save_to_csv(link, name, comments, rates, filename):
    try:
        datalist = pd.read_csv(filename)
    except:
        datalist = pd.DataFrame(columns=['Link', 'Name', 'Comment', 'Rate'])
    # add data to data list
    new_datalist = pd.DataFrame(columns=['Link', 'Name', 'Comment', 'Rate'])
    new_datalist['Link'] = [link for i in range(len(comments))]
    new_datalist['Name'] = [name for i in range(len(comments))]
    new_datalist['Comment'] = comments
    new_datalist['Rate'] = rates

    datalist = datalist.append(new_datalist, ignore_index=True, sort=False)
    # save file
    datalist[['Link', 'Name', 'Comment', 'Rate']].to_csv(filename, encoding='utf-8-sig')
    return


def crawl_link_of_items(link):
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    # Create a driver to perform actions in website as: crawl,event
    browser = webdriver.Chrome(options=options)
    #
    browser.get(link)
    browser.implicitly_wait(0)
    print(link)
    time.sleep(5)
    browser.execute_script('window.scrollTo(0, 300);')
    time.sleep(3)
    browser.execute_script('window.scrollTo(300, 600);')
    time.sleep(2)
    browser.execute_script('window.scrollTo(600, 900);')
    time.sleep(2)
    browser.execute_script('window.scrollTo(900, 1200);')
    time.sleep(2)
    browser.execute_script('window.scrollTo(1200, 1500);')
    time.sleep(2)
    browser.execute_script('window.scrollTo(1500, 1800);')
    time.sleep(2)
    browser.execute_script('window.scrollTo(1800, 2100);')
    time.sleep(2)
    browser.execute_script('window.scrollTo(2100, 2400);')
    time.sleep(2)
    browser.execute_script('window.scrollTo(2400, 2700);')
    time.sleep(2)
    browser.execute_script('window.scrollTo(2700, 3000);')
    time.sleep(2)
    browser.execute_script('window.scrollTo(3000, 3300);')
    time.sleep(2)
    browser.execute_script('window.scrollTo(3300, 3600);')
    time.sleep(2)

# get link of item in page
    links = []
    link_elements = browser.find_elements_by_css_selector('#main > div > div.shopee-page-wrapper > div:nth-child(2) > div > div > div.container._2_Y1cV > div.jrLh5s > div > div > div.row.shopee-search-item-result__items > div > div > a')
    #link_elements = browser.find_elements_by_css_selector("#main > div > div.shopee-page-wrapper > div:nth-child(2) > div > div > div.container._1EofO_ > div.SzZ8hs > div > div > div.row.shopee-search-item-result__items > div > div > a")
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
            name, comments, rates = crawl_comment_of_item(lik)
            save_to_csv(lik, name, comments, rates, filename)
    else:
        isFound = False
        for lik, i in zip(links, range(len(links))):
            if lik.endswith(continued_link):
                isFound = True
                print("Found")
            if isFound:
                print("{}/{}".format(i, len(links)))
                name, comments, rates = crawl_comment_of_item(lik)
                save_to_csv(lik, name, comments, rates, filename)
def crawl_singer_item(link,filename):
    name, comments, rates = crawl_comment_of_item(link)
    save_to_csv(link, name, comments, rates, filename)
if __name__ == '__main__':
     page = 0
     for page in range(40):
         crawl("https://shopee.vn/search?keyword=%C4%91%E1%BB%93ng%20h%E1%BB%93&page={0}&ratingFilter=1&sortBy=sales".format(page), filename='./shopee-dongho-5star.csv')
    #crawl_singer_item("https://shopee.vn/%C4%90%E1%BB%93ng-h%E1%BB%93-n%E1%BB%AF-Mstianq-h4-d%C3%A2y-da-cao-c%E1%BA%A5p-m%E1%BA%B7t-tr%C3%B2n-c%E1%BB%B1c-xinh-i.49740633.1735967828", filename='./shopee-dongho.csv')
        #crawl("https://www.lazada.vn/catalog/?_keyori=ss&from=suggest_normal&page={0}&q=%C4%91%E1%BB%93ng%20h%E1%BB%93%20nam%20ch%E1%BB%91ng%20n%C6%B0%E1%BB%9Bc&spm=a2o4n.searchlist.search.6.1fde2ce8d35TaK&sugg=%C4%91%E1%BB%93ng%20h%E1%BB%93%20nam%20ch%E1%BB%91ng%20n%C6%B0%E1%BB%9Bc_5_1".format(page + 1), filename='./lazada-dongho2.csv')
    #crawl("https://shopee.vn/search?keyword=%C4%91%E1%BB%93ng%20h%E1%BB%93&page=0&sortBy=sales", filename='./shopee-dongho.csv')
