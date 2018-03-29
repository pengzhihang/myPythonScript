#coding:utf-8

'''
Created on 2018年3月28日

@author: Moxian
'''
import requests
import sys
import re
import os
import time

if(len(sys.argv)==2):
    a=sys.argv[1]
else:
    a=sys.argv[1]+' '+sys.argv[2]  

httpHeand={
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.8',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}
 
''' 
 
1、获取Hash与AlbumID
 
'''
 
getData={'keyword':a.decode('gbk').encode('utf-8'),'page':'1','pagesize':'1','clientver':'=&platform=WebFilter'}
   
hashUrl='http://songsearch.kugou.com/song_search_v2'
   
getHashandAlbumID=requests.get(hashUrl,params=getData,headers=httpHeand)

hashRe='(,"FileHash":")([\s\S]*?)(",")'

albumIdRe='(,"AlbumID":")([\s\S]*?)(",")'

hashValue=re.search(hashRe,getHashandAlbumID.content)

albumIdValue=re.search(albumIdRe,getHashandAlbumID.content)

''' 
 
2、获取Mp3下载地址
 
'''

getUrl='http://www.kugou.com/yy/index.php'

musicData={'r':'play/getdata','hash':hashValue.group(2),'album_id':albumIdValue.group(2)}

getMusicUrl=requests.get(getUrl,params=musicData,headers=httpHeand)

musicRe='(","play_url":")([\s\S]*?)(",")'

musicUrl=re.search(musicRe,getMusicUrl.content).group(2).replace('\\','')

musicFile=requests.get(musicUrl)

if(os.path.exists('d:\\myMusic')==False):
    os.makedirs('d:\\myMusic')

with open('d:\\myMusic\\'+sys.argv[1]+'.mp3', "wb") as code:
     code.write(musicFile.content)