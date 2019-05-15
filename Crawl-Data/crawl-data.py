import sys
import time

import pandas as pd
from selenium import webdriver

# add path that containing chromedriver.exe
sys.path.append('../chromedriver.exe')


# Hide Chrome browser open new window


def crawl_conversation_of_item(link_of_item):
    print("Crawl conversation in {0}".format(link_of_item))
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    # Create a driver to perform actions in website as: crawl,event
    browser = webdriver.Chrome(options=options)
    #
    browser.get(link_of_item)
    browser.implicitly_wait(20)

    # init variables
    name_of_item = ""
    # find in html element that containing question, answer and get text
    questions = []
    answers = []
    page = 1
    try:
        # find in html element that containing name of item
        name_element = browser.find_element_by_xpath("//div[@class='rowtop']/h1")
        name_of_item = name_element.text

        while (1):
            element_ques = browser.find_elements_by_xpath(
                "//ul[@class = 'listcomment']/li/div[@class = 'listreply']/../div[@class = 'question']")
            element_ans = browser.find_elements_by_xpath(
                "//ul[@class = 'listcomment']/li/div[@class = 'listreply']/div[1]/div[@class='cont']")
            for ques, ans in zip(element_ques, element_ans):
                time.sleep(0.2)
                question = ques.text.replace('\n', ' ')
                answer = ans.text.replace('\n', ' ')
                if (question not in questions):
                    questions.append(question)
                    answers.append(answer)
                    print("{0}: Page {1}: {2}:------:{3}".format(name_of_item, page, question, answer))
                pass
            # click next page
            xpath = "//div[@class = 'pagcomment']/a[contains(@onclick,'listcomment') and @title = 'trang {0}']".format(
                page + 1)
            elm = browser.find_element_by_xpath(xpath)
            elm.click()
            time.sleep(1)
            page = page + 1
        pass
    except:
        print("---------------------------End in {0}--------------------------".format(page))
        pass

    print("Crawnl in {0} get {1} pair data".format(name_of_item, len(questions)))
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
    datalist[['Link', 'Name', 'Question', 'Answer']].to_csv(filename,index=False, encoding='utf-8-sig')
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
            name, questions, answers = crawl_conversation_of_item(lik)
            save_to_csv(lik, name, questions, answers, filename)
    else:
        isFound = False
        for lik, i in zip(links, range(len(links))):
            if lik.endswith(continued_link):
                isFound = True
                print("Found")
            if isFound:
                print("{}/{}".format(i, len(links)))
                name, questions, answers = crawl_conversation_of_item(lik)
                save_to_csv(lik, name, questions, answers, filename)

def crawl_conversation_singer_item(link, filename):
    name, questions, answers = crawl_conversation_of_item(link)
    save_to_csv(link, name, questions, answers, filename)
if __name__ == '__main__':
    crawl("https://www.thegioididong.com/dong-ho-thong-minh", "./question-answer-tgdd-dong-ho.csv", continued_link="dong-ho-thong-minh/samsung-galaxy-watch-46mm")
    #crawl_conversation_singer_item("https://www.thegioididong.com/dong-ho-thong-minh/apple-watch-s4-gps-44mm-vien-nhom-day-vai-hong","./question-answer-tgdd-dong-ho.csv")
