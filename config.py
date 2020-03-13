'''

提供UA和IP代理

'''
import my_fake_useragent  # 这个超好用my_fake_useragent.UserAgent().random()随机返回一个UA
import requests


class Config:
    def __init__(self):
        pass

    def getheaders(self):
        return {'user-agent': my_fake_useragent.UserAgent().random()}

    def getproxies(self):
        # url = 'https://api.xiaoxiangdaili.com/ip/get?appKey=530595293713289216&appSecret=hISgmKhy&cnt=&wt=text&method=http&city=&province='#小象代理
        url = 'http://dps.kdlapi.com/api/getdps/?orderid=908407943957242&num=1&pt=1&sep=1'  # 快代理
        headers = {'User-Agent': my_fake_useragent.UserAgent().random()}
        response = requests.get(url=url, headers=headers)
        proxy = response.content.decode('utf-8')
        print("代理IP为：" + proxy)
        proxies = {
            'http': 'http://' + proxy,
            'https': 'https://' + proxy,
        }
        return proxies


# config=Config()
# print(config.getproxy())
# print(config.getua())
print(Config().getheaders())
