from urllib.parse import urljoin
from selenium import webdriver
import requests
import time


from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By

BASE_URL = 'https://login2.scrape.center/'
LOGIN_URL = urljoin(BASE_URL,'/login')
INDEX_URL = urljoin(BASE_URL,'/page/1')
USERNAME ='admin'
PASSWORD = 'admin'

option = ChromeOptions()
option.add_argument('--headless')
browser = webdriver.Chrome(option)
browser.set_window_size(1366,768)

browser.get(BASE_URL)
browser.find_element(By.CSS_SELECTOR,'input[name="username"]').send_keys(USERNAME)
browser.find_element(By.CSS_SELECTOR,'input[name="password"]').send_keys(PASSWORD)
browser.find_element(By.CSS_SELECTOR,'input[type="submit"]').click()
time.sleep(10)

cookies = browser.get_cookies()
print('Cookies',cookies)
browser.close()


session =  requests.Session()
for c in cookies:
    session.cookies.set(c['name'],c['value'])

response_index = session.get(INDEX_URL)
print('status',response_index.status_code)
print('url',response_index.url)



