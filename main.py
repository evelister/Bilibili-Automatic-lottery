import requests
import re
import time

class Bili():
    def __init__(self):
        self.sendurl = 'http://api.vc.bilibili.com/dynamic_repost/v1/dynamic_repost/repost'
        self.followurl = 'http://api.bilibili.com/x/relation/modify'

        self.uid = 398615483
        self.crsf = '0b0aaa23e07c010d59763fbd9022bb56' #d157c4892cd8f8d9563b3f0c2c049fcf
        self.cookie = {'Cookie': 'LIVE_BUVID=AUTO2515384570455126; sid=ibe7qbit; rpdid=oloqxswlpodoskqpxlmqw; im_notify_type_5104114=0; fts=1538549006; UM_distinctid=1663f7ddb6514c-0b534ebf22e637-5701631-144000-1663f7ddb66143; im_local_unread_5104114=0; CURRENT_FNVAL=16; _uuid=C2CBE326-E776-D6C2-0877-5A4203C1658729296infoc; buvid3=D0DAD267-4C0A-4BE7-B5A0-11C995A8389124331infoc; LIVE_PLAYER_TYPE=1; arrange=matrix; CNZZDATA1271442956=552419302-1544848601-%7C1544848601; Hm_lvt_bfc6c23974fbad0bbfed25f88a973fb0=1546339676,1546866100,1547027130; Hm_lvt_f5df380d5163c1cc4823c8d33ec5fa49=1544849464,1546339676,1546866100,1547027130; stardustvideo=1; im_seqno_5104114=3751; gr_user_id=2a165bc2-cecc-42d4-adcf-d534b24a66fb; grwng_uid=3ad44073-7215-47a6-bb76-b9ed46b7051f; finger=17c9e5f5; im_seqno_398615483=10; im_local_unread_398615483=0; CURRENT_QUALITY=80; DedeUserID=398615483; DedeUserID__ckMd5=2cb9ea3da8ccc46a; SESSDATA=954f3ad7%2C1554108719%2C462a6d31; bili_jct=0b0aaa23e07c010d59763fbd9022bb56; _dfcaptcha=3b5a8f04e4adbba104c156f8223d2070; CNZZDATA2724999=cnzz_eid%3D2088997712-1538661200-https%253A%252F%252Fwww.bilibili.com%252F%26ntime%3D1551606792; bp_t_offset_398615483=226653232461413960; Hm_lvt_8a6e55dbd2870f0f5bc9194cddf32a02=1551610735,1551610839,1551610846,1551610993; Hm_lpvt_8a6e55dbd2870f0f5bc9194cddf32a02=1551610993'}
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}

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
    host_uids = [387594603, 23131813, 123469889, 397155220]
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