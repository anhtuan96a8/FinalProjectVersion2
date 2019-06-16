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
    time.sleep(8)
    # init variables
    comments = []
    types = []
    page = 1
    try:
        while (1) :
            try :
                # find in html element that containing name of item
                path = '//*[@id="result-box"]/div[1]/div/div/div[{0}]/div[2]/div[5]/div/div[1]/a[1]'.format(page)
                comment_element = browser.find_element_by_xpath(path)
                comment_element.click()
                time.sleep(4)

                while (1):
                    try:
                        element_cmts = browser.find_elements_by_xpath('//*[@id="review-list"]/li/div[2]/div/span')
                        for cmt in element_cmts:
                            time.sleep(0.4)
                            comment = cmt.text
                            length_comment = len(comment)
                            if (length_comment > 0 and length_comment < 80):
                                type0 = 0
                                comments.append(comment)
                                types.append(type0)
                                print("{0} : {1}".format(types, comment))
                                pass
                            else:
                                pass
                        try:
                            xpath = "#review-list > li.pn-loadmore.fd-clearbox.ng-scope > a"
                            elm = browser.find_element_by_xpath(xpath)
                            elm.click()
                            time.sleep(3)
                            pass
                        except:
                            break
                    except:
                        break
                close_element = browser.find_element_by_xpath('//*[@id="fdDlgReviews"]/div[2]')
                close_element.click()
                page = page + 1
            except : break

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
    time.sleep(10)


# get link of item in page
    links = []
    link_elements = browser.find_elements_by_css_selector('#page-container > div > div.section_1wD5 > div.resultPanel_2-sN > div:nth-child(3) > div > div > div > div > a')
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
            comments, comments_type = crawl_comment_of_item(link)
            save_to_csv(comments, comments_type, filename)
    else:
        isFound = False
        for lik, i in zip(links, range(len(links))):
            if lik.endswith(continued_link):
                isFound = True
                print("Found")
            if isFound:
                print("{}/{}".format(i, len(links)))
                comments, comments_type = crawl_comment_of_item(link)
                save_to_csv(comments, comments_type, filename)
def crawl_singer_item(link,filename):
    comments, comments_type = crawl_comment_of_item(link)
    save_to_csv(comments, comments_type, filename)
if __name__ == '__main__':
    crawl_singer_item("https://www.foody.vn/ho-chi-minh/an-vat-via-he?CategoryGroup=food&c=an-vat-via-he", filename='./foody.csv')
    #crawl_singer_item("https://www.sendo.vn/dong-ho-nam-chinh-hang-prema-smm116-10986317.html?source_block_id=search_products&source_info=desktop2_60_1557883947640_a96ae3a7242e4efe9cf4dff875b425b9_-1_algo6_-1_424_3_-1&source_page_id=search_norder_30_desc", filename='./sendo-dongho12.csv')
        #crawl("https://www.lazada.vn/catalog/?_keyori=ss&from=suggest_normal&page={0}&q=%C4%91%E1%BB%93ng%20h%E1%BB%93%20nam%20ch%E1%BB%91ng%20n%C6%B0%E1%BB%9Bc&spm=a2o4n.searchlist.search.6.1fde2ce8d35TaK&sugg=%C4%91%E1%BB%93ng%20h%E1%BB%93%20nam%20ch%E1%BB%91ng%20n%C6%B0%E1%BB%9Bc_5_1".format(page + 1), filename='./lazada-dongho2.csv')
    #crawl("https://www.sendo.vn/tim-kiem?p=10&q=%C4%91%E1%BB%93ng%20h%E1%BB%93&sortType=norder_30_desc", filename='./sendo-dongho6.csv')
