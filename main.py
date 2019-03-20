import requests
import re
import time

class Bili():
    def __init__(self):
        self.sendurl = 'http://api.vc.bilibili.com/dynamic_repost/v1/dynamic_repost/repost'
        self.followurl = 'http://api.bilibili.com/x/relation/modify'

        self.uid = 这里是uid
        self.crsf = 这里是crsf_token
        self.cookie = {'Cookie': '这里是cookie'}
        self.header = {'User-Agent': '这里是user-agent'}

    def get(self):
        res = requests.get(geturl1, cookies=self.cookie, headers=self.header)
        cards = res.json().get('data').get('cards')
        for card in cards:
            card1 = card.get('card')
            pattern = re.compile('"orig_dy_id": (.*?), "pre_dy_id.*?uid": (.*?), "uname', re.S)
            items = re.findall(pattern, card1)
            for item in items:
                yield {
                    'dynamic_id': item[0],
                    'uid': item[1]
                }

    def follow(self):
        data = {
            'fid': item['uid'],
            'act': 1,
            're_src': 11,
            'jsonp': 'jsonp',
            'csrf': self.crsf
        }
        requests.post(self.followurl, data=data, cookies=self.cookie, headers=self.header)

    def send(self):
        data = {
            'uid': self.uid,
            'dynamic_id': item['dynamic_id'],
            'content': '//@飞碟说 @天天卡牌 @某幻君 :转发动态',
            'at_uids': '5581898,10462362,1577804',
            'ctrl': '[{"data":"5581898","location":2,"length":4,"type":1},{"data":"10462362","location":7,"length":5,"type":1},{"data":"1577804","location":13,"length":4,"type":1}]',
            'csrf_token': self.crsf
        }
        requests.post(self.sendurl, data=data, cookies=self.cookie, headers=self.header)

if __name__ == "__main__":
    host_uids = [387594603, 23131813, 123469889, 397155220]#这是四个抽奖up，可以修改
    geturl = 'http://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid=%s&offset_dynamic_id=0'

    bili = Bili()
    for host_uid in host_uids:
        i = 0
        geturl1 = geturl % (host_uid)
        for item in bili.get():
            bili.follow()
            bili.send()
            i = i + 1
            if i % 10 == 0:
                time.sleep(120)
        time.sleep(120)
        print(i)
