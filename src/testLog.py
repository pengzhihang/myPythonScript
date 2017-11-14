#coding:utf-8

import myTools

import logging

logging.basicConfig(level=logging.DEBUG,
                    filename='c:\\11.txt',
                    filemode='w',
                    format='%(asctime)s - %(filename)s - [line:%(lineno)d] - [%(levelname)s] - : %(message)s')

log=logging.StreamHandler()
log.setLevel(logging.INFO)
logFormat=logging.Formatter('%(asctime)s - %(filename)s - [line:%(lineno)d] - [%(levelname)s] - : %(message)s')
log.setFormatter(logFormat)
logging.getLogger('').addHandler(log)

logging.debug('调试信息')
logging.info('常规信息')
logging.warning('警告信息')
logging.error('错误信息')
logging.critical('崩溃信息')


