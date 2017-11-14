#coding:utf-8
import requests,re,json,sys,os,random,linecache,time

loginUrl='http://sso.vmall.moxian.com/mo_common_sso/m2/vmall/login'
moQiangUrl='http://grab.vmall.moxian.com/mo_grab/m2/mograb/grab'
current_path = sys.path[0]
userListDir = os.path.join(current_path, 'userList.txt')
moQiangPid=file(os.path.join(current_path,'moQiangPid.txt'),'a+')

class MoQiang():

# =============================================获取登录的Token=============================================

    def loginVmall(self):
        count = len(open(userListDir).readlines())
        randomNum = random.randrange(1, count, 1)
        randomLine = linecache.getline(userListDir, randomNum).strip('\n')
        account = randomLine.strip().split(',')[0]
        password = randomLine.strip().split(',')[1]
        postData = {"userAgent": "10", "account": account, "password": password,
                    "deviceId": "268db04a09776a6e105d575e5ea335ec",
                    "deviceToken": "2d50003c79dd12dec9deda75dbd17f4403cc993be87238c7926ecc8ad29ef398"}
        header = {'Content-Type': 'application/json'}
        postRequests = requests.post(loginUrl, data=json.dumps(postData), headers=header)
        reToken = '"token":"(.+?)",'
        reUserID = '{"userId":(.+?),'
        tokenResult = re.search(reToken, postRequests.content)
        userIDResule = re.search(reUserID, postRequests.content)
        postRequest = [tokenResult.group(1), userIDResule.group(1)]
        return postRequest

# =============================================魔枪功能=============================================

    def robot(self,moQiangId):
        while 1:
            try:
                loginResult = self.loginVmall()
                moQiangData = {"batchInfoId": moQiangID}
                moQiangHeader = {'userId': loginResult[1], 'token': loginResult[0], 'appType': 'moxian',
                                 'Content-Type': 'application/json'}
                moQiang = requests.post(moQiangUrl, data=json.dumps(moQiangData), headers=moQiangHeader)
                reMoqiangResult = '{"result":(.+?),'
                moQiangResult = re.search(reMoqiangResult, moQiang.content)
                moqiangResult = moQiangResult.group(1)
                if moqiangResult == "true":
                    time.sleep(random.randrange(120, 160))
            except Exception as e:
                print e

if __name__ == '__main__':
    moQiangID = sys.argv[1]
    moQiangPid.write(str(moQiangID) + ',' + str(os.getpid()) + '\n')
    moQiangPid.close()
    test=MoQiang()
    test.robot(moQiangID)

