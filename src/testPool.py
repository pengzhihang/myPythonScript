#coding:utf-8
import random
import time
from concurrent.futures import ThreadPoolExecutor
import requests
from lxml import etree

re=requests.get('http://ip.jiangxianli.com/')
getHtml=etree.HTML(re.content)
getIPS=getHtml.xpath("//tbody/tr/td[2]")
getPORTS=getHtml.xpath("//tbody/tr/td[3]")
getTYPES=getHtml.xpath("//tbody/tr/td[4]")

tl=ThreadPoolExecutor(20)

def getResult(proxie):
    
    try:
        re=requests.get('http://2000019.ip138.com/',proxies=proxie,timeout=10)
    
        getHtml=etree.HTML(re.content)
        
        getIP=getHtml.xpath("//p[@align='center']")
        
        print getIP[0].text
        
    except:
        print '失效IP'

for i in range(len(getIPS)):
    
    if getTYPES[i].text.encode('utf-8')=='高匿':
    
        print 'IP地址:%s , 端口号:%s'%(getIPS[i].text,getPORTS[i].text)
        
        proxie={'http':'http://%s:%s'%(getIPS[i].text,getPORTS[i].text)}
        
        tl.submit(getResult,proxie)


# with open('d:\\hb01.txt','r') as re:
#     getTxt=re.readlines()
# re.close() 
# 
# 
# for i in getTxt:
#     a=i.split(',')
#     print '账户名:%s , Token值:%s'%(a[0],a[1])

# 
# for i in range(1,9):
#     for j in range(9-i):
#         print j*' '+i*'*'

# 
# def writeLang():
#     with open('D:\\testLang.txt','at') as tl:
#         a=str(time.time())+'现在时间'+'\n'
#         tl.write(a)
#         tl.close()
# a=ThreadPoolExecutor(1000)
# 
# for i in range(300000):
#    a.submit(writeLang())


# 
# # 中奖计数
# g1=0
# g2=0
# g3=0
# g4=0
# g5=0
# g6=0
# g7=0
# g8=0
# # 奖池计数
# d1=1
# d2=2
# d3=37
# d4=160
# d5=400
# d6=6000
# d7=8000
# d8=99999999
#  
# for i in range(100000):
#      
#     a=random.randint(0,100000)
#  
#     if a>=1 and a<=25:
#         if d1==0:
#             g8+=1
#         else:
#             print '恭喜获得一等奖'
#             g1+=1
#             d1-=1
#     elif a>=26 and a<=50:
#         if d2==0:
#             g8+=1
#         else:
#             print '恭喜获得二等奖'
#             g2+=1
#             d2-=1
#     elif a>=51 and a<=925:
#         if d3==0:
#             g8+=1
#         else:
#             print '恭喜获得三等奖'
#             g3+=1
#             d3-=1
#     elif a>=926 and a<=4000:
#         if d4==0:
#             g8+=1
#         else:
#             print '恭喜获得四等奖'
#             g4+=1
#             d4-=1
#     elif a>=4001 and a<=10000:
#         if d5==0:
#             g8+=1
#         else:
#             print '恭喜获得五等奖'
#             g5+=1
#             d5-=1
#     elif a>=10001 and a<=15000:
#         if d6==0:
#             g8+=1
#         else:
#             print '恭喜获得六等奖'
#             g6+=1
#             d6-=1
#     elif a>=15001 and a<=20000:
#         if d7==0:
#             g8+=1
#         else:
#             print '恭喜获得七等奖'
#             g7+=1
#             d7-=1
#     else :
#         print '恭喜获得八等奖'
#         g8+=1
#         d8-=1
#          
# print g1
# print g2
# print g3
# print g4
# print g5
# print g6
# print g7
# print g8
#  
# print '=========================='
#  
# print d1
# print d2
# print d3
# print d4
# print d5
# print d6
# print d7
# print d8

#     
# lists=[0.00025,0.0005,0.00925,0.04,0.1,0.15,0.2,0.5]
# 
# for i in lists:
#     print i*100000