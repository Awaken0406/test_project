import ast
import datetime
import json
import os
import random
import re
import sys
from playwright.sync_api import Playwright, sync_playwright, expect
import time
import pygame
import requests
from playwright.sync_api import Page
import logging
import mysql_db
import auto_fill
from mysql_db import CProxyData

USER = ''
PASSWORD = ''

IP_LIMIT = False


def read_config():
    with open('./deu.ini', 'r') as f:
        g_config = f.read()

    global USER
    global PASSWORD
    config = ast.literal_eval(g_config)
    USER =   config['account']
    PASSWORD = config['password']

#USER = '2428721828@qq.com'
#PASSWORD = 'Kbh123456@'
logger = {}
def init_log():
  global logger
  logger = logging.getLogger()
  logger.setLevel(logging.INFO)

# 创建控制台 handler
  console_handler = logging.StreamHandler()
  console_handler.setLevel(logging.INFO)


# 创建文件 handler
  file_handler = logging.FileHandler('deu_log.log')
  file_handler.setLevel(logging.INFO)

# 指定日志记录格式
  formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
  console_handler.setFormatter(formatter)
  console_handler.encoding = 'utf-8'
  file_handler.setFormatter(formatter)

# 将 handler 添加到 logger 中
  logger.addHandler(console_handler)
  logger.addHandler(file_handler)





def get_proxy(proxyData:mysql_db.CProxyData):

    params = {
        'num': 1,
        'pt': 1,
        'sep': 1,
        'dedup':1,
        'secret_id': proxyData.secret_id,
        'signature': proxyData.signature,
    }
    api = 'https://dps.kdlapi.com/api/getdps/'

    count_params = {
          'secret_id': proxyData.secret_id,
          'signature': proxyData.signature,
        } 
    r = requests.get('https://dps.kdlapi.com/api/getipbalance',count_params)
    if r.status_code == 200:
        data = json.loads(r.text)
        value = data['data']['balance']
        logger.info('剩余IP:%s',value)

    r = requests.get(api,params)
    if r.status_code == 200:
        ip = r.text
        proxy = {
            "server": f'http://{ip}',
            "username": proxyData.proxy_name,
            "password": proxyData.proxy_password,
            } 
                 
        time_params = {
          'secret_id': proxyData.secret_id,
          'signature': proxyData.signature,
          'proxy' : r.text
        }
        r = requests.get('https://dps.kdlapi.com/api/getdpsvalidtime',time_params)
        if(r.status_code == 200):
            data = json.loads(r.text)
            value = data['data'][ip]
            current_time = datetime.datetime.now()
            delta = datetime.timedelta(seconds=int(value))
            future_time = current_time + delta   
            formatted_time = future_time.strftime('%Y-%m-%d %H:%M:%S')
            future_time = datetime.datetime.strptime(formatted_time, '%Y-%m-%d %H:%M:%S')
            logger.info('IP:%s,有效时长:%d min,持续到:%s',ip,int(int(value) / 60),future_time)
           
        
        return proxy
    else:
        return None

def PlayMusic(name):
  try:
    dir_path = './Muisc/'
    pygame.mixer.music.load(dir_path + name)
    pygame.mixer.music.play()
    logger.info('%s playing...',name)
  except Exception as e:
        logger.info('Muisc error %s',e)




def response_event(response,page):
   logger.info('response_event,status=%d,url=%s,',response.status,response.url)
   if(response.status == 429 and 'https://lift-apicn.vfsglobal.com/appointment/CheckIsSlotAvailable' in requests.url):
        logger.info('response_event 429,ip limit,url=%s',response.url)
        global IP_LIMIT
        IP_LIMIT = True


def do_it(page:Page):

      #<div class="alert alert-info border-0 rounded-0"> 最早可预约的时间 : 25-07-2023 </div>
       pattern = re.compile(r'<div class="alert alert-info border-0 rounded-0"> 最早可预约的时间 : (.*?) </div>',re.S)
       match = re.search(pattern, page.content())
       date = match.group(1)
       time_date = datetime.datetime.strptime(date, "%d-%m-%Y").date()
       logging.info("最早可预约的时间:%s",time_date)
       page.get_by_role("button", name="继续").click()
       time.sleep(3)

       data = mysql_db.GetAccount_deu(time_date)
       if(date == None):
          logging.info('没有符合日期的')
          return


       try:
          logging.info('收取验证码的邮箱:%s',USER)
          birthDate =datetime.datetime.strftime(datetime.datetime.strptime(data.birth, '%Y-%m-%d'), '%Y-%m-%d %b')
          effectiveDate =datetime.datetime.strftime(datetime.datetime.strptime(data.effective, '%Y-%m-%d'), '%Y-%m-%d %b')
          logging.info('姓名:%s %s,性别:%s,护照号:%s,有效期:%s,出生日期:%s',data.sexual,data.name,data.sex,data.passport,birthDate,effectiveDate)
          auto_fill.fill_data(page, data)
       except Exception as e:
          logging.info('%s',e)

       while(True):
         time.sleep(10000)

def run(page:Page) -> None:
 
    js = """
        Object.defineProperties(navigator, {webdriver:{get:()=>undefined}});
        """
    page.add_init_script(js)
   # page.on("response", lambda response: response_event(response,page))
    page.goto("https://visa.vfsglobal.com/chn/zh/deu/login")
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
    page.get_by_text("德国签证申请中心 - 广州").click()
    time.sleep(7)
 #   page.locator("#mat-select-value-3").click()
 #   page.get_by_text("SchenGen visa").click()
  
    content = page.content()
    #c = re.compile('很抱歉，目前没有可预约时段',re.S)
    c = re.compile('最早可预约的时间',re.S)
    s = re.search(c,content)
    count = 0
    while(s == None and count < 23):
        page.locator("#mat-select-value-1").click()
        page.get_by_text("德国签证申请中心 - 南京").click()#
        time.sleep(1)
        page.locator("#mat-select-value-1").click()
        page.get_by_text("德国签证申请中心 - 广州").click()
        count +=1
        logger.info('load count =%d',count)
        page.wait_for_load_state('load')
        time.sleep(5)
        content = page.content()
        s = re.search(c,content)
 

    if(s == None):
        logger.info("目前没有可预约时段")
    else:  
        try:
            PlayMusic('星辰大海.mp3')
            do_it(page)
        except Exception as e:
            logger.info('do_it,%s',e) 



if __name__ == "__main__":
 with sync_playwright() as playwright:
    init_log()   
    read_config()
    pygame.init()
    proxyData = mysql_db.GetProxyData()
    index =0
    while(True):    
        #if(index % 3 == 0):
        proxy = get_proxy(proxyData)
       # index += 1
        if proxy == None:
            logger.info('没有代理了')
            sys.exit()
        logger.info("proxy=%s",proxy['server'])
        browser = playwright.chromium.launch(headless=False,proxy=proxy)
        context = browser.new_context()
        page = context.new_page()
        try:
            run(page)
        except Exception as e:
           logger.info('error %s',e)    
           
        page.close()
        context.close()
        browser.close()
        IP_LIMIT = False    
        time.sleep(5)
