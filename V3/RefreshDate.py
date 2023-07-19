import datetime
import re
import sys
from playwright.sync_api import Playwright, sync_playwright
import time
import pygame
import os
import random
import logging
from redis import StrictRedis
import re
import datetime
import pickle




LIMIT_FLAG_IP = False
LIMIT_FLAG_VISIT = False
LIMIT_ACCOUNT = False
logger = {}
WAIT_BASE = 30
FINISH = False


redisdb = StrictRedis(host='localhost',port=6379,db=0,password=None)

class CDateClass:
   def __init__(self, account,password):
      self.account = account
      self.password = password
      self.effective = True


def check_html(html):   
    global LIMIT_FLAG_VISIT
    global LIMIT_ACCOUNT
    c = re.compile('明日重置',re.S)
    s = re.search(c,html)
    if(s != None):
        LIMIT_FLAG_VISIT = True
        logger.info("visit limit !!!")
    
    c = re.compile('Your account has been frozen',re.S)
    s = re.search(c,html)
    if(s != None):
        LIMIT_ACCOUNT = True
        logger.info("account limit !!!")
 
  



def Login(page,account,password): 
    page.goto("https://portal.ustraveldocs.com/?language=Chinese%20(Simplified)&country=China")
    page.wait_for_load_state('networkidle', timeout=30000)
    page.get_by_label("电子邮件",).click()
    page.get_by_label("电子邮件").fill(account)
    time.sleep(1)
    page.get_by_label("密码").click()
    page.get_by_label("密码").fill(password)
    time.sleep(1)
    page.get_by_label("*我已经阅读并理解 隐私政策").check()
    time.sleep(1)
    page.get_by_role("button", name="登陆").click()   
    time.sleep(5)  
    page.wait_for_event('domcontentloaded')
    page.get_by_text("重新预约").click()
    time.sleep(3) 




#403
#<label class="ctp-checkbox-label"><input type="checkbox"><span class="mark"></span><span class="ctp-label">确认您是真人</span></label>
#响应
def response_event(response,page):
  # logger.info('response_event,url=%s',response.url)
   if(response.status == 403):
        logger.info('response_event 403,url=%s',response.url)
        try:
            page.wait_for_event('domcontentloaded')     
       
            # 选择嵌套的 iframe 元素
            iframe_locator = page.locator("iframe")
            # 查找 iframe 元素的 ElementHandle 对象
            iframe_element = iframe_locator.element_handle()
            page2 = iframe_element.content_frame()          
            ckeckbox = page2.locator('input[type=checkbox]')
            ckeckbox.check()
            logger.info('response_event, check checkbox')
            #locator = page.frame_locator("#my-iframe").get_by_text("Submit")
           
        except Exception as e:
           logger.info('response_event 403,not find checkbox!!! %s',e)
   elif(response.status == 429):
      global LIMIT_FLAG_IP
      LIMIT_FLAG_IP = True
      logger.info('IP limit!!!')
   elif(response.status == 200 and 
        ('https://portal.ustraveldocs.com/scheduleappointment' in response.url)):
      text = response.text()
      global redisdb
      # 匹配日期字符串
      date_pattern = re.compile(r"\d{1,2}-\d{1,2}-\d{4}")
      date_list = re.findall(date_pattern,text)
      list = []
      for date in date_list:
        time = datetime.datetime.strptime(date, "%d-%m-%Y")
        logger.info("%s",time.date())
        list.append(str(time.date()))
      if(len(list) > 0):
        #serialized_dates = pickle.dumps(list)
        redisdb.set('date',str(list))
        logger.info('写入日期')
        global FINISH
        FINISH = True



def run(page,account,password):
    js = """
        Object.defineProperties(navigator, {webdriver:{get:()=>undefined}});
        """
    page.add_init_script(js)
     # 监听响应事件
    page.on("response", lambda response: response_event(response,page))
    try:
      Login(page,account,password)
      try:
          page.wait_for_selector("随便测试", timeout=1000).click()
      except:
         logging.info('测试')
      count = 2
      while(FINISH == False and count > 0):
        time.sleep(3) 
        count -= 1
    except Exception as e:
       logging.info('error login : %s',e)
       return
    
    check_html(page.content())   






def read_config():
    with open('./refresh_config.ini','r') as f:
        info = f.read()
    my_list = eval(info)
    list = []
    for item in my_list:
        account, password = item.split(':')
        list.append(CDateClass(account,password))

    return list


def init_log():
  global logger
  logger = logging.getLogger()
  logger.setLevel(logging.DEBUG)

# 创建控制台 handler
  console_handler = logging.StreamHandler()
  console_handler.setLevel(logging.DEBUG)


# 创建文件 handler
  file_handler = logging.FileHandler('refresh_date_log.log')
  file_handler.setLevel(logging.DEBUG)

# 指定日志记录格式
  formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
  console_handler.setFormatter(formatter)
  console_handler.encoding = 'utf-8'
  file_handler.setFormatter(formatter)

# 将 handler 添加到 logger 中
  logger.addHandler(console_handler)
  logger.addHandler(file_handler)



def PlayMusic(name):
  try:
    dir_path = './Muisc/'
    pygame.mixer.music.load(dir_path + name)
    pygame.mixer.music.play()
    logger.info('%s playing...',name)
  except Exception as e:
        logger.info('Muisc error %s',e)

   
  

if __name__ == "__main__":
  with sync_playwright() as playwright:
    if redisdb.ping() == False:
       logger.info('Could not establish Redis connection')
       sys.exit()
    init_log()
    pygame.init()
    account_list = read_config()
    if len(account_list) <= 0:
       logger.info('account is null')
       sys.exit()  

    index = 0
    round = 1
    while(True):
      data = account_list[index]  
      logger.info('round=%d,account=%s',round,data.account)
      round += 1
      browser = playwright.chromium.launch(headless=False)
      context = browser.new_context()
      page = context.new_page()

      run(page,data.account,data.password)      
      page.close()
      context.close()
      browser.close()

      FINISH = False
      if(LIMIT_FLAG_IP):
        logger.info('IP limit Stop !!!')
        PlayMusic('提醒.mp3')
        break
      if(LIMIT_FLAG_VISIT):
        logger.info('visit limit !!!,remove:%s',data.account)
        account_list.remove(data)
        PlayMusic('提醒.mp3')
      elif(LIMIT_ACCOUNT):
        logger.info('account limit !!!,remove:%s',data.account)
        account_list.remove(data)
        PlayMusic('提醒.mp3')
      
      LIMIT_FLAG_VISIT = False
      LIMIT_ACCOUNT = False
      index += 1
      if index >= len(account_list):
         index = 0
      add = random.uniform(1,5)
      waitSecond =  WAIT_BASE * 60 / len(account_list)
      waitSecond += add
      logger.info('%s',f'account len:{len(account_list)}  waiting {waitSecond}s {waitSecond / 60}min ...')
      time.sleep(waitSecond)
   

    time.sleep(60)
   
