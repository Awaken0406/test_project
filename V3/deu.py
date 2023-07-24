import ast
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
  logger.setLevel(logging.DEBUG)

# 创建控制台 handler
  console_handler = logging.StreamHandler()
  console_handler.setLevel(logging.DEBUG)


# 创建文件 handler
  file_handler = logging.FileHandler('deu_log.log')
  file_handler.setLevel(logging.DEBUG)

# 指定日志记录格式
  formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
  console_handler.setFormatter(formatter)
  console_handler.encoding = 'utf-8'
  file_handler.setFormatter(formatter)

# 将 handler 添加到 logger 中
  logger.addHandler(console_handler)
  logger.addHandler(file_handler)



secret_id = 'o3jriybjgabkw9s4ttmo'
signature = 'cck1v6kn2to5ms1qaisjatzpf7lyt92b'
proxy_name = 'd2704271743'
proxy_password = '9an858x3'
# 定义API配置
params = {
        'num': 1,
        'pt': 1,
        'sep': 1,
        'dedup':1,
        'secret_id': secret_id,
        'signature': signature,
    }
api = 'https://dps.kdlapi.com/api/getdps/'


def get_proxy():
    global api
    global params

    count_params = {
          'secret_id': secret_id,
          'signature': signature,
        } 
    r = requests.get('https://dps.kdlapi.com/api/getipbalance',count_params)
    if r.status_code == 200:
        logger.info(r.text)

    r = requests.get(api,params)
    if r.status_code == 200:
        proxy = {
            "server": f'http://{r.text}',
            "username": proxy_name,
            "password": proxy_password,
            } 
        
             
        time_params = {
          'secret_id': secret_id,
          'signature': signature,
          'proxy' : r.text
        }
        r = requests.get('https://dps.kdlapi.com/api/getdpsvalidtime',time_params)
        if(r.status_code == 200):
           logger.info(r.text)
        
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
       page.get_by_role("button", name="继续").click()
       PlayMusic('星辰大海.mp3')
       while(True):
         time.sleep(10000)




if __name__ == "__main__":
 with sync_playwright() as playwright:
    init_log()   
    read_config()
    pygame.init()
    proxy = None
    index =0
    while(True):    
        #if(index % 3 == 0):
        proxy = get_proxy()
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
