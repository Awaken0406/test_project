import datetime
import re
import sys
from playwright.sync_api import Playwright, sync_playwright
import time
import pygame
import os
import random



LIMIT_FLAG_IP = False
LIMIT_FLAG_VISIT = False

def parse_date(from_date,to_date):
  from_obj = datetime.datetime.strptime(from_date, "%Y-%m-%d")
  to_obj = datetime.datetime.strptime(to_date, "%Y-%m-%d")

  start_date = datetime.date(from_obj.year, from_obj.month, from_obj.day)
  end_date = datetime.date(to_obj.year, to_obj.month, to_obj.day)
  delta = end_date - start_date
  if(delta.days <= 0):
     print('时间区间错误date error!!!')
     sys.exit()

def check_html(html):   
    global LIMIT_FLAG_VISIT
    c = re.compile('明日重置',re.S)
    s = re.search(c,html)
    if(s != None):
        LIMIT_FLAG_VISIT = True
        print("visit limit !!!")
        return False
    return True




def PlayMusic(name):
  dir_path = 'D:/SenGe_Code/Muisc/'
  pygame.mixer.music.load(dir_path + name)
  pygame.mixer.music.play()
  print(name,'playing...')




def Login(page): 
    page.goto("https://portal.ustraveldocs.com/?language=Chinese%20(Simplified)&country=China")
    page.wait_for_load_state('networkidle', timeout=30000)
    page.get_by_label("电子邮件").click()
    page.get_by_label("电子邮件").fill(user)
    time.sleep(1)
    page.get_by_label("密码").click()
    page.get_by_label("密码").fill(password)
    time.sleep(1)
    page.get_by_label("*我已经阅读并理解 隐私政策").check()
    time.sleep(1)
    page.get_by_role("button", name="登陆").click()   
    time.sleep(3)  
    page.get_by_text("重新预约").click()
   # page.get_by_text("继续").click()
    time.sleep(3) 
    #page.get_by_role("button", name="确认").click()   
    #time.sleep(3) 
    #page.get_by_role("button", name="继续").click() 
   # time.sleep(3)




#403
#<label class="ctp-checkbox-label"><input type="checkbox"><span class="mark"></span><span class="ctp-label">确认您是真人</span></label>
#响应
def response_event(response,page):

   if(response.status == 403):
        print('response_vent,url',response.url)
        try:
            page.wait_for_event('domcontentloaded')     
            page.wait_for_timeout(7*1000)
       
            # 选择嵌套的 iframe 元素
            iframe_locator = page.locator("iframe")
            # 查找 iframe 元素的 ElementHandle 对象
            iframe_element = iframe_locator.element_handle()
            page2 = iframe_element.content_frame()          
            ckeckbox = page2.locator('input[type=checkbox]')
            ckeckbox.check()
            print('response_event, check checkbox')
            #locator = page.frame_locator("#my-iframe").get_by_text("Submit")
           
        except Exception as e:
           print('response_event 403,not find checkbox!!!',e)
   elif(response.status == 429):
      global LIMIT_FLAG_IP
      LIMIT_FLAG_IP = True
      print('IP limit!!!')


#检查时间
def check_date(html):
    global START_DATE
    global END_DATE
      
    start_obj = datetime.datetime.strptime(START_DATE, '%Y-%m-%d')
    end_obj = datetime.datetime.strptime(END_DATE, '%Y-%m-%d')
      
    com = re.compile('<td><input type="checkbox" name="thePage:SiteTemplate.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(\d+)',re.S)
    result = re.findall(com,html)
    for date_str in result:
        date_obj = datetime.datetime.strptime(date_str[1], '%A %B %d, %Y')
        if date_obj >= start_obj and date_obj <= end_obj:
            print('刷到了恭喜!!!:',date_obj.date())
            return 1
        if date_obj < start_obj:
            print('有更早的日期:',date_obj.date())
            return 2
    return 0


def run(page) -> None:
   # page = context.new_page()
    js = """
        Object.defineProperties(navigator, {webdriver:{get:()=>undefined}});
        """
    page.add_init_script(js)
     # 监听响应事件
    page.on("response", lambda response: response_event(response,page))
    Login(page)
    html = page.content()
    ret = check_date(html)
    if(ret == 1):
      try:
        link_elements = page.query_selector_all('input[type="checkbox"][name*="thePage:SiteTemplate:theForm:"]')   
        for link in reversed(link_elements):
           link.click()
           break
        time.sleep(1)  
       #page.get_by_role("button", name="安排面谈时间").click()   
        PlayMusic('星辰大海.mp3')
        time.sleep(10000)
      except Exception as e:
        PlayMusic('错误.mp3')
        print('nothing',e)
        time.sleep(60)
    elif(ret == 2): 
        try:
          PlayMusic('提醒.mp3')
          time.sleep(10000)
        except Exception as e:
          print('nothing',e)

    check_html(html)      
   

#每半小时登陆一次，如果有预约时间段内就直接抢,如果有更早的时间则选择该时间并停下来等待并通知。
#如果没有则关闭页面,等待下次登陆,一直循环。
#设置特殊时间段，特殊时间段内缩短等待登陆时间 
#设置多开

START_DATE = '2024-1-1'
END_DATE = '2024-2-25'
with sync_playwright() as playwright:
    pygame.init()
    parse_date(START_DATE,END_DATE)
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    while(True):      
      page = context.new_page()
      run(page)      
      page.close()

      if(LIMIT_FLAG_IP):
        print('IP limit Stop !!!')
        break
      if(LIMIT_FLAG_VISIT):
        print('visit limit Stop !!!')
        break
      waitStart = int(random.uniform(25,30))
      print(f'waiting {waitStart}min ...')
      time.sleep(waitStart * 60)

    

    context.close()
    browser.close()


