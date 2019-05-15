import sys
import time
import re
import os

import pandas as pd
from selenium import webdriver

# add path that containing chromedriver.exe
sys.path.append('../chromedriver.exe')


# Hide Chrome browser open new window

def get_number_qsaw_link():
    link = []
    link_little = []
    options = webdriver.ChromeOptions()
    browser = webdriver.Chrome(options=options)

    with open('./test.txt') as f:
        for line in f:
            x = 0
            line = line.rstrip()
            print(line)
            browser.get(line)
            browser.implicitly_wait(10)
            name_element_filter = browser.find_element_by_css_selector("#module_product_qna > div.mod-title > div")
            print(name_element_filter.text)
            numbers = re.findall('\d+',name_element_filter.text)
            numbers = map(int,numbers)
            x = max(numbers)
            print(x)
            if x > 24:
                print(line)
                link.append(line)
            else:
                print(line)
                link_little.append(line)
    file = open('linkmany.txt','w')
    for x in link:
        file.write(x+'\n')
    file.close()
    file2 = open('link_little.txt','w')
    for e in link_little:
        file2.write(e+'\n')
    file.close()
                  
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
if __name__ == '__main__':
    #get_number_qsaw_link()
    # page = 1
    # for page in range(50):
    #crawl("https://www.lazada.vn/catalog/?_keyori=ss&from=search_history&page={0}&q=%C4%91%E1%BB%93ng%20h%E1%BB%93&spm=a2o4n.home.search.1.8e71e182PNpChe&sugg=%C4%91%E1%BB%93ng%20h%E1%BB%93_0_1".format(page + 1), filename='./lazada-dongho.csv')
    crawl_singer_item("https://www.lazada.vn/products/dong-ho-nam-cuena-14-mat-den-day-da-sang-trong-tang-ngay-1-vong-phong-thuy-1-pin-du-phong-i238119677-s358904571.html?search=1", filename='./lazada-dongho-question-answer1.csv')
