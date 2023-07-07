from urllib.parse import urljoin
from selenium import webdriver
import requests
import time


from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By

BASE_URL = 'https://portal.ustraveldocs.com/?language=Chinese%20(Simplified)&country=China'
LOGIN_URL = urljoin(BASE_URL,'/login')
INDEX_URL = urljoin(BASE_URL,'/page/1')
USERNAME ='SenGeMail@163.com'
PASSWORD = 'Qq734697554'

option = ChromeOptions()
option.add_argument('--headless')
option.add_experimental_option('excludeSwitches',['enable-automation'])
option.add_experimental_option('useAutomationExtension',False)

user_agent =  ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
option.add_argument(f'user-agent={user_agent}')

browser = webdriver.Chrome(option)
browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',{
    'source' : 'Object.defineProperty(navigator,"webdriver",{get:()=>undefined})'
})
browser.set_window_size(1366,768)

browser.get(BASE_URL)
print(browser.page_source)

browser.find_element(By.CSS_SELECTOR,'input[name="loginPage:SiteTemplate:siteLogin:loginComponent:loginForm:username"]').send_keys(USERNAME)
browser.find_element(By.CSS_SELECTOR,'input[name="loginPage:SiteTemplate:siteLogin:loginComponent:loginForm:password"]').send_keys(PASSWORD)
browser.find_element(By.CSS_SELECTOR,'input[type="checkbox"]').click()
browser.find_element(By.CSS_SELECTOR,'input[type="submit"]').click()
time.sleep(5)


print(browser.page_source)
browser.close()

#使用selenium, 打开网站-->登录-->预约时间->一直刷新时间->刷新日期->选择时间->提交

#通过执行javascript代码修改参数请求指定日期 -> 选择时间提交。
