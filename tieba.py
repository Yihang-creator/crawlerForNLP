# -*- coding = utf-8 -*-
# Author: Yihang He
# @Time : 2021/8/5 6:50 PM
# @Author : Yihang He
# @File : tieba.py
# @Software: PyCharm

from selenium import webdriver
import pandas as pd
import time


def generate_urls():

    list = driver.find_elements_by_xpath("//a[contains(@class,'j_th_tit')]")
    linkList = []
    for item in list:
        try :
            link = item.get_attribute("href")
            linkList.append(link)
        except:
            continue


    return linkList

def generate_comments(linkList):
    import time

    for href in linkList:
        driver.get(href)
        last_page = 1
        try:
            buttons = driver.find_elements_by_xpath("//li[@class='l_pager pager_theme_4 pb_list_pager']/a")
            last_url = buttons[-1].get_attribute("href")
            if isinstance(last_url, str):
                last_page = int(last_url[-1])
        except:
            print("no buttons")  # continue

        for i in range(1, last_page + 1):
            generate_comments_one_page(href + "?pn=" + str(i))

def generate_comments_one_page(url):
        import time

        driver.get(url)
        total_height = int(driver.execute_script("return document.body.scrollHeight"))
        try :
            topic = driver.find_element_by_xpath("//h1[contains(@class,'core_title_txt')]").text
        except:
            topic = ""

        for i in range(1, total_height, 100):
            driver.execute_script("window.scrollTo(0, {});".format(i))


        list_items = driver.find_elements_by_xpath("//div[contains(@class,'l_post j_l_post l_post_bright')]")
        for item in list_items:
            author = ""
            comment_entry = ""
            comments_responses = []
            time = ""
            try:
                author = item.find_element_by_css_selector("a[class*='p_author_name']").text
            except:
                print("no authors")

            try:
                comment_entry = item.find_element_by_css_selector("div[class='d_post_content j_d_post_content  clearfix']").text
            except:
                print("no main comments")

            try:
                time = item.find_element_by_css_selector(".p_tail > li:nth-of-type(2) > span").text
            except:
                print("no time")

            try:
                comments_responses = item.find_elements_by_css_selector("span[class='lzl_content_main']")
                comments_responses = list(map(lambda e: e.text, comments_responses))

            except:
                print("no comments")

            comment = [url, topic, author, time, comment_entry, comments_responses]
            comments.append(comment)
        return 0


def write_csv(datalist, path):
    headers=["链接","标题","作者","日期","评论","回复"]
    test = pd.DataFrame(columns=headers,data=datalist)
    test.to_csv(path, encoding='utf-8-sig')
    return test


urls = []
driver = webdriver.Chrome(r'/usr/local/bin/chromedriver')
comments = []
# driver.get("https://tieba.baidu.com/")
# time.sleep(60)

for i in range(0, 4000, 50):
    driver.get("https://tieba.baidu.com/f?kw=%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD&ie=utf-8&pn=" + str(i))
    if (i == 0):
        time.sleep(60)
    urls.extend(generate_urls())
    time.sleep(1)

print(urls)


generate_comments(urls)
time.sleep(2)
path = r'./tieba022.csv'
write_csv(comments, path)
driver.quit()