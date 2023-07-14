import datetime
import json
import re
import sys
from playwright.sync_api import Playwright, sync_playwright
import time
import pygame
import os
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


user = 
password = 
LIMIT_FLAG_IP = False
LIMIT_FLAG_VISIT = False

body = '内容'
def SendMail():
  # 邮件发送方的邮箱地址和邮箱密码
  sender_email = 'SenGeMail@163.com'
  sender_password = 'TKTHLXRKIFHWZRXY'
  # 邮件接收方的邮箱地址
  recipient_email = '734697554@qq.com'
  # 邮件主题和内容
  subject = '邮件通知'

  # 创建 MIMEMultipart 对象，用于组合邮件主体和附件

  message = MIMEMultipart()
  message['Subject'] = subject
  message['From'] = sender_email
  message['To'] = recipient_email
  # 添加邮件正文
  global body
  message.attach(MIMEText(body))
  with smtplib.SMTP_SSL('smtp.163.com', 465) as server:
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, recipient_email, message.as_string())



def parse_html(html):

      com = re.compile('<input type="checkbox" name="thePage:SiteTemplate:theForm.*?<td>(.*?)</td><td>(.*?)</td><td>(\d+)</td>',re.S)
      result = re.findall(com,html)
      global body
      if(len(result) > 0):
        body = result
        for date_str in result:
          print(date_str)
        return True
      
      global LIMIT_FLAG_VISIT
      c = re.compile('明日重置',re.S)
      s = re.search(c,html)
      if(s != None):
        LIMIT_FLAG_VISIT = True
        print("visit limit !!!")
        return False
      return False



def pase_date(from_date,to_date):
  from_obj = datetime.datetime.strptime(from_date, "%Y-%m-%d")
  to_obj = datetime.datetime.strptime(to_date, "%Y-%m-%d")

  start_date = datetime.date(from_obj.year, from_obj.month, from_obj.day)
  end_date = datetime.date(to_obj.year, to_obj.month, to_obj.day)
  delta = end_date - start_date
  if(delta.days <= 0):
     print('date error!!!')
     sys.exit()

  time_list =[]
  for i in range(delta.days):
      date = start_date + datetime.timedelta(days=i)
      date_str = date.strftime("%m/%d/%Y")
      date_str = date_str.replace('/', '%2F')
      time_list.append(date_str)
  return time_list
      


def PlayMusic():
  dir_path = 'D:/Users/chenyongsen/Music/'
  file_names = [f for f in os.listdir(dir_path) if not f.startswith('!!!')]
  pygame.init()
  name = random.choice(file_names)
  pygame.mixer.music.load(dir_path + name)
  pygame.mixer.music.play()
  print(name,'playing...')


def my_function():
    static_var = -1
    def increment_static_var():
          nonlocal static_var
          static_var += 1
          return static_var
    return increment_static_var

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
    #page.get_by_text("重新预约").click()
    page.get_by_text("继续").click()
    time.sleep(3) 
    page.get_by_role("button", name="确认").click()   
    time.sleep(3) 
    page.get_by_role("button", name="继续").click() 
    time.sleep(3)

def modify_post_request(route, request,time_list,func):
    # 获取原始请求的payload参数
    payload =  request.post_data
    # 判断是否为需要拦截的POST请求数据
    if request.method == 'POST' and payload and 'selectedDate' in payload:
    
      # 修改指定字段的值
      #  payload_dict['selectedDate'] = '01/31/2024'
        #date = "01%2F30%2F2024"   
        #date = random.choice(time_list)
        time_len = len(time_list)
        count = func() % time_len
        date = time_list[count]
        print('select date',date.replace('%2F', '/'))
        # 使用正则表达式匹配 selectedDate 的值，并将其替换为新的值
        payload = re.sub(r'(selectedDate=)[^&]+', r'\g<1>' + date, payload)
        route.continue_(method=request.method, headers=request.headers, post_data=payload)

        #No appointments are available for 11/01/2023.

    else:
        # 不需要拦截，直接继续请求
        route.continue_()



#403
#<label class="ctp-checkbox-label"><input type="checkbox"><span class="mark"></span><span class="ctp-label">确认您是真人</span></label>

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
      



def run(page,time_list) -> None:
   # page = context.new_page()
    js = """
        Object.defineProperties(navigator, {webdriver:{get:()=>undefined}});
        """
    page.add_init_script(js)
     # 监听响应事件
    page.on("response", lambda response: response_event(response,page))
    Login(page)
    func = my_function()
    page.route('https://portal.ustraveldocs.com/scheduleappointment',lambda route: modify_post_request(route,route.request,time_list,func))


    waitTime = 0
    refreshTime = int(random.uniform(120, 150))
    while( True):
      #<td class=" " onclick="DP_jQuery_1689243664265.datepicker._selectDay('#datepicker',1,2024, this);return false;"><a class="ui-state-default" href="#">20</a></td>
      link_elements = page.query_selector_all('td[onclick*="DP_jQuery_"]')   
      for link in link_elements:
        if(link.is_enabled()):
           link.hover() 
           link.click()
           break
           
      random_number = int(random.uniform(50, 80))
      waitTime += random_number
      print('random time',random_number,'s')
      time.sleep(random_number)
      if(parse_html(page.content())):
        try:
          page.unroute('https://portal.ustraveldocs.com/scheduleappointment')
          SendMail()
          PlayMusic()
        except Exception as e:
          print('nothing',e)
        break   
      #print('waitTime:',waitTime,"refreshTime:",refreshTime)
      if waitTime >= refreshTime:     
       # print('refresh page')
       # page.reload()  
        waitTime = 0
        refreshTime = int(random.uniform(120, 150))

    time.sleep(1000)
    # ---------------------
    page.close()






with sync_playwright() as playwright:
    time_list = pase_date('2023-11-20','2023-11-30')
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    while(True):
      try:
        page = context.new_page()
        run(page,time_list)   
      except TimeoutError as e:
        print(f"TimeoutError: {e}")
        page.close()
      except Exception as e:
        print(f"An error occurred: {e}")
        page.close()     


      if(LIMIT_FLAG_IP):
        print('IP limit Stop !!!')
        break
      if(LIMIT_FLAG_VISIT):
        print('visit limit Stop !!!')
        break
      waitStart = int(random.uniform(120,180))
      print(f'waiting {waitStart}s ...')
      time.sleep(waitStart)

    

    context.close()
    browser.close()
