import datetime
import json
import re
import sys
from playwright.sync_api import Playwright, sync_playwright, expect
import time
import pygame
import os
import random
import tkinter as tk


user = '' 
password = ''

def Login(page): 
    page.goto("https://portal.ustraveldocs.com/?language=Chinese%20(Simplified)&country=China")
    page.get_by_label("电子邮件").click()
    page.get_by_label("电子邮件").fill(user)
    time.sleep(2)
    page.get_by_label("密码").click()
    page.get_by_label("密码").fill(password)
    time.sleep(2)
    page.get_by_label("*我已经阅读并理解 隐私政策").check()
    time.sleep(1)
    page.get_by_role("button", name="登陆").click()   
    time.sleep(3)  
    #page.get_by_text("重新预约").click()
    page.get_by_text("继续").click()
    time.sleep(30) 


def modify_post_request(route, request,time_list):
    # 获取原始请求的payload参数
    payload =  request.post_data
    # 判断是否为需要拦截的POST请求数据
    if request.method == 'POST' and payload and 'selectedDate' in payload:
    
      # 修改指定字段的值
      #  payload_dict['selectedDate'] = '01/31/2024'

        #date = "01%2F30%2F2024"
        date = random.choice(time_list)
        print('select date',date.replace('%2F', '/'))
        # 使用正则表达式匹配 selectedDate 的值，并将其替换为新的值
        payload = re.sub(r'(selectedDate=)[^&]+', r'\g<1>' + date, payload)
        route.continue_(method=request.method, headers=request.headers, post_data=payload)

        #No appointments are available for 11/01/2023.

    else:
        # 不需要拦截，直接继续请求
        route.continue_()



def parse_html(html):
      com = re.compile('<input type="checkbox" name="thePage:SiteTemplate:theForm.*?<td>(.*?)</td><td>(.*?)</td><td>(\d+)</td>',re.S)
      result = re.findall(com,html)
      if(len(result) > 0):
        for date_str in result:
          print(date_str)
        return True
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


def run(playwright: Playwright,time_list) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    js = """
        Object.defineProperties(navigator, {webdriver:{get:()=>undefined}});
        """
    page.add_init_script(js)
    Login(page)
    page.route('https://portal.ustraveldocs.com/scheduleappointment',lambda route: modify_post_request(route,route.request,time_list))

    while( True):
      page.get_by_role("link", name="30").click()  
      random_number = int(random.uniform(30, 60))
      print('wait',random_number,'s')
      time.sleep(random_number)
      if(parse_html(page.content())):
         page.unroute('https://portal.ustraveldocs.com/scheduleappointment')
         PlayMusic()
         break


    time.sleep(1000)
    # ---------------------
    page.close()
    context.close()
    browser.close()





with sync_playwright() as playwright:
    time_list = pase_date('2023-11-20','2023-11-30')
    run(playwright,time_list)


  #1) <a href="#" class="ui-state-default">30</a> aka get_by_role("link", name="30")
  #  2) <span class="ui-state-default">30</span> aka get_by_role("row", name="24 25 26 27 28 29 30").get_by_text("30")
  #  3) <td>08:30</td> aka get_by_role("cell", name="08:30")
