from playwright.sync_api import Page
import time



class CAccountClass:
  def __init__(self):
    self.sexual  = ''
    self.name  = ''
    self.sex = ''
    self.phone = '' 
    self.mail = ''
    self.passport = ''
    self.start = '' 
    self.end = '' 
    self.birth = ''
    self.effective = ''


def fill_data(page:Page,data:CAccountClass):
    page.get_by_placeholder("请输入名", exact=True).click()
    page.get_by_placeholder("请输入名", exact=True).fill(data.sexual)
    page.get_by_placeholder("请输入名.").click()
    page.get_by_placeholder("请输入名.").fill(data.name)

    


    page.get_by_placeholder("输入护照号").click()
    page.get_by_placeholder("输入护照号").fill(data.passport)
    #page.locator(".col-12 > app-input-control > div > .mat-form-field > .mat-form-field-wrapper > .mat-form-field-flex > .mat-form-field-infix").first.click()
    page.get_by_placeholder("44").fill("86")
    page.get_by_placeholder("012345648382").click()
    page.get_by_placeholder("012345648382").fill(data.phone)
    page.get_by_placeholder("输入邮箱地址").click()
    page.get_by_placeholder("输入邮箱地址").click()
    page.get_by_placeholder("输入邮箱地址").fill(data.mail)

"""
    page.locator("#mat-select-value-9").click()  
    page.get_by_text("中国").click()
    page.locator("#mat-select-value-7").click()
    if data.sex == 1:
        page.get_by_text("男性").click()
    else:
        page.get_by_text("女性").click()

    page.locator("app-ngb-datepicker").filter(has_text="出生日期*").locator("div").nth(3).click()
    time.sleep(0.5)
    page.get_by_role("combobox", name="Select month").select_option(str(data.birth.month))
    page.get_by_role("combobox", name="Select year").select_option(str(data.birth.year))
    page.get_by_role("gridcell", name=str(data.birth.strftime("%A, %B %d, %Y"))).get_by_text(str(data.birth.day)).click()

    page.locator("app-ngb-datepicker").filter(has_text="护照有效期*").locator("div").nth(3).click()
    time.sleep(0.5)
    page.get_by_role("combobox", name="Select month").select_option(str(data.effective.month))
    page.get_by_role("combobox", name="Select year").select_option(str(data.effective.year))
    #page.get_by_text(str(data.effective.day), exact=True).click()
    page.get_by_role("gridcell", name=str(data.effective.strftime("%A, %B %d, %Y"))).get_by_text(str(data.effective.day)).click()
    """

