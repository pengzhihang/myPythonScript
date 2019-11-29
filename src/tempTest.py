#coding:utf-8
import json

a={}

for i in range(10):
    
    a.fromkeys(str(i),i)
    
print a