#coding=utf8

import hashlib
import json
import random

import requests

class Baidu_Translate:
    def __init__(self, words):
        self.url = "https://fanyi-api.baidu.com/api/trans/vip/translate"
        self.q = words
        self.fromLang = 'auto'
        self.toLang = 'zh'
        self.appid = '20181108000231643'
        self.secretKey = 'ZRvY04W6YyMOnUMHXbub'
        self.salt = str(random.randint(32768, 65536))
        self.sign = self.appid + self.q + self.salt + self.secretKey
        m1 = hashlib.md5()
        m1.update(self.sign.encode('utf-8'))
        self.sign = m1.hexdigest()
    def translate(self):
        url = self.url
        data = {
            'q' : self.q,
            'from' : self.fromLang,
            'to' : self.toLang,
            'appid' : self.appid,
            'salt' : self.salt,
            'sign' : self.sign
        }
        resp = requests.post(url=url,data=data)
        # print(resp.status_code)
        trans_result = json.loads(resp.content).get('trans_result')[0].get('dst')
        return trans_result

if(__name__ == '__main__'):
    w = "what a beautiful girl"
    t = Baidu_Translate(w)
    print(t.translate())