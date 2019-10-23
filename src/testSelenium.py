#coding:utf-8

from selenium import webdriver
import time

wb=webdriver.Chrome()

wb.get('http://10.1.1.61:8090/#/login')

wb.maximize_window()

try:

    wb.find_element_by_xpath('//div[@label="邮箱/手机"]//input').send_keys('13410448384')
    
    wb.find_element_by_xpath('//div[@label="登录密码"]//input').send_keys('Qq646832611')
    
    wb.find_element_by_id('submitForm').click()
    
    time.sleep(10)
    
    wb.quit()
except:
    wb.quit()