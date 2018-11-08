#coding=utf8
import json

import requests


class Google_Translate:
    def __init__(self, q = ''):
        self.method = 'Google'
        self.url = "https://translate.google.cn"
        self.q = q
        self.headers = {
            'accept': '*/*',
            'accept-encoding':'gzip, deflate, br',
            'accept-language':'zh-CN,zh;q=0.9',
            'cookie':'_ga=GA1.3.1936707078.1541472661; 1P_JAR=2018-11-8-8; _gid=GA1.3.11121852.1541666315; NID=146=dfUw-CGjYomLXpEoTn-GBQfQAmOAclNCkyWO_IOVXujT9pesJhhXGpUUNECNkjn23Q1pmcsZPQjwkX5m1R2edN_xpFjdVl4K9mhYa9xcpiQH7EZHQrxmceUl6BwZ1R1abNs2WStE6PPXRzsIoIbcojUuKdl0HaiX9Syvb_5e6zw',
            'referer':'https://translate.google.cn/m/translate',
            'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/70.0.3538.77 Chrome/70.0.3538.77 Safari/537.36'
        }

    # 获取google翻译内容的tk值
    # a：要翻译的内容，以字符串指定
    # 注意：要翻译的内容只能是英文，即只能是包含ASCII码的英文字符串
    def get_tk(self, a):
        TKK = (lambda a=561666268, b=1526272306:str(406398) + '.' + str(a + b))()
        
        def b(a, b):
            for d in range(0, len(b)-2, 3):
                c = b[d + 2]
                c = ord(c[0]) - 87 if 'a' <= c else int(c)
                c = a >> c if '+' == b[d + 1] else a << c
                a = a + c & 4294967295 if '+' == b[d] else a ^ c
            return a
        
        e = TKK.split('.')
        h = int(e[0]) or 0
        g = []
        d = 0
        f = 0
        while f < len(a):
            c = ord(a[f])
            if 128 > c:        
                g.insert(d,c)
                d += 1
            else:
                if 2048 > c:
                    g[d] = c >> 6 | 192
                    d += 1
                else:
                    if (55296 == (c & 64512)) and (f + 1 < len(a)) and (56320 == (ord(a[f+1]) & 64512)):
                        f += 1
                        c = 65536 + ((c & 1023) << 10) + (ord(a[f]) & 1023)
                        g[d] = c >> 18 | 240
                        d += 1
                        g[d] = c >> 12 & 63 | 128
                        d += 1
                    else:
                        g[d] = c >> 12 | 224
                        d += 1
                        g[d] = c >> 6 & 63 | 128
                        d += 1
                    g[d] = c & 63 | 128
                    d += 1
            f += 1
        a = h
        for d in range(len(g)):
            a += g[d]
            a = b(a, '+-a^+6')
        a = b(a, '+-3^+b+-f')
        a ^= int(e[1]) or 0
        if 0 > a:a = (a & 2147483647) + 2147483648
        a %= 1E6
        return str(int(a)) + '.' + str(int(a) ^ h)

    def translate(self):
        tk = self.get_tk(self.q)
        path = "/translate_a/single?client=webapp&sl=auto&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&source=bh&ssel=0&tsel=0&kc=1&tk={0}&q={1}".format(tk, self.q)
        proxies = {
            'http': 'socks5://user:pass@127.0.0.1:1080',
            'https': 'socks5://user:pass@127.0.0.1:1080'
        }
        url = self.url + path
        resp = requests.get(url = url, headers = self.headers, proxies = proxies)
        try:
            trans_result = json.loads(resp.content)[0][0][0]
        except:
            trans_result = ''
            print(json.loads(resp.content))
        finally:
            return trans_result


if(__name__ == '__main__'):
    w = "hello world"
    t = Google_Translate(w)
    print(t.translate())
