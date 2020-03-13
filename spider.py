import requests
import threading
import re
import time
from lxml import etree
from DoubanSpider.config import Config
from DoubanSpider.db import Db


class DoubanSpider():
    def __init__(self):
        self.headers = Config().getheaders()
        self.proxies = Config().getproxies()
        self.db = Db()
        self.lock = threading.Lock()
        self.stop = False

    def inittagurl(self):
        url = 'https://book.douban.com/tag/?view=type&icn=index-sorttags-all'
        response = self.gethtml(url)
        names, urls = self.parsetag(response.content.decode('utf-8'))
        for i in range(0, len(names)):
            self.db.taginsert(name=names[i], url="https://book.douban.com" + urls[i])

    def gethtml(self, url):
        try:
            response = requests.get(url=url, headers=self.headers, proxies=self.proxies)
            print("请求成功：" + url)
            # return response
        except requests.exceptions.ProxyError:  # 还可能有其他异常未处理
            self.lock.acquire()
            print("代理异常，更换代理并重新发起请求")
            self.proxies = Config().getproxies()
            print("顺带更换一下UA，反正没成本")
            self.headers = Config().getheaders()
            self.lock.release()
            response = self.gethtml(url)
        except requests.exceptions.InvalidHeader:
            self.lock.acquire()
            print("UA异常，更换新的UA")
            self.headers = Config().getheaders()
            self.lock.release()
            response = self.gethtml(url)
        return response

    def parsetag(self, html):
        html = etree.HTML(html)
        urls = html.xpath("//table[@class='tagCol']/tbody/tr/td/a/@href")  # list
        names = html.xpath("//table[@class='tagCol']/tbody/tr/td/a/text()")
        return names, urls

    def gettagurl(self):  # 从数据库中获取所有tagurl
        names, urls = self.db.tagquery()
        return urls

    def parsepage(self, html):
        html = etree.HTML(html)
        names = html.xpath("//li[@class='subject-item']/div[@class='info']/h2/a/@title")
        urls = html.xpath("//li[@class='subject-item']/div[@class='info']/h2/a/@href")
        return names, urls

    def getpageurl(self, url):
        for i in range(0, 110):
            pageurl = url + "?start=" + str(i * 20) + "&type=T"
            response = self.gethtml(pageurl)
            names, urls = self.parsepage(response.content.decode('utf-8'))
            for k in range(0, len(names)):
                self.lock.acquire()
                self.db.bookinsert(name=names[k], url=urls[k])
                self.lock.release()
                # print(names[k] + ":" + urls[k])
            if len(names) == 0:
                print("查找到第" + str(i) + "页就停止了")
                break

    def getelement(self, elements):
        if len(elements) > 0:
            return elements[0]
        return ""

    def parsebook(self, htmll):
        html = etree.HTML(htmll)
        name = self.getelement(html.xpath("//*[@id='wrapper']/h1/span/text()"))
        # name = html.xpath("//*[@id='wrapper']/h1/span/text()")[0]  # 书名
        auth = self.getelement(html.xpath("//*[@id='info']/a/text()"))
        # auth = html.xpath("//*[@id='info']/a/text()")  # 作者
        auth = str(auth)
        auth = auth.strip().replace(" ", "").replace("\n", "")
        press = self.getelement(re.findall(r"<span.*?出版社:</span>\s*(.*?)<br", htmll))
        # press = re.findall(r"<span.*?出版社:</span>\s*(.*?)<br", htmll)[0]  # 出版社
        time = self.getelement(re.findall('''<span.*?出版年:</span>\s*([0-9\-]+)<br''', htmll))
        # time = re.findall('''<span.*?出版年:</span>\s*([0-9\-]+)<br''', htmll)[0]  # 出版时间
        pages = self.getelement(re.findall('''<span.*?页数:</span>\s*([0-9]+)<br''', htmll))
        # pages = re.findall('''<span.*?页数:</span>\s*([0-9]+)<br''', htmll)[0]  # 页数
        price = self.getelement(re.findall('''<span.*?定价:</span>.*?([0-9\.]+)元?<br''', htmll))
        # price = re.findall('''<span.*?定价:</span>.*?([0-9\.]+)元?<br''', htmll)[0]  # 定价
        ISBN = self.getelement(re.findall('''<span.*?ISBN:</span>.*?([0-9]+)<br''', htmll))
        # ISBN = re.findall('''<span.*?ISBN:</span>.*?([0-9]+)<br''', htmll)[0]
        score = self.getelement(html.xpath("//*[@id='interest_sectl']/div/div[2]/strong/text()"))
        # score = html.xpath("//*[@id='interest_sectl']/div/div[2]/strong/text()")[0]  # 评分
        score = str(score)
        score = score.strip()
        assessor = self.getelement(html.xpath("//*[@id='interest_sectl']/div/div[2]/div/div[2]/span/a/span/text()"))
        # assessor = html.xpath("//*[@id='interest_sectl']/div/div[2]/div/div[2]/span/a/span/text()")[0]  # 评论员数量
        # print(name, auth, press, time, pages, price, ISBN, score, assessor)
        return name, auth, press, time, pages, price, ISBN, score, assessor

    def getbook(self, url):
        response = self.gethtml(url)
        names, urls = self.parsepage(response.content.decode('utf-8'))  # 书籍名称和链接
        if len(urls) is 0:
            self.lock.acquire()
            self.stop = True
            self.lock.release()
            return
        for i in range(0, len(urls)):
            # print(names[i],urls[i])
            response = self.gethtml(urls[i])  # 书名，链接，id，出版商，各种信息全部入库
            name, auth, press, time, pages, price, ISBN, score, assessor = self.parsebook(
                response.content.decode('utf-8'))
            self.lock.acquire()
            self.db.bookinsert(name=name, auth=auth, press=press, time=time, pages=pages, price=price, ISBN=ISBN,
                               score=score, assessor=assessor, url=urls[i])
            self.lock.release()

    def crawler(self):
        urls = self.gettagurl()
        for i in range(0, len(urls)):  # 第i个标签
            print("进行到第"+str(i)+"个标签")
            for j in range(0, 110):  # 第j页
                time.sleep(5)
                url = urls[i] + "?start=" + str(j * 20) + "&type=T"
                threading.Thread(target=self.getbook, args=(url,)).start()
                self.lock.acquire()
                if self.stop is True:
                    self.stop = False
                    self.lock.release()
                    print("到第" + str(j) + "页为止")
                    break
                else:
                    self.lock.release()


test = DoubanSpider()
test.crawler()

'''
爬的太快了，可以用QUEUE控制一下线程数量


发现的待捕获异常
requests.exceptions.TooManyRedirects: Exceeded 30 redirects.

'''
