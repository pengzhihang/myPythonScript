#coding:utf-8
#!/usr/bin/python
import subprocess

while 1:
        subprocess.Popen("mysql -h 61.139.126.53 -p 3306 -u root mysql --password=blah", shell=True).wait()