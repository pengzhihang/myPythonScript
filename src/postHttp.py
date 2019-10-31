#coding:utf-8

'''
Created on 2017年9月11日

@author: Moxian
'''
import requests,re

# =============================================================获取最新章节=============================================================

hostName="http://m.booktxt.net"

hostUrl=hostName+"/wapbook/1137.html"

httpHeand={
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.8',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

getRequests=requests.get(hostUrl,headers=httpHeand)

reTxt='(<p><a href=")([\s\S]*?)(\">)'

searchResult=re.search(reTxt,getRequests.content)

# =============================================================查看最新小说=============================================================

newUrl=hostName+str(searchResult.group(2))

newGet=requests.get(newUrl,headers=httpHeand)

newTxt='(</a></p>)([\s\S]*?)(<p style="width:100%;text-alight:center;">)'

getResult=re.search(newTxt,newGet.content.decode('GBK'))

postUrl="https://sc.ftqq.com/SCU11653Tbb41ab3e084b263443c485a677d3705559b5fe1344043.send"

postData={"text":"一念永恒","desp":getResult.group(2).replace('&nbsp;','').replace('<br/>','\n')}

postRequest=requests.post(postUrl,data=postData)

