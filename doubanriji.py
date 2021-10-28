# -*- coding = utf-8 -*-
# Author: Yihang He
# @Time : 2021/8/5 12:10 AM
# @Author : Yihang He
# @File : doubanriji.py
# @Software: PyCharm


from selenium import webdriver
import time
from bs4 import BeautifulSoup
import pandas as pd
import re

driver = webdriver.Chrome(r'/usr/local/bin/chromedriver')
driver.get('https://www.douban.com/')
# iframe = driver.find_element_by_tag_name("iframe")
# driver.switch_to.frame(iframe)
# driver.find_element_by_class_name('account-tab-account').click()
# driver.find_element_by_id('username').send_keys(username)
# driver.find_element_by_id('password').send_keys(password)
# driver.find_element_by_class_name('btn-account').click()
time.sleep(20)


def generate_urls():
    """
    获取人工智能搜索页的豆瓣日记信息
    """
    urls = ["https://www.douban.com/search?cat=1015&q=%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD"]
    template = 'https://www.douban.com/j/search?q=%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD&start={param}&cat=1015'

    for p in range(1, 101):
        url = template.format(param=p * 20)
        urls.append(url)

    return urls


def generate_hrefs(urls):
    import time, datetime

    hrefs = []
    for url in urls:
        driver.get(url)
        search_window = driver.current_window_handle
        pageContent = driver.page_source
        time.sleep(4)

        pattern = re.compile('sid: (\d+)', re.S)
        results = re.findall(pattern, pageContent)

        for line in results:
            href = "https://www.douban.com/note/" + line
            hrefs.append(href)

    return hrefs

this_year = time.strptime("2020-08-08 00:00:00","%Y-%m-%d %H:%M:%S")

def generate_articles(hrefs):
    import time, datetime

    articles = []
    for href in hrefs:
        print(href)

        driver.get(href)

        search_window = driver.current_window_handle
        pageSource = driver.page_source
        time.sleep(4)

        try :
            soup = BeautifulSoup(pageSource)
            title_author = soup.find("div", attrs={"class": "note-header note-header-container"})
            # 文章标题
            title = title_author.find("h1", attrs={"": ""}).text
            # 文章作者
            author = title_author.find("a", attrs={"class": "note-author"}).text
            # 文章发布时间
            date = title_author.find("span", attrs={"class": "pub-date"}).text
            publish_time = time.strptime(date, "%Y-%m-%d %H:%M:%S")
            if publish_time < this_year:
                continue

        # 文章正文
            res = soup.find("div", attrs={"id": "link-report"})
            note = res.find("div", attrs={"class": "note"})
            txt = note.text

        except :
            continue


        # 点赞数
        try:
            support = soup.find("span", attrs={"class": "react-num"}).text

        except:
            support = ""
        # 标签
        try:
            topics = soup.find('div', attrs={"class": "mod-tags"})
            topics_a = topics.find_all("a")

            tags = []
            for topic_a in topics_a:
                topic = topic_a.text
                tags.append(topic)

            tag = " ".join(tags)

        except:
            tag = ""

        # 评论信息
        try:
            divs = soup.find_all("div", attrs={"class": "comment-content"})
            meta_headers = soup.find_all("div", attrs={"class": "meta-header"})

            comments = []
            for line1, line2 in zip(divs, meta_headers):
                span = line1.find("span")
                review = span.text
                a = line2.find_all("a", attrs={"title": re.compile(".*")})
                comment_user = a[0].text
                comment_time = line2.find("time").text
                comment = [comment_user, review, comment_time]
                comments.append(comment)

        except:
            comments = []

        article = [href, title, author, date, txt, support, tag, comments]
        articles.append(article)

    return articles


def write_csv(datalist, path):
    headers=["链接","标题","作者","日期","文本","点赞","标签","评论"]
    test = pd.DataFrame(columns=headers,data=datalist)
    test.to_csv(path, encoding='utf-8-sig')
    return test


urls = generate_urls()
hrefs = generate_hrefs(urls)
articles = generate_articles(hrefs)
path = r'./douban.csv'

write_csv(articles, path)