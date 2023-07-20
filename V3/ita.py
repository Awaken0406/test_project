import re
import sys
from playwright.sync_api import Playwright, sync_playwright, expect
import time
import requests
from playwright.sync_api import Page

USER = 'SenGeMail@163.com'
PASSWORD = 'Qq734697554@'

#USER = '2428721828@qq.com'
#PASSWORD = 'Kbh123456@'



# 定义API配置
params = {
        'num': 1,
        'pt': 1,
        'sep': 1,
        'dedup':1,
        'secret_id': 'oo28ceg7wvkkb7dcaxxx',
        'signature': 'cqve9xl1u4vpyqq677g1a4j313qno16u',
    }
api = 'https://dps.kdlapi.com/api/getdps/'

# 通过API获取代理
def get_proxy():
    global api
    global params

    r = requests.get(api,params)
    if r.status_code == 200:
        proxy = {
            "server": f'http://{r.text}',
            "username": "d2304848217",
            "password": "9an858x3",
            } 
        return proxy
    else:
        return None




def run(page:Page) -> None:
 
    js = """
        Object.defineProperties(navigator, {webdriver:{get:()=>undefined}});
        """
    page.add_init_script(js)
    page.goto("https://visa.vfsglobal.com/chn/zh/ita/login")
    page.wait_for_load_state("domcontentloaded")
    time.sleep(3)
  #  page.get_by_role("button", name="Accept Cookies").click()
    page.get_by_placeholder("jane.doe@email.com").click()
    page.get_by_placeholder("jane.doe@email.com").fill(USER)
    page.get_by_placeholder("**********").click()
    time.sleep(1)
    page.get_by_placeholder("**********").fill(PASSWORD)
    time.sleep(3)
    page.get_by_role("button", name="登录").click()
    time.sleep(3)
    page.get_by_role("button", name="开始新的预约").click()
    time.sleep(1)


    page.locator("#mat-select-value-1").click()
    page.get_by_text("广州意大利签证申请中心").click()
    time.sleep(1)
    page.locator("#mat-select-value-3").click()
    page.get_by_text("SchenGen visa").click()
    time.sleep(1)
    time.sleep(3)
    
    content = page.content()
    c = re.compile('很抱歉，目前没有可预约时段',re.S)
    s = re.search(c,content)
    if(s != None):
        print("目前没有可预约时段")
    else:
       print(content)
       while(True):
         time.sleep(100)


if __name__ == "__main__":
 with sync_playwright() as playwright:   
    proxy = None
    index =0
    while(True):    
        if(index % 3 == 0):
            proxy = get_proxy()
        index += 1
        if proxy == None:
            sys.exit()
        print("proxy=",proxy['server'])
        browser = playwright.chromium.launch(headless=False,proxy=proxy)
        context = browser.new_context()
        page = context.new_page()
        try:
            run(page)
        except Exception as e:
           print('error',e)               
        page.close()
        context.close()
        browser.close()
        time.sleep(60 * 1)
