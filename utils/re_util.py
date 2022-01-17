#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2021/2/7 13:19
'''
import re

punctuation = '!,;:?"\'、，；“.” *'


def removePunctuation(text):
    text = re.sub(r'[{}]+'.format(punctuation), ' ', text)
    return text.strip()


def search_text_by_reg(reg, text):
    try:
        search = re.search(reg, text)
        groups = search.group()
        return groups
    except:
        return None


def find_texts_by_reg(reg, text):
    try:
        searchs = re.findall(reg, text)
        return searchs
    except:
        return None


if __name__ == '__main__':
    re.compile(r'asd$')

    # search = search_text_by_reg(r'(\d{7,11})', "你好12345678911厕所")
    cookies = "AlteonP=APcZL2TcHKz3B3twFFdCVw$$; Path=/, JSESSIONID=8KS2h9ML0HYTw2lTNQXyynkDDLpf5VnTpjgfLxgvxLhrBCJGHrsf!-530257836; path=/; HttpOnly"
    # search = find_texts_by_reg(r'(AlteonP=.+?);|(JSESSIONID=.+?);', cookies)
    search ="; ".join(find_texts_by_reg(r'(JSESSIONID=.+?|AlteonP=.+?)(?=;)', cookies))
    print(f"【().search={search}】")
