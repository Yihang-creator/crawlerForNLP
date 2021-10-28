# -*- coding = utf-8 -*-
# Author: Yihang He
# @Time : 2021/9/15 11:37 PM
# @Author : Yihang He
# @File : jianshu.py
# @Software: PyCharm





# -*- coding = utf-8 -*-
# Author: Yihang He
# @Time : 2021/8/5 6:50 PM
# @Author : Yihang He
# @File : tieba.py
# @Software: PyCharm

from selenium import webdriver
import pandas as pd
import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def generate_urls():

    list = driver.find_elements_by_css_selector("a.title")
    linkset = set()
    for item in list:
        try :
            link = item.get_attribute("href")
            linkset.add(link)
        except:
            continue
    print(linkset)
    return linkset

def generate_comments_one_page(url):
        # title author time content url num
        import time

        driver.get(url)

        try:
            title = driver.find_element_by_css_selector("h1._1RuRku").text
        except:
            title = ""
            print("title missing")

        try :
            author = driver.find_element_by_css_selector(".FxYr8x a").text
        except:
            author = ""
            print("author missing")

        try:
            time = driver.find_element_by_css_selector("time").text
        except:
            time = ""
            print("time missing")

        try:
            content = driver.find_element_by_css_selector("article").text
        except:
            content = ""
            print("content missing")

        try:
            support = driver.find_element_by_css_selector("span._1LOh_5").text
        except:
            support = ""
            print("support missing")


        comment = [title, author, time, content, url, support]
        return comment


def write_csv(datalist, path):
    headers=["title","author","time","content","url","num"]
    test = pd.DataFrame(columns=headers,data=datalist)
    test.to_csv(path, encoding='utf-8-sig')
    return test


urls = set()
driver = webdriver.Chrome(r'/usr/local/bin/chromedriver')
comments = []




def one_time_crawl():  # 利用set去重
    # 访问搜索页
    driver.get("https://www.jianshu.com/search?q=%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD&page=1&type=note")
    for i in range(0,101):
        # 等待页面加载成功
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.title")))
        # 最近三天 按钮
        driver.find_element_by_css_selector("svg").click()
        three_day_element = driver.find_element_by_css_selector("li.v-select-options-item:nth-of-type(4)")
        ActionChains(driver).move_to_element(three_day_element).click()
        # 读取当前页文章url
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.title")))
        urls.union(generate_urls())

        time.sleep(0.5)
    return

while (len(urls) < 3000):
    one_time_crawl()
    print("one time")
    time.sleep(0.5)

print(urls)

for url in urls:
    comments.append(generate_comments_one_page(url))
    time.sleep(0.5)

path = r'./data/jianshu_second_time.csv'
write_csv(comments, path)
driver.quit()