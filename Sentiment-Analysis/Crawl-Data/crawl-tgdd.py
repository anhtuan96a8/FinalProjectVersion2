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
    browser.implicitly_wait(20)

    # init variables
    name_of_item = ""
    # find in html element that containing comment and get text
    comments = []
    rates = []
    page = 1
    try:
        # find in html element that containing name of item
        name_element = browser.find_element_by_xpath("//div[@class='rowtop']/h1")
        name_of_item = name_element.text

        while (1):
            element_cmts = browser.find_elements_by_xpath("//ul[@class = 'ratingLst']/li[@class = 'par']/div/p/i")
            element_spans = browser.find_elements_by_xpath("//ul[@class = 'ratingLst']/li[@class = 'par']/div/p/span")
            for cmt, sp in zip(element_cmts, element_spans):
                time.sleep(1)
                comment = cmt.text
                # get star rate
                elements_stars = sp.find_elements_by_xpath("./i[@class = 'iconcom-txtstar']")
                stars = len(elements_stars)
                # add to list
                comments.append(comment)
                rates.append(stars)
                print("{0} Star: {1}".format(stars, comment))
                pass
            # click next page
            xpath = "//a[@href='javascript:ratingCmtList({0})']".format(page + 1)
            elm = browser.find_element_by_xpath(xpath)
            elm.click()
            time.sleep(1)
            page = page + 1
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
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    # Create a driver to perform actions in website as: crawl,event
    browser = webdriver.Chrome(options=options)
    #
    browser.get(link)
    browser.implicitly_wait(20)
    # click showmore until show all item
    try:
        while (1):
            element = browser.find_element_by_xpath("//section/a[@class='viewmore']")
            time.sleep(1)
            element.click()
            time.sleep(2)
    except:
        pass


# get link of item in page
    links = []
    link_elements = browser.find_elements_by_xpath("//ul[@class = 'homeproduct']/li/a")
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


if __name__ == '__main__':
    crawl("https://www.thegioididong.com/dong-ho-deo-tay", filename='./tgdd-dong-ho-raw2.csv')
