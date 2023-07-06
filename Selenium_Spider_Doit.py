import time
import re
import tesserocr
from selenium import webdriver
from io import BytesIO
from PIL import Image
from retrying import retry
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import numpy as np
from selenium.webdriver import ChromeOptions


def preprocess(image):
    image = image.convert('L')
    array = np.array(image)
    array = np.where(array > 100,255,0)
    image = Image.fromarray(array.astype('uint8'))
    return image

@retry(stop_max_attempt_number=10, retry_on_result=lambda x:x is False)
def login(browser):
    browser.get('https://captcha7.scrape.center/')
    browser.find_element(By.CSS_SELECTOR,'.username input[type="text"]').send_keys('admin')
    browser.find_element(By.CSS_SELECTOR,'.password input[type="password"]').send_keys('admin')
    captcha = browser.find_element(By.CSS_SELECTOR,'#captcha')
    image = Image.open(BytesIO(captcha.screenshot_as_png))
    image = preprocess(image)
    captcha = tesserocr.image_to_text(image)
    captcha = re.sub('[^a-zA-Z0-9]','',captcha)#清除字母数字以外的字符
    print('image='+captcha)
    browser.find_element(By.CSS_SELECTOR,'.captcha input[type="text"]').send_keys(captcha)
    browser.find_element(By.CSS_SELECTOR,'.login').click()

    try: 
        WebDriverWait(browser,10).until(EC.presence_of_element_located((By.XPATH,'//h2[contains(.,"登录成功")]')))
        print(browser.page_source)
        print("登录成功")
        time.sleep(2)
        browser.close() 
        return True
    except TimeoutException:
        return  False

if __name__ =='__main__':
    option = ChromeOptions()
    option.add_argument('--headless')
    browser = webdriver.Chrome(option)

    login(browser)
