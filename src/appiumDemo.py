# coding:utf-8

'''
Created on 2017��10��26��

@author: Moxian
'''

from appium import webdriver
import time


desired_caps = {
                'platformName': 'Android',
                'deviceName': '80SQBDQB22DVE',
                'platformVersion': '7.1.1',
                'appPackage': 'com.lemon.faceu',
                'appActivity': 'com.lemon.faceu.login.LoadingPageActivity',
                'resetKeyboard': True,
                'unicodeKeyboard':True
                } 

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)

driver.wait_activity('com.lemon.faceu.login.ChooseEntryActivity', 3, 6)

# driver.find_element_by_xpath('//com.lemon.faceu:id/ll_login_wx//android.widget.ImageView[1]').click()

driver.find_element_by_android_uiautomator('new UiSelector().className("android.widget.ImageView").fromParent(new UiSelector().text("Q Q 登录"))').click()

driver.wait_activity('com.tencent.open.agent.AuthorityActivity', 3, 6)

driver.find_element_by_android_uiautomator('new UiSelector().text("登录")').click()

driver.wait_activity('.mainpage.MainActivity', 3, 6)

driver.find_element_by_android_uiautomator('new UiSelector().resourceId("com.lemon.faceu:id/iv_layout_three_tab_left_icon")').click()


time.sleep(5)

print driver.current_activity

# driver.find_element_by_id('com.morow.shopping:id/login_account_et').clear()

# driver.find_element_by_android_uiautomator('new UiSelector().text("Add note")')

# time.sleep(2)

# driver.find_element_by_id('com.morow.shopping:id/login_account_et').send_keys("cn42212201")

# driver.find_element_by_id('com.morow.shopping:id/login_pawwWord_et')

# driver.find_element_by_id('com.morow.shopping:id/login_pawwWord_et').send_keys('abc123')

# driver.find_element_by_id('com.morow.shopping:id/login_button').click()

# print driver.page_source

driver.quit()