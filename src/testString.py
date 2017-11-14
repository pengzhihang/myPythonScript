'''

@author: Moxian

'''


fileStr=open('./myapp.log',"r")

strFile=fileStr.read()

strA=strFile.split('\n')

print strA[0]

fileStr.close()