#coding:utf-8
import logging
import requests
import re
import smtplib
from email.mime.text import MIMEText

def sayHello(a):

    print a

def lookBook(host):

    httpHost=requests.get(host)

    print httpHost.content.decode('gbk')

    httpHost.close()

def searchTxt(a,b):

    sourceFile = open(a, "r")

    search_str = b

    search_reults = re.search(search_str, sourceFile.read())

    sourceFile.close()

    return search_reults.group(0)

def sendMail(sendAD,sendTitle,sendMSG):

    mailUser = "luciferlly@qq.com"
    mailPasswd = "nxmthtsrqtwfbbij"
    msg = MIMEText(sendMSG, _subtype='plain', _charset='UTF-8')
    msg["Subject"] = sendTitle
    msg["From"] = mailUser
    msg["To"] = sendAD

    try:
        maillObj = smtplib.SMTP_SSL("smtp.qq.com", 465)
        maillObj.login(mailUser, mailPasswd)
        maillObj.sendmail(mailUser, sendAD, msg.as_string())
        maillObj.quit()
        print "邮件发送成功!"
    except smtplib.SMTPException, e:
        print "邮件发送失败,%s" % e