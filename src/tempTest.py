#coding:utf-8

import requests

re=requests.get('http://www.baidu.com')

print re.text


