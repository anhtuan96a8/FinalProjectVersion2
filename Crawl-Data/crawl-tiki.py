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
    time.sleep(6)
    # init variables
    name_of_item = ""
    # find in html element that containing comment and get text
    comments = []
    rates = []
    page = 1
    try:
        # find in html element that containing name of item
        name_element = browser.find_element_by_css_selector('#product-name > span:nth-child(3)')
        name_of_item = name_element.text
        element_click_to_rate = browser.find_element_by_css_selector('body > div.wrap > div.container.product-container > div.row.product-summary > div.product-cart > div > div.product-brand-block > div > div > div:nth-child(1) > div > div.item-rating a')
        element_click_to_rate.click()
        time.sleep(1.5)
        element_click_to_chose = browser.find_element_by_css_selector('#product-review-box > div > div.review-filter > div:nth-child(3) > button')
        element_click_to_chose.click()
        time.sleep(0.5)
        element_click_to_chose_2 = browser.find_element_by_xpath('//*[@id="product-review-box"]/div/div[1]/div[2]/ul/li[2]/a')
        element_click_to_chose_2.click()
        time.sleep(1)

        while (1):
            
            element_cmts = browser.find_elements_by_css_selector("#product-review-box > div > div.review-list > div > div.product-col-2 > div > div.description.js-description > p > span:nth-child(1)")
            print(len(element_cmts))
            try:
                element_spans = browser.find_elements_by_xpath('//*[@id="product-review-box"]/div/div[2]/div/div[3]/div[1]/div[1]/span/span')
                print(len(element_spans))
                for cmt, sp in zip(element_cmts, element_spans):
                    time.sleep(0.4)
                    comment = cmt.text
                    if (comment != ""):
                        # get star rate
                        #elements_stars = sp.find_element_by_xpath("./*[@class = 'active_-0Kp']")
                        style = sp.get_attribute("style")
                        if "100" in style:
                            stars = 5
                        elif "80" in style:
                            stars = 4
                        elif "60" in style:
                            stars = 3
                        elif "40" in style:
                            stars = 2
                        else:
                            stars = 1
                        # add to list
                        if(stars !=5):
                            comments.append(comment)
                            rates.append(stars)
                            print("{0} Star: {1}".format(stars, comment))
                        pass
                    else:
                        pass
                try:
                    xpath = "//*[@id='product-review-box']/div/div[2]/div[6]/ul/li/a[contains(text(),'{0}')]".format(page + 1)
                    #selector = "#main > div > div.shopee-page-wrapper > div.page-product > div.container > div:nth-child(3) > div.page-product__content > div.page-product__content--left > div:nth-child(2) > div > div.product-ratings__list > div.shopee-page-controller.product-ratings__page-controller > button.shopee-icon-button.shopee-icon-button--right"
                    #elm = browser.find_element_by_css_selector(selector)
                    elm = browser.find_element_by_xpath(xpath)
                    elm.click()
                    time.sleep(3)
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
    print(link)
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    # Create a driver to perform actions in website as: crawl,event
    browser = webdriver.Chrome(options=options)
    #
    browser.get(link)
    browser.implicitly_wait(7)
    browser.execute_script('window.scrollTo(1, 500);')
    time.sleep(8)

# get link of item in page
    links = []
    link_elements = browser.find_elements_by_css_selector('body > div.wrap > div > div.product-listing > div:nth-child(2) > div.product-box-list > div > a')
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
    page = 18
    for page in range(18,28):
         crawl("https://tiki.vn/search?q=%C4%91%E1%BB%93ng+h%E1%BB%93&rating=1&order=top_seller&page={0}".format(page), filename='./tiki-dongho-star.csv')
    #crawl_singer_item("https://tiki.vn/dong-ho-thong-minh-inwatch-c1-p584220.html?src=search&2hi=0&keyword=%C4%91%E1%BB%93ng+h%E1%BB%93", filename='./tiki-dongho2.csv')
        #crawl("https://www.lazada.vn/catalog/?_keyori=ss&from=suggest_normal&page={0}&q=%C4%91%E1%BB%93ng%20h%E1%BB%93%20nam%20ch%E1%BB%91ng%20n%C6%B0%E1%BB%9Bc&spm=a2o4n.searchlist.search.6.1fde2ce8d35TaK&sugg=%C4%91%E1%BB%93ng%20h%E1%BB%93%20nam%20ch%E1%BB%91ng%20n%C6%B0%E1%BB%9Bc_5_1".format(page + 1), filename='./lazada-dongho2.csv')
    #crawl("https://tiki.vn/search?q=%C4%91%E1%BB%93ng+h%E1%BB%93&order=top_seller&rating=1", filename='./tiki-dongho.csv')
