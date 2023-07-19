import re
from playwright.sync_api import Playwright, sync_playwright, expect
import time

USER = 'SenGeMail@163.com'
PASSWORD = 'Qq734697554@'
logger = {}

#USER = '2428721828@qq.com'
#PASSWORD = 'Kbh123456@'

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
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
    page.get_by_text("D Visa and Study").click()
    time.sleep(1)
    page.locator("#mat-select-value-3").click()
    page.get_by_text("D Visa and Study").click()
    page.wait_for_event('networkidle')
    time.sleep(3)
    
    context = page.context()
    c = re.compile('明日重置',re.S)
    s = re.search(c,context)
    if(s != None):
        LIMIT_FLAG_VISIT = True
        logger.info("visit limit !!!")
    while(True):
        time.sleep(100)
    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
