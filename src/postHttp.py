#coding:utf-8

'''
Created on 2017年9月11日

@author: Moxian
'''
import requests,re

# =============================================================获取最新章节=============================================================

hostName="http://m.booktxt.net"

hostUrl=hostName+"/wapbook/1137.html"

getRequests=requests.get(hostUrl)

reTxt='(<p><a href=")([\s\S]*?)(\">)'

searchResult=re.search(reTxt,getRequests.content)

# =============================================================查看最新小说=============================================================

newUrl=hostName+str(searchResult.group(2))

newGet=requests.get(newUrl)

newTxt='(</a></p>)([\s\S]*?)(<p style="width:100%;text-alight:center;">)'

getResult=re.search(newTxt,newGet.content.decode('GBK'))

postUrl="https://sc.ftqq.com/SCU11653Tbb41ab3e084b263443c485a677d3705559b5fe1344043.send"

postData={"text":"一念永恒","desp":getResult.group(2).replace('&nbsp;','').replace('<br/>','\n')}

postRequest=requests.post(postUrl,data=postData)
