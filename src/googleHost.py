#coding:utf-8
import xml.etree.ElementTree
import re
import requests
import platform

host="http://www.360kb.com/kb/2_122.html"

http_requests=requests.get(host)

get_str='(<code class="Ini">)([\s\S]*?)(</code>)'

re_str=re.search(get_str,http_requests.text)

if platform.uname()[0]=='Windows':
    file = r'c:\windows\system32\drivers\etc\hosts'
else:
    file = r'/etc/hosts'
 
host_file=open(file,"w")

host_file.write(re_str.group(2))

host_file.close()

print re_str.group(2)