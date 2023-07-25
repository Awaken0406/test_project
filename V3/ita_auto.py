import ast
import datetime
import re
import time
from playwright.sync_api import Playwright, sync_playwright, expect
import auto_fill
import mysql_db
from auto_fill import CAccountClass
from playwright.sync_api import Page

def do_it(page:Page):

      #<div class="alert alert-info border-0 rounded-0"> 最早可预约的时间 : 25-07-2023 </div>
       pattern = re.compile(r'<div class="alert alert-info border-0 rounded-0"> 最早可预约的时间 : (.*?) </div>',re.S)
       match = re.search(pattern, page.content())
       date = match.group(1)
       print(date)
       time_date = datetime.datetime.strptime(date, "%d-%m-%Y").date()
       print("日期:%s",time_date)
       page.get_by_role("button", name="继续").click()
       time.sleep(3)
       data = mysql_db.GetAccount(time_date)
       if(date == None):
           return
       print(vars(data))
       auto_fill.fill_data(page, data)
       while(True):
         time.sleep(10000)

def run(playwright: Playwright, data:CAccountClass) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://visa.vfsglobal.com/chn/zh/hun/login")
    page.get_by_placeholder("jane.doe@email.com").click()
    page.get_by_placeholder("jane.doe@email.com").fill(data.account)
    time.sleep(1)
    page.get_by_placeholder("**********").click()
    page.get_by_placeholder("**********").fill(data.password)
    time.sleep(1)
    page.get_by_role("button", name="登录").click()
    time.sleep(5)
    page.get_by_role("button", name="开始新的预约").click()
    time.sleep(3)
    page.locator("#mat-select-value-1").click()
    page.get_by_text("广州匈牙利签证申请中心").click()
    time.sleep(1)
    page.locator("#mat-select-value-3").click() 
    page.get_by_text("短期签证").click()
    time.sleep(1)
    page.locator("div").filter(has_text=re.compile(r"^选择类型$")).nth(2).click()
    page.get_by_text("科学研究").click()
    time.sleep(5)
    #page.get_by_text("最早可预约的时间 : 25-07-2023").click()
   # page.get_by_role("button", name="继续").click()
   # time.sleep(8)
    try:
        do_it(page)
    except Exception as e:
        print(e)

    time.sleep(100000)
    page.close()

    # ---------------------
    context.close()
    browser.close()


def read_config():
    with open('./ita_auto.ini', 'r') as f:
        g_config = f.read()
    config = ast.literal_eval(g_config)
    data = CAccountClass()
    data.account =   config['account']
    data.password = config['password']
    data.sexual  = config['sexual']
    data.name  = config['name']
    data.Sex = config['sex']
    data.phone = config['phone']
    data.mail = config['mail']
    data.passport = config['passport']

    data.start = datetime.datetime.strptime(config['start'], "%Y-%m-%d").date()
    data.end = datetime.datetime.strptime(config['end'], "%Y-%m-%d").date()
    data.birth = datetime.datetime.strptime(config['birth'], "%Y-%m-%d").date()
    data.effective = datetime.datetime.strptime(config['effective'], "%Y-%m-%d").date()#有效期
    return data



data = read_config()
with sync_playwright() as playwright:
    run(playwright,data)





   
