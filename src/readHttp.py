#coding:utf-8

import requests, re
import myTools

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


print getResult.group(2).replace('&nbsp;','').replace('<br/>','\n')


