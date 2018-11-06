# 金山词霸翻译，只能翻译单词，给出详细解析

import requests
import re

def get_page(url):
    try:
        response = requests.get(url,timeout=10)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response.text
    except:
        print('Failed')
        return None


def parse_page(html):
    original_word = re.compile(r'<div class="in-base-top .*?<h1 class="keyword">(.*?)</h1>',re.S)
    translation = re.compile(r'<li class="clearfix">(.*?)</li>',re.S)
    try:
        original_input = re.findall(original_word,html)
        print(original_input[0].strip())   # 输出查询的内容
    except:
        print('Sorry,it is not found.')
        print(''.center(20,'='))
    items = re.findall(translation,html) # 匹配各词义
 
    for item in items:
        part = re.compile(r'<span class="prop">(.*?)</span>',re.S)
        meanings = re.compile(r'<span>(.*?)</span>')
        print(re.findall(part,item)[0]) # 输出词性
        meaning = re.findall(meanings,item)
        for i in range(len(meaning)):
            print(meaning[i]) # 输出词义
        print(''.center(20,'=')) # 分割线


def main():
    while True:
        base_url = 'http://www.iciba.com/'
        word = input('Please input what you want to check(input q to exit):')
        if word == 'q':
            break    # 输入'q'退出查询
        else:
            url  = base_url + word
            print(url)
        html = get_page(url)
        parse_page(html)


if __name__ == '__main__':
    main()