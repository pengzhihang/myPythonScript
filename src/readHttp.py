#coding:utf-8

import requests, re
import myTools

# =============================================================获取最新章节=============================================================

hostName="http://m.booktxt.net"

hostUrl=hostName+"/wapbook/1137.html"

getRequests=requests.get(hostUrl)

reTxt='(<div style=\'background-color:#F4F4F4\'><a href=\')([\s\S]*?)(\'>)'

searchResult=re.search(reTxt,getRequests.content)

# =============================================================查看最新小说=============================================================

newUrl=hostName+str(searchResult.group(2))

newGet=requests.get(newUrl)

newTxt='(<div id="nr1"\>)([\s\S]*?)(</div>)'

getResult=re.search(newTxt,newGet.content.decode('GBK'))

myTools.sendMail('peng.zhihang@moxiangroup.com','一念永恒',getResult.group(2).replace('&nbsp;','').replace('<br />',''))


