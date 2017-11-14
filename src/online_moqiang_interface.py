#!/usr/bin/env python
# coding: UTF-8
import requests, time, json, os
import sys, logging, random
import hashlib,linecache

reload(sys)
sys.setdefaultencoding('utf-8')
# grablist = 'http://grab.dev2.moxian.com/mo_grab/m2/mograb/rank?batchInfoId='+str(activityid)+'&pageSize=10'
graburl = 'http://grab.moxian.com/mo_grab/m2/grabplug'
current_path = sys.path[0]
useraccount_file_path = os.path.join(current_path, 'token.txt')
giftId_pid_file = file(os.path.join(current_path, 'giftId_pid.txt'), 'a+')


def initLogging(logFilename):
    logging.basicConfig(
        level=logging.WARNING,
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
        filename=logFilename,
        filemode='a')
    console = logging.StreamHandler()
    console.setLevel(logging.WARNING)
    formatter = logging.Formatter('%(asctime)s %(filename)s LINE %(lineno)-2d : %(levelname)-s %(message)s');
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

class Grab(object):
    def getbatchInfoId(self, header):
        global grablist
        try:
            grablistreq = requests.get(grablist, headers = header)
            response = grablistreq.json()
            batchInfoId = response.get('data').get('batchInfoId')
            return batchInfoId
        except Exception as e:
            print e

    def grab(self, giftId):
        global graburl, grabcount
        i = 0
        while 1:
            try:
                count = len(open(useraccount_file_path).readlines())
                randomNum = random.randrange(1, count, 1)
                randomLine = linecache.getline(useraccount_file_path, randomNum).strip('\n')
                logging.warning('随机获取文件中的第%s行，内容为：%s'%(randomNum, randomLine))
                phoneNo = randomLine.strip().split(',')[0]
                token = randomLine.strip().split(',')[1]
                userid = randomLine.strip().split(',')[2]
                header = {'Content-Type': 'application/json', 'appType': 'mopai', 'userId': userid, 'token': token}
                batchinfoId = self.getbatchInfoId(header)
                m2 = hashlib.md5()
                m2.update(str(batchinfoId))
                mac = m2.hexdigest()
                body = {'batchInfoId': giftId, 'mac': mac}
                grabstart = time.time()
                grabreq = requests.post(graburl, data=json.dumps(body), headers=header)
                print grabreq
                response = grabreq.json()
                print response
                grabend = time.time()
                logging.warning('the start time is %s'%grabstart)
                logging.warning('the end time is %s'%grabend)
                grabdelay = int(str(grabend)[:10]) - int(str(grabstart)[:10])
                logging.warning('the delay time is %s' % grabdelay)
                logging.warning(header)
                logging.warning(body)
                logging.warning(response)
                code = response.get('code')
                result1 = response.get('result')
                if result1 == True:
                    i = i + 1
                    logging.warning('*********************抢拍者：%s*********************' % phoneNo)
                    logging.warning('*********************以上是第%s次抢拍，然后随机等待60-100秒*********************'%i)
                    time.sleep(random.randrange(60, 100))
            except Exception as e:
                logging.warning(e)

if __name__ == '__main__':
    #activityid = 106
    activityid = sys.argv[1]
    grablist = 'http://grab.moxian.com/mo_grab/m2/mograb/rank?batchInfoId=' + str(activityid) + '&pageSize=10'
    initLogging('activity_' + str(activityid) + '.log')
    giftId_pid_file.write(str(activityid) + ',' + str(os.getpid()) + '\n')
    giftId_pid_file.close()
    test = Grab()
    test.grab(activityid)
