import sys
import socket
import chardet

print sys.getdefaultencoding()

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(("10.10.1.104",4022))
data=s.recv(1024)
print chardet.detect(data)
print data.decode('Windows-1253')
