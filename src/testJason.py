#coding:utf-8
import requests
import json
import time
 
url='http://10.1.1.61:8090/'
# url='https://www.citex.io/'

# loads为把jason格式转换为电子字典格式
# 
# hump为把电子字典格式转换为jason格式


#1、 获取美元，人民币兑率 
getLegalRateRequest=requests.get(url+'common/exchange/list')
legalRateData=json.loads(getLegalRateRequest.content)
def getLegalRate(name):
    for i in legalRateData['result']:
        if i['name']==name:
            Rate=float(i['rate'])
    return Rate

# 2、获取币种美元汇率价格
getCurrencyRateRequest=requests.get(url+'common/exchange/coins')
currencyRateData=json.loads(getCurrencyRateRequest.content)
def getCurrencyRate(currencyId):
    for i in currencyRateData['result']:
        if i['currencyId']==int(currencyId):
            coinsRate=float(i['latest'])
            return coinsRate