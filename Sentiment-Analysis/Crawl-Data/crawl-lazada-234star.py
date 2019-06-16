import sys
import time
import re

import pandas as pd
from selenium import webdriver

# add path that containing chromedriver.exe
sys.path.append('../chromedriver.exe')


# Hide Chrome browser open new window


def crawl_comment_of_item(link_of_item):
    # init variables
    name_of_item = ""
    # find in html element that containing comment and get text
    comments = []
    rates = []
    
    print("Crawl comments in {0}".format(link_of_item))
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    # Create a driver to perform actions in website as: crawl,event
    browser = webdriver.Chrome(options=options)
    #
    browser.get(link_of_item)
    browser.implicitly_wait(10)


    try:
        # find in html element that containing name of item
        name_element = browser.find_element_by_xpath("//div[@class='pdp-product-title']/div/span")
        name_of_item = name_element.text

        for tu in range(3,7):
            name_element_filter = browser.find_element_by_css_selector("#module_product_review > div > div:nth-child(2) > div > div:nth-child(2) > span.lazada.lazada-ic-Filter1.lazada-icon.oper-icon")
            print(name_element_filter.text)
            name_element_filter.click()
            time.sleep(1)
            try:

                name_element_filter_star = browser.find_element_by_css_selector("body > div:nth-child(41) > div > div > ul > li:nth-child({0})".format(tu))

                remove_element = name_element_filter_star.get_attribute("class")
                if ("disabled" in remove_element):
                    name_element_filter.click()
                    time.sleep(0.7)
                    continue
                print(name_element_filter_star.text)

                name_element_filter_star.click()

                print("oke 2")
                page = 1
                time.sleep(1)
                while (1):
                    element_cmts = browser.find_elements_by_xpath("//div[@class = 'item']/div[@class = 'item-content']/div[@class = 'content']")
                    element_spans = browser.find_elements_by_xpath("//div[@class = 'item']/div[@class = 'top']/div")
                    for cmt, sp in zip(element_cmts, element_spans):
                        time.sleep(0.4)
                        comment = cmt.text
                        if (comment != ""):
                            # get star rate
                            elements_stars = sp.find_elements_by_xpath("./img[@src = '//laz-img-cdn.alicdn.com/tfs/TB19ZvEgfDH8KJjy1XcXXcpdXXa-64-64.png']")
                            stars = len(elements_stars)
                            # add to list
                            #stars = re.sub("\D","",name_element_filter.text)
                            comments.append(comment)
                            rates.append(stars)
                            print("{0} Star: {1}".format(stars, comment))
                            pass
                        else:
                            pass
                    # find next button

                    # click next page
                    try:
                        xpath = "//*[@id='module_product_review']/div/div[3]/div[2]/div/div/button[contains(text(),'{0}')]".format(page + 1)
                        #elm = browser.find_element_by_css_selector("#module_product_review > div > div:nth-child(3) > div.next-pagination.next-pagination-normal.next-pagination-arrow-only.next-pagination-medium.medium.review-pagination > div > button.next-btn.next-btn-normal.next-btn-medium.next-pagination-item.next")
                        elm = browser.find_element_by_xpath(xpath)
                        elm.click()
                        time.sleep(1)
                        page = page + 1
                        pass
                    except:
                        break
            except:
                pass
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
    name, questions, answers = crawl_comment_of_item(link)
    save_to_csv(link, name, questions, answers, filename)
if __name__ == '__main__':
    page = 0
    for page in range(40):
        crawl("https://www.lazada.vn/catalog/?from=input&page={0}&q=dong%20ho&rating=1".format(page + 1), filename='./lazada-dongho-234star.csv')
    #crawl_singer_item("https://www.lazada.vn/products/sieu-hotdong-ho-nam-gimto-day-da-cao-cap-hien-thi-lich-ngay-i258906668-s359709743.html?search=1", filename='./lazada-dongho-234star.csv')
        #crawl("https://www.lazada.vn/catalog/?_keyori=ss&from=suggest_normal&page={0}&q=%C4%91%E1%BB%93ng%20h%E1%BB%93%20nam%20ch%E1%BB%91ng%20n%C6%B0%E1%BB%9Bc&spm=a2o4n.searchlist.search.6.1fde2ce8d35TaK&sugg=%C4%91%E1%BB%93ng%20h%E1%BB%93%20nam%20ch%E1%BB%91ng%20n%C6%B0%E1%BB%9Bc_5_1".format(page + 1), filename='./lazada-dongho2.csv')
    #crawl("https://www.lazada.vn/catalog/?_keyori=ss&from=input&page=2&q=%C4%91%E1%BB%93ng%20h%E1%BB%93%20th%C3%B4ng%20minh&spm=a2o4n.searchlist.search.go.23fb31f601qD7X", filename='./lazada-dongho.csv')
