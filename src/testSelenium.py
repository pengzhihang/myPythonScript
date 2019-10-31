# coding:utf-8

import time
from selenium import webdriver


wb = webdriver.Chrome()

wb.get('http://10.1.1.61:8090/#/pool')

wb.maximize_window()

jsScript = '''localStorage.setItem('userToken','{"email":"","phone":"13******84","access_token":"fbf754fd-c627-4ffd-9fff-8cf7b51da745","token_type":"bearer","refresh_token":"4d83092d-8c6e-41b6-ae89-8813b4549d8b","expires_in":259199,"scope":"xx","inviteCode":"HDZS","twoVerification":1,"loginVerification":1,"countryCode":"CN","uuid_token":"169C8333133BD9E27CBB63A3DC1B7C12","sign_code":"e216bfe7744d4ff78d45a8efed4c8afa"}')'''

wb.execute_script(jsScript)

wb.refresh()

wb.find_element_by_xpath('//a[contains(text(),"交易中心")]').click()

time.sleep(5)




# 
# 
# try:
# 
#     wb.find_element_by_xpath('//div[@label="邮箱/手机"]//input').send_keys('13410448384')
#     
#     wb.find_element_by_xpath('//div[@label="登录密码"]//input').send_keys('Qq646832611')
#     
#     wb.find_element_by_id('submitForm').click()
#     
#     time.sleep(10)
#     
#     wb.quit()
# except:
#     wb.quit()
