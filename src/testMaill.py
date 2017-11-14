#coding:utf-8

import smtplib
from email.mime.text import MIMEText
import requests

gethost=requests.get('http://www.runoob.com/python/python-exercise-example2.html')

mailUser = "luciferlly@qq.com"
mailPasswd  = "nxmthtsrqtwfbbij"
sengTo   = "peng.zhihang@moxiangroup.com;hangcheng163@163.com"

msg = MIMEText(gethost.content, _subtype='html', _charset='UTF-8')

msg["Subject"] = "这里是邮件标题"
msg["From"]=mailUser
msg["To"]=mailPasswd

try:
    maillObj = smtplib.SMTP_SSL("smtp.qq.com", 465)
    maillObj.login(mailUser, mailPasswd)
    maillObj.sendmail(mailUser, sengTo, msg.as_string())
    maillObj.quit()
    print "邮件发送成功!"
except smtplib.SMTPException,e:
    print "邮件发送失败,%s"%e