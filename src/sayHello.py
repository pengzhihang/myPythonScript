

import requests

hostName="http://m.booktxt.net"

hostUrl=hostName+"/wapbook/1137_2648936.html"

getRequests=requests.get(hostUrl)

print getRequests.content.decode('GBK')