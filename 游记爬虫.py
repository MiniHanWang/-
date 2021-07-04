# -*- coding: utf-8 -*-
import random
import time
import bs4
import os
import csv
import requests
import datetime
import selenium
import codecs
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from requests.adapters import HTTPAdapter
from requests import session

class jingjinji:

    def __init__(self):
        pass

    #全局变量
    searchBase = 'http://www.mafengwo.cn/search/q.php?q={}'#搜索页面
    filePath = ''# 文件名
    maxPageCount = 800# 预制最大页数，用于提高效率
    maxPastCount = 100000# 预制最大游记数量
    pastCount = 0
    startCount = 5416#从哪儿开始
    startPage = 1#从第几页开始

    #时间
    dateMin = datetime.datetime.strptime('2020-6-1', '%Y-%m-%d')
    dateMax = datetime.datetime.strptime('2021-6-1', '%Y-%m-%d')

    #requests请求头
    header = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3",
        "Cookie": "mfw_uuid=5dd27340-0f45-ff42-1a3a-0744fe7a90b5; "
                  "oad_n=a%3A3%3A%7Bs%3A3%3A%22oid%22%3Bi%3A1029%3Bs%3A2%3A%22dm%22%3Bs%3A15%3A%22www.mafengwo.cn%22"
                  "%3Bs%3A2%3A%22ft%22%3Bs%3A19%3A%222019-11-18+18%3A32%3A32%22%3B%7D; __mfwc=direct; "
                  "uva=s%3A92%3A%22a%3A3%3A%7Bs%3A2%3A%22lt%22%3Bi%3A1574073153%3Bs%3A10%3A%22last_refer%22%3Bs%3A24"
                  "%3A%22https%3A%2F%2Fwww.mafengwo.cn%2F%22%3Bs%3A5%3A%22rhost%22%3BN%3B%7D%22%3B; "
                  "__mfwurd=a%3A3%3A%7Bs%3A6%3A%22f_time%22%3Bi%3A1574073153%3Bs%3A9%3A%22f_rdomain%22%3Bs%3A15%3A"
                  "%22www.mafengwo.cn%22%3Bs%3A6%3A%22f_host%22%3Bs%3A3%3A%22www%22%3B%7D; "
                  "__mfwuuid=5dd27340-0f45-ff42-1a3a-0744fe7a90b5; "
                  "UM_distinctid=16e7e123fef4e1-02c4731bcb3d0e-14291003-1fa400-16e7e123ff06e1; "
                  "__mfwa=1574073154592.41083.3.1574077524550.1574171715575; __mfwlv=1574171715; __mfwvn=2; "
                  "__jsluid_h=9ef4c7cb671f9afa2aad419a179a1647; __omc_chl=; __omc_r=; "
                  "PHPSESSID=clmadiuq6sha7va0elf73rlam5; Hm_lvt_8288b2ed37e5bc9b4c9f7008798d2de0=1574073155,"
                  "1574171716,1574173100; CNZZDATA30065558=cnzz_eid%3D2060055507-1574071549-https%253A%252F%252Fwww"
                  ".mafengwo.cn%252F%26ntime%3D1574173216; __mfwb=7fcff7a4dc01.16.direct; __mfwlt=1574174200; "
                  "Hm_lpvt_8288b2ed37e5bc9b4c9f7008798d2de0=1574174201; "
                  "__jsl_clearance=1574174686.567|0|ieQmVq2XUoUQcN%2F3QLUUQ5Q5DN0%3D",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 "
                      "Safari/537.36 "
    }
    #selenium的请求头
    def getDriver(self):#为selenium设置请求头
        options = webdriver.ChromeOptions()
        options.add_argument('User-Agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"')
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("headless")# 不打开网页
        # options.add_argument("--no-sandbox") # linux only
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        driver = webdriver.Chrome(options=options)
        driver.execute_cdp_cmd("Network.enable", {})
        driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browserClientA"}})
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    })
                """
        })
        return driver
        pass


    # 滚动加载
    def roll(self, num, browser):
        for i in range(num):
            ActionChains(browser).send_keys(Keys.PAGE_DOWN).perform()
        pass


    def getPage(self, url):
        try:
            s = session()
            s.mount('http://', HTTPAdapter(max_retries=99))#重试99次
            s.mount('https://', HTTPAdapter(max_retries=99))
            rqs = s.request("GET", url=url, timeout=15, headers=self.header)
        except Exception as e:
            soup = bs4.BeautifulSoup(rqs.text, 'lxml')
            print("进入网页失败！" + soup.text.title())
        else:
            return rqs
        pass


    def getPageText(self, url):
        rqs = self.getPage(url)
        text = rqs.text
        rqs.close()#关闭链接节省内存
        return text
        pass


    def search(self, name):# 查找并返回相应的游记结果
        page = self.getPageText(self.searchBase.format(name))#搜索结果页面文本
        soup = bs4.BeautifulSoup(page, 'lxml')
        searchMddWrap = soup.find('div', class_='search-mdd-wrap')

        url = searchMddWrap.find('a').get('href')
        page0 = self.getPage(url)#获取首页头图文本
        url = page0.url[-10:-5]
        url = "http://www.mafengwo.cn/yj/" + url + '/2-0-1.html'

        return url
        pass


    def getPostList(self, url, name):
        postCount = 0
        needCount = 0
        page = self.getPageText(url)
        soup = bs4.BeautifulSoup(page, 'lxml')
        pagebar = soup.find('span', class_='count')
        count = int(pagebar.find('span').text)
        url = url.replace('2-0-1.html', '') + '2-0-{}.html'
        print(url)
        url_list = []
        print('共{}页'.format(count))
        count = count if count < self.maxPageCount else self.maxPageCount
        print('取{}页'.format(count))
        for i in range(count):

            # if i + 1 < self.startPage: continue # 测试用，无必要时撤销这一行###############################################

            print('第{}页扫描'.format(i + 1))
            page = self.getPageText(url.format(str(i + 1)))
            soup = bs4.BeautifulSoup(page, 'lxml')
            postList = soup.find_all('div', class_='post-cover')
            for post in postList:
                postCount += 1
                if i + 1 >= self.startPage:
                    needCount += 1
                a = post.find('a')
                url_list.append("http://www.mafengwo.cn" + a.get("href"))
        print('游记列表扫描完毕,本次爬取共{}项'.format(postCount))
        print('需要{}项'.format(needCount))
        print('正在写入list数据')
        file = open(name + 'UrlList.txt', mode='w', encoding='utf-8')
        for item in url_list:
            file.write(item+'\n')
        file.close()
        print('list写入完成')
        return url_list
        pass

    def getPostListByFile(self, name):
        path = name+'UrlList.txt'
        if not os.path.isfile(path):
            return None
        file = open(path, mode='r', encoding='utf-8')
        print(path)
        list_ = file.readlines()
        file.close()
        return list_

    # 加载游记
    def getPost(self, url):

        timer = time.process_time()
        path = url[-13:-5]

        #这里动态加载太多了，直接采用selenium
        browser = self.getDriver()
        browser.get(url)

        #以下代码是在应付这个破网站的动态加载
        while 1:
            try:
                browser.find_element_by_class_name('vc_article')
                break
            except Exception as e:
                if time.process_time() - timer > 6:# 超过60秒则访问超时
                    print('访问超时！')
                    return '访问超时', '访问超时', '2021-6-1', '访问超时'
                continue
        #滚动加载
        while browser.find_element_by_class_name('mfw-toolbar').get_attribute('style') == 'display: block;':
            self.roll(100, browser)
            for i in range(64):
                if browser.find_element_by_class_name('mfw-toolbar').get_attribute('style') != 'display: block;':
                    time.sleep(0.1)
                    self.roll(1, browser)
                else:
                    break
            pass
        pass
        # 获取文章信息
        page = browser.page_source
        soup = bs4.BeautifulSoup(page, 'lxml')
        # 日期
        dateStr = soup.find('span', class_='time').text
        dateStr = dateStr[0:10]
        date = datetime.datetime.strptime(dateStr, '%Y-%m-%d')
        # 标题
        title = soup.find('h1', class_='headtext').text
        # 作者
        author = soup.find('a', class_='per_name').text
        author = author.replace('\n', '').replace('  ', '')

        if date > self.dateMax or date < self.dateMin: # 如果不在规定日期内的话返回
            return author, title, dateStr, 'none'

        #输出游记的文字内容
        text = ''
        article = soup.find_all('p', class_='_j_note_content _j_seqitem')
        for p in article:
            text += p.text.replace(' ', '').replace('\n', '')
            if time.process_time() - timer > 60:
                print('访问超时！')
                return author, title, dateStr, '访问超时'
            pass
        #输出
        data = (author, title, dateStr, text)
        # out = open('yj/' + path + '.csv', mode='w', encoding='gbk')
        # writer = csv.writer(out)
        # for i in data:
        #     writer.writerow(i)
        # out = open('yj/' + path + '.txt', mode='a', encoding="utf-8")
        # out.write(text)
        # out.close()

        browser.close()

        return data
        pass

    # 爬虫
    def spider(self, name):
        # 打开文件
        path = 'yj/' + name + '.csv'
        if self.startCount > 1:
            out = open('path', mode='w')
            out.write('')#清空文件
        out = open(path, mode='a', encoding='gbk', errors='ignore', newline='')  # 消除了错误格式的影响以及空行
        writer = csv.writer(out)

        self.pastCount = 0
        print('{}游记数据爬取中'.format(name))
        url = self.search(name)
        print(url)

        url_list = self.getPostListByFile(name)
        if url_list is None:
            url_list = self.getPostList(url, name)

        for item in url_list:
            self.pastCount += 1
            if self.pastCount < self.startCount:
                continue
            print('#'+str(self.pastCount))
            print('扫描页面{}'.format(item))
            try:
                d = self.getPost(item)
            except Exception as e:
                print("ERROR:网页打开错误")
                print(e)
            pass
            date = datetime.datetime.strptime(d[2], '%Y-%m-%d')
            print(d[1])
            print(date)
            if self.dateMax >= date >= self.dateMin:
                print('在规定时间范围内，开始写入数据')
                writer.writerow(d)
                print('数据写入结束')
            elif date < self.dateMin:
                break

            if self.pastCount > self.maxPastCount:
                break

            # if date < datetime.datetime.strptime('2021-5-7', '%Y-%m-%d'): break # 测试用，无必要是撤销###################

            print()
            pass
        out.close()
        print(name+'数据写入结束，爬取结束')
        print()
        pass

    def searchID(self, name, ID):
        #寻找相应ID的项目编号
        url = self.search(name)
        print('查找'+name+' ID:'+ID)
        print(url)
        url_list = self.getPostList(url)
        count = 0
        for item in url_list:
            count += 1
            if item[-13:-5] == ID:
                break
            pass
        return count
        pass

    def main(self):
        self.spider('北京')
        self.startCount = 1
        pass
    pass

if __name__ == '__main__':
    obj = jingjinji()
    obj.main()
    print(obj)
