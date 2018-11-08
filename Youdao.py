#coding=utf8
import hashlib
import json
import random
import time

import requests


class Youdao_translate:
    def __init__(self, q = ''):
        self.method = 'Youdao'
        self.url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        # 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&sessionFrom='
        self.q = q
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'OUTFOX_SEARCH_USER_ID=2134433087@10.168.8.63; OUTFOX_SEARCH_USER_ID_NCOO=1169082631.2327397; UM_distinctid=166e6fced9678d-09999fb351adce-24414032-1fa400-166e6fced981232; JSESSIONID=aaa8oUTo3fEHQ_qC3sYBw; NTES_SESS=o45cf5gkilthQmqsqRKlih1I7asJobDBP3aIm57_H9qPzSAkzfcxNLFLThzSkIL_P1aNKfR0Ok5O7.HFZkoQkpOjBUv_u9jcQCL8m_BkXuwVj9TP5IdwO7r3HuajO.ETmVcOiulzkU3yQ0nTkbsU3qu7tv_URQW4YHEqUt9RzrlWVq8.TyecIORxaf60k1itw0SWQRl54Y4jL; S_INFO=1541663444|0|3&80##|twd4619; P_INFO=twd4619@163.com|1541663444|0|search|00&99|gux&1540784291&imooc#gux&450100#10#0#0|173219&0||twd4619@163.com; ___rl__test__cookies=1541664777755',
            'Host': 'fanyi.youdao.com',
            'Origin': 'http://fanyi.youdao.com',
            'Referer': 'http://fanyi.youdao.com/',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/70.0.3538.77 Chrome/70.0.3538.77 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

    # js的代码： f = "" + ((new Date).getTime() + parseInt(10 * Math.random(), 10)),
    # 通过13位的时间戳加上一个随机的个位数
    # python 中的时间戳是 10位加小数点，可以乘以 1000 取整
    def get_salt(self):
        # 获取时间戳
        timestamp = time.time()
        # 生成salt
        salt = int(timestamp*1000) + int(random.random()*10)
        return salt

    # var g = n.md5(u + d + f + c);
    # sign 通多几个数相加然后进行 md5 加密
    def get_sign(self):
        u = "fanyideskweb"
        d = self.q
        f = self.get_salt()
        c = "rY0D^0'nM0}g5Mm1z%1G4"
 
        str_data = u + str(d) + str(f) + c
 
        # md5加密
        m = hashlib.md5()
        m.update(str_data.encode('utf-8'))
        sign = m.hexdigest()
 
        return f, sign

    # 翻译过程
    def translate(self):
        salt, sign = self.get_sign()
        data = {
            "i": self.q,
            "from": "AUTO",
            "to": "AUTO",
            "smartresult": "dict",
            "client": "fanyideskweb",
            "salt": salt,
            "sign": sign,
            "doctype": "json",
            "version": "2.1",
            "keyfrom": "fanyi.web",
            "action": "FY_BY_CLICKBUTTION",
            "typoResult": "false"
        }
        resp = requests.post(url = self.url, data = data, headers = self.headers)
        try:
            trans_result = json.loads(resp.content).get('translateResult')[0][0].get('tgt')
        except:
            trans_result = ''
            print(json.loads(resp.content))
        finally:
            return trans_result
        
 
if(__name__ == '__main__'):
    w = "hello world"
    t = Youdao_translate(w)
    print(t.translate())
