# -*- coding:utf-8 -*-
import ctypes
import json
import re

import requests


class Baidu_Translate:
    def __init__(self, q = ''):
        self.method = 'Baidu'
        self.url = 'https://fanyi.baidu.com/transapi'
        self.q = q
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'BAIDUID=275F38AA4217D7457B13149A554D7E59:FG=1; BIDUPSID=275F38AA4217D7457B13149A554D7E59; PSTM=1541335243; locale=zh; to_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; from_lang_often=%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D; delPer=0; H_PS_PSSID=1457_21091_18559_26350_22159; PSINO=6; BDUSS=Wo2OH55WVpTQkZNRURhclVjN1k4cWRJQVZ3ZGw0OVlJLXV2OXRrUFNTdWtaZ3RjQVFBQUFBJCQAAAAAAAAAAAEAAADimTMp0KG2q2xpYW5qdW4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKTZ41uk2eNbV; ZD_ENTRY=google; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1541506531,1541517881,1541658734,1541668632; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1541672085; REALTIME_TRANS_SWITCH=0',
            'Host': 'fanyi.baidu.com',
            'Origin': 'https://fanyi.baidu.com',
            'Referer': 'https://fanyi.baidu.com/',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/70.0.3538.77 Chrome/70.0.3538.77 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

    def get_sign(self,gtk,r):
        m = int(gtk.split(".")[0])
        s = int(gtk.split(".")[1])
        S = {}
        v = 0
        c = 0
        while v < len(r):
            A = ord(r[v])
            if 128 > A:
                S[str(c)] = A
                c = c + 1
            else:
                if 2048 > A:
                    S[str(c)] = A >> 6 | 192
                    c = c + 1
                else:
                    if 55296 == (64512 & A) and v + 1 < len(r) and 56320 == (64512 & ord(r[v+1])):
                        v = v + 1
                        A = 65536 + ((1023 & A) << 10) + (1023 & ord(r[v]))
                        S[str(c)] = A >> 18 | 240
                        c = c + 1
                        S[str(c)] = A >> 12 & 63 | 128
                        c = c + 1
                    else:
                        S[str(c)] = A >> 12 | 224
                        c = c + 1
                        S[str(c)] = A >> 6 & 63 | 128
                        c = c + 1
                        S[str(c)] = 63 & A | 128
                        c = c + 1
            v = v + 1
        p = m
        b = 0
        F = "+-a^+6"
        D = "+-3^+b+-f"
        while b < len(S):
            p = p + S[str(b)]
            p = self.get_n(p, F)
            b = b + 1
        p = self.get_n(p, D)
        p ^= s
        if not 0 > p:
            p = p
        else:
            p = (2147483647 & p) + 2147483648
        p = p % 1e6
        p = str(int(p)) + "." + str((int(p) ^ m))
        # print(p)
        return p

    def get_n(self,p, D):
        t = 0
        while t < len(D)-2:
            a = D[t+2]
            if a >= "a":
                a = ord(a[0])-87
            else:
                a = int(a)
            if D[t + 1] == "+":
                a = self.unsigned_right_shift(p, a)
            else:
                a = p << a
            if D[t] == "+":
                p = p + a & 4294967295
            else:
                p = p ^ a
            t = t + 3
        return p

    def int_overflow(self,val):
        maxint = 2147483647
        if not -maxint-1 <=val <=maxint:
            val = (val + (maxint + 1)) % (2 * (maxint + 1)) - maxint -1
        return val

    def unsigned_right_shift(self,n, i):
        if n < 0:
            n = ctypes.c_uint32(n).value
        if i < 0:
            return -self.int_overflow(n << abs(i))
        return self.int_overflow(n >> i)

    def get_token_gtk(self):
        url = 'https://fanyi.baidu.com/'
        headers = self.headers
        response =requests.get(url,headers=headers)
        gtk_pattern = re.compile(r"window.gtk = '(.*?)';", re.S)
        gtk_results = re.findall(gtk_pattern,response.text)
        gtk = gtk_results[0]

        token_pattern = re.compile(r"token:(.*?),", re.S)
        token_results = re.findall(token_pattern, response.text)
        token = token_results[0].replace("'", "")
        # print(token, gtk)
        return token, gtk

    def translate(self):
        data = {
            'from': 'en',
            'to': 'zh',
            'query': self.q,
            'transtype': 'translang',
            'simple_means_flag': '3',
            'sign': '',
            'token': ''
        }
        token, gtk = self.get_token_gtk()
        data['sign'] = str(self.get_sign(gtk, self.q))
        data['token'] = str(token)
        resp = requests.post(url = self.url, data = data, headers = self.headers)
        try:
            trans_result = json.loads(resp.content).get('data')[0].get('dst')
        except:
            trans_result = ''
            print(json.loads(resp.content))
        finally:
            return trans_result

if(__name__ == '__main__'):
    w = 'hello world'
    t = Baidu_Translate(w)
    print(t.translate())
