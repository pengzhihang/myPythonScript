#coding:utf-8

import requests

re=requests.get('http://www.baidu.com')

print re.text

import unittest

class TestCase(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testMet1(self):
        pass

if __name__ == '__main__':
    unittest.main()
