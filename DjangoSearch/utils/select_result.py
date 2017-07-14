#!/usr/bin/python
#-*-coding:utf-8-*-

import types
from w3lib.html import replace_entities
from urllib.parse import urljoin,urlparse
from hashlib import md5
import random, string

NULL = [None,'null']

list_first_item = lambda x: x[0] if x else None
list_item_at = lambda x, idx: x[idx] if x else None

list_first_str = lambda x: x[0].strip() if x else ""
list_str_at = lambda x,idx: x[idx].strip() if x else ""

list_first_int = lambda x: int(x[0]) if x else 0
list_int_at = lambda x,idx: list_str_at(x, idx) if x else 0


def clean_link(link_text):
    """
        Remove leading and trailing whitespace and punctuation
    """

    return link_text.strip("\t\r\n '\"")

clean_url = lambda base_url, u, response_encoding: urljoin(base_url, replace_entities(clean_link(u.decode(response_encoding))))
"""
    remove leading and trailing whitespace and punctuation and entities from the given text.
    then join the base_url and the link that extract
"""


# 获取url的md5编码
def get_linkmd5id(link):
    return md5(link.strip().encode('utf-8')).hexdigest()

# 生成随机ID
def generateRandomID():
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(15))
