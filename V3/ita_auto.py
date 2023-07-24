import ast
import datetime
import re
import time
from playwright.sync_api import Playwright, sync_playwright, expect


class CAccountClass:
  def __init__(self):
    self.account = ''
    self.password = ''
    self.sexual  = ''
    self.name  = ''
    self.Sex = ''
    self.phone = '' 
    self.mail = ''
    self.passport = ''
    self.start = '' 
    self.end = '' 
    self.birth = ''
    self.effective = ''


def fill_data(page,data:CAccountClass):
    page.get_by_placeholder("请输入名", exact=True).click()
    page.get_by_placeholder("请输入名", exact=True).fill(data.sexual)
    page.get_by_placeholder("请输入名.").click()
    page.get_by_placeholder("请输入名.").fill(data.name)
    page.locator("#mat-select-value-7").click()
    if data.Sex == 1:
        page.get_by_text("男性").click()
    else:
        page.get_by_text("女性").click()

    page.locator("app-ngb-datepicker").filter(has_text="出生日期*").locator("div").nth(3).click()
    page.get_by_role("combobox", name="Select month").select_option(str(data.birth.month))
    page.get_by_role("combobox", name="Select year").select_option(str(data.birth.year))
    page.get_by_text(str(data.birth.day), exact=True).click()
    
    page.locator("#mat-select-value-9").click()  
    page.get_by_text("中国").click()

    page.get_by_placeholder("输入护照号").click()
    page.get_by_placeholder("输入护照号").fill(data.passport)
    #page.locator(".col-12 > app-input-control > div > .mat-form-field > .mat-form-field-wrapper > .mat-form-field-flex > .mat-form-field-infix").first.click()
    page.get_by_placeholder("44").fill("86")
    page.get_by_placeholder("012345648382").click()
    page.get_by_placeholder("012345648382").fill(data.phone)
    page.get_by_placeholder("输入邮箱地址").click()
    page.get_by_placeholder("输入邮箱地址").click()
    page.get_by_placeholder("输入邮箱地址").fill(data.mail)


    page.locator("app-ngb-datepicker").filter(has_text="护照有效期*").locator("div").nth(3).click()
    page.get_by_role("combobox", name="Select month").select_option(str(data.effective.month))
    page.get_by_role("combobox", name="Select year").select_option(str(data.effective.year))
    #page.get_by_text(str(data.effective.day), exact=True).click()
    page.get_by_role("gridcell", name=str(data.effective.strftime("%A, %B %d, %Y"))).get_by_text(str(data.effective.day)).click()

    """ 
    page.get_by_role("button", name="保存").click()
    page.get_by_role("button", name="继续").click()
    page.get_by_text("24日").click()
    page.get_by_role("cell", name="9649702 选择").get_by_label("选择选择").check()
    page.get_by_role("button", name="继续").click()
    page.locator("label").filter(has_text="我接受").click()
    page.locator("#mat-checkbox-2 > .mat-checkbox-layout > .mat-checkbox-inner-container").click()
    page.get_by_role("button", name="确认").click()
    """

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
    page.get_by_role("button", name="继续").click()
    time.sleep(8)
    try:
        fill_data(page,data)
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
    data.start.day
    return data



data = read_config()
with sync_playwright() as playwright:
    run(playwright,data)





   
