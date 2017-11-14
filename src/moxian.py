#coding:utf-8
import requests,re,json,sys,os,random,linecache,time

loginUrl='http://login.test.moxian.com/mo_common_login/m2/auth/login'
moQiangUrl='http://grab.test.moxian.com/mo_grab/m2/mograb/grab'
current_path = sys.path[0]
userListDir = os.path.join(current_path, 'moxian.txt')

class MoQiang():

# =============================================获取登录的Token=============================================

    def loginVmall(self):
        count = len(open(userListDir).readlines())
        randomNum = random.randrange(1, count, 1)
        randomLine = linecache.getline(userListDir, randomNum).strip('\n')
        account = randomLine.strip().split(',')[0]
        password = randomLine.strip().split(',')[1]
        postData = {"useraccount": account, "userpass": password,
                    "loginAppType": "moxian"}
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
            loginResult=self.loginVmall()
            moQiangData = {"batchInfoId": moQiangID}
            moQiangHeader = {'userId': loginResult[1], 'token': loginResult[0], 'appType': 'moxian',
                             'Content-Type': 'application/json'}
            moQiang = requests.post(moQiangUrl, data=json.dumps(moQiangData), headers=moQiangHeader)
            reMoqiangResult='{"result":(.+?),'
            moQiangResult=re.search(reMoqiangResult,moQiang.content)
            moqiangResult=moQiangResult.group(1)
            if moqiangResult=="true":
                time.sleep(random.randrange(60,100))

if __name__ == '__main__':
    moQiangID = sys.argv[1]
    test=MoQiang()
    test.robot(moQiangID)

