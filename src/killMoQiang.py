# /usr/bin/env python
# -*- coding:utf-8 -*-
# sys.setdefaultencoding('utf-8')
import os
import sys

current_path = sys.path[0]

class killMoQiang(object):
    def killprocess(self, activityId):
        for linedate in open('moQiangPid.txt'):
            giftid = linedate.strip().split(',')[0]
            pid = linedate.strip().split(',')[1]
            if int(giftid) == activityId:
                os.popen('kill -9 ' + pid)
                continue

if __name__ == '__main__':
    activityid = sys.argv[1]
    test = killMoQiang()
    test.killprocess(int(activityid))


