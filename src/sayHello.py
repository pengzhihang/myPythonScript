#coding:utf-8

'''
Created on 2017年9月11日

@author: Moxian
'''
import requests,re,json


# =============================================================获取最新章节=============================================================

hostName="http://m.booktxt.net"

httpHeand={
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.8',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

hostUrl=hostName+"/wapbook/1137.html"

httpRequests=requests.get(hostUrl,headers=httpHeand)

print httpRequests.content