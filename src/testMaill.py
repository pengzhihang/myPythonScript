#coding:utf-8

import smtplib
from email.mime.text import MIMEText
import requests

gethost=requests.get('http://www.baidu.com')

htmlPage=''''''

mailUser = "luciferlly@qq.com"
mailPasswd  = "ssyzdmfdftjebfhg"
sengTo   = "zhangwq@citex.io"

msg = MIMEText(htmlPage, _subtype='html', _charset='utf-8')

msg["Subject"] = "使用Python发送邮件"
msg["From"]=mailUser
msg["To"]=sengTo

try:
    maillObj = smtplib.SMTP_SSL("smtp.qq.com", 465)
    maillObj.login(mailUser, mailPasswd)
    maillObj.sendmail(mailUser, sengTo, msg.as_string())
    maillObj.quit()
    print "邮件发送成功!"
except smtplib.SMTPException,e:
    print "邮件发送失败,%s"%e
