from Google import Google_Translate
from Baidu import Baidu_Translate
from Youdao import Youdao_translate
from multiprocessing.pool import Pool

G = Google_Translate()
B = Baidu_Translate()
Y = Youdao_translate()

def translate(T):
    print("{}：{}".format(T.method, T.translate()))

if(__name__ == '__main__'):
    while True:
        q = input("输入需要翻译的内容，输入q退出：\n")
        if(q == '' or q == 'q'):
            break
        G.q = q
        B.q = q
        Y.q = q
        print("-"*50)
        with Pool(3) as p:
            p.map(translate,[G,B,Y])
        print("-"*50)