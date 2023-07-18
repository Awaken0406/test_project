import ast
import datetime
import re
import sys
from playwright.sync_api import Playwright, sync_playwright
import time
import pygame
import os
import random
import logging
import pickle
from redis import StrictRedis

class CAccountClass:
   def __init__(self, account,password,start,end,count):
      self.account = account
      self.password = password
      self.start = start
      self.end = end
      self.confirmCount = count
      self.effective = True

#新增监听响应并获取日期，并选择日期

LIMIT_FLAG_IP = False
LIMIT_FLAG_VISIT = False
TRY_DATE = None
logger = {}
WAIT_BASE = 30
DATE_LIST = []
redisdb = StrictRedis(host='localhost',port=6379,db=0,password=None)
DB_KEY = 'date'
FINISH = False

def check_html(html):   
    global LIMIT_FLAG_VISIT
    c = re.compile('明日重置',re.S)
    s = re.search(c,html)
    if(s != None):
        LIMIT_FLAG_VISIT = True
        logger.info("visit limit !!!")
        return False
    return True




def PlayMusic(name):
  try:
    dir_path = './Muisc/'
    pygame.mixer.music.load(dir_path + name)
    pygame.mixer.music.play()
    logger.info('%s playing...',name)
  except Exception as e:
        logger.info('Muisc error %s',e)




def Login(page,data:CAccountClass): 
    page.goto("https://portal.ustraveldocs.com/?language=Chinese%20(Simplified)&country=China")
    page.wait_for_load_state('networkidle', timeout=30000)
    page.get_by_label("电子邮件",).click()
    page.get_by_label("电子邮件").fill(data.account)
    time.sleep(1)
    page.get_by_label("密码").click()
    page.get_by_label("密码").fill(data.password)
    time.sleep(1)
    page.get_by_label("*我已经阅读并理解 隐私政策").check()
    time.sleep(1)
    page.get_by_role("button", name="登陆").click()   
    time.sleep(5)  
    page.wait_for_event('domcontentloaded')
    if(data.confirmCount == 0):#第一次预约还没预约到时间的
      page.get_by_text("继续").click()
      time.sleep(3) 
      page.get_by_role("button", name="确认").click()   
      time.sleep(3) 
      page.get_by_role("button", name="继续").click() 
    else:
      page.get_by_text("重新预约").click()
    time.sleep(3) 


def modify_post_request(route, request):
  try:
    # 获取原始请求的payload参数
    payload =  request.post_data
    # 判断是否为需要拦截的POST请求数据
    if request.method == 'POST' and payload and 'selectedDate' in payload:
        global TRY_DATE
        if(TRY_DATE == None):
           logger.info('Error TRY_DATE is None!!!')
           return
        date = TRY_DATE
      # 修改指定字段的值
      #  payload_dict['selectedDate'] = '01/31/2024'
        #date = "01%2F30%2F2024"   
        date_str = date.strftime("%m/%d/%Y")
        date_str = date_str.replace('/', '%2F')
        logger.info('select date %s',date_str.replace('%2F', '/'))
        # 使用正则表达式匹配 selectedDate 的值，并将其替换为新的值
        payload = re.sub(r'(selectedDate=)[^&]+', r'\g<1>' + date_str, payload)
        route.continue_(method=request.method, headers=request.headers, post_data=payload)

        #No appointments are available for 11/01/2023.

    else:
        # 不需要拦截，直接继续请求
        route.continue_()
  except Exception as e:
    logger.info('modify_post_request error %s',e)


#403
#<label class="ctp-checkbox-label"><input type="checkbox"><span class="mark"></span><span class="ctp-label">确认您是真人</span></label>
#响应
def response_event(response,page):

   if(response.status == 403):
        logger.info('response_event,url=%s',response.url)
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
            logger.info('response_event, check checkbox')
            #locator = page.frame_locator("#my-iframe").get_by_text("Submit")
           
        except Exception as e:
           logger.info('response_event 403,not find checkbox!!! %s',e)
   elif(response.status == 429):
      global LIMIT_FLAG_IP
      LIMIT_FLAG_IP = True
      logger.info('IP limit!!!')
   elif(response.status == 200 and 'https://portal.ustraveldocs.com/scheduleappointment' in response.url):
    try:
      text = response.text()
      global DATE_LIST
      global redisdb
      # 匹配日期字符串
      date_pattern = re.compile(r"\d{1,2}-\d{1,2}-\d{4}")
      date_list = re.findall(date_pattern,text)
      list = []
      for date in date_list:
        time = datetime.datetime.strptime(date, "%d-%m-%Y")
        logger.info("%s",time.date())
        list.append(str(time.date()))
        DATE_LIST.append(time.date())
      if(len(list) > 0):
        #serialized_dates = pickle.dumps(list)
        redisdb.set(DB_KEY,str(list))
        logger.info('写入日期')
        global FINISH
        FINISH = True
    except Exception as e:
       logger.info('error print date,%s',e)


#检查时间
def check_time(html,data:CAccountClass):

    
    com = re.compile('<td><input type="checkbox" name="thePage:SiteTemplate.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(\d+)',re.S)
    result = re.findall(com,html)
    for date_str in result:
        date_obj = datetime.datetime.strptime(date_str[1], '%A %B %d, %Y')
        date_obj = date_obj.date()
        if date_obj >= data.start and date_obj <= data.end:
            logger.info('%s',f'恭喜:"{data.account}"抢到号!!!,时间{date_obj}')
            return 1
        if date_obj < data.start:
            logger.info('有更早的日期:%s',date_obj)
            return 2
    return 0

#检查日期
def check_date(page,data:CAccountClass):  

    global DATE_LIST
    global TRY_DATE
    for date in DATE_LIST:
       if(date >= data.start and date <= data.end):
            logger.info("有想要的时间了!!! %s",date)
            TRY_DATE = date
            link_elements = page.query_selector_all('td[onclick*="DP_jQuery_"]')   
            for link in link_elements:
                if(link.is_enabled()):
                    link.hover() 
                    link.click()
                    break       
            time.sleep(3)
            return True
    return False
          
      
#确认时间
def Confirm(page,data:CAccountClass,list):
    try:
        link_elements = page.query_selector_all('input[type="checkbox"][name*="thePage:SiteTemplate:theForm:"]')   
        for link in reversed(link_elements):
           link.click()
           break
        time.sleep(1) 
        if(data.confirmCount == 0):
           page.get_by_role("button", name="安排面谈时间").click()
           list.remove(data)  
        PlayMusic('星辰大海.mp3')
        time.sleep(10000)
    except Exception as e:
        PlayMusic('错误.mp3')
        logger.info('other error %s',e)
        time.sleep(300)

def run(page,data:CAccountClass,list) -> None:
   # page = context.new_page()
    js = """
        Object.defineProperties(navigator, {webdriver:{get:()=>undefined}});
        """
    page.add_init_script(js)
     # 监听响应事件
    page.on("response", lambda response: response_event(response,page))
    try:
      Login(page,data)
    except Exception as e:
       logging.info('error login : %s',e)
       return

    page.route('https://portal.ustraveldocs.com/scheduleappointment',lambda route: modify_post_request(route,route.request))

    global DATE_LIST

    html = page.content()
    ret = check_time(html,data)
    if(ret == 1): #有就直接确认  
        Confirm(page,data,list)
        logger.info('流程1')
    elif(ret == 2): 
        while(len(DATE_LIST) <= 0):
            logger.info('wait DATE_LIST')
            time.sleep(1)
        #再往后检查一下
        logger.info('流程2')
        if(check_date(page,data)):
            logger.info('流程3')
            html = page.content()
            #再次检查时间
            s = check_time(html,data)
            if(s == 1):
                logger.info('流程4')
                Confirm(page,data,list)
        else:
            PlayMusic('提醒.mp3')
            time.sleep(10000)
    count = 10
    while(FINISH == False and count > 0):
        time.sleep(3) 
        count -= 1 
    check_html(html)      
   




def read_config():
    with open('./config.ini', 'r') as f:
        g_config = f.read()


    date_pattern = re.compile("{(.*?)}",re.S)
    date_list = date_pattern.findall(g_config)

    list = []
    for item in date_list:
        item = item.replace("'", "")
        account, password,start,end,count = item.split(':')
        strat_obj = datetime.datetime.strptime(start, "%Y-%m-%d")
        end_obj = datetime.datetime.strptime(end, "%Y-%m-%d")
        if(strat_obj > end_obj):
            logger.info('时间区间错误date error!!!')
            sys.exit()
        list.append(CAccountClass(account,password,strat_obj.date(),end_obj.date(),int(count)))
    return list
  



def init_log():
  global logger
  logger = logging.getLogger()
  logger.setLevel(logging.DEBUG)

# 创建控制台 handler
  console_handler = logging.StreamHandler()
  console_handler.setLevel(logging.DEBUG)


# 创建文件 handler
  file_handler = logging.FileHandler('message.log')
  file_handler.setLevel(logging.DEBUG)

# 指定日志记录格式
  formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
  console_handler.setFormatter(formatter)
  console_handler.encoding = 'utf-8'
  file_handler.setFormatter(formatter)

# 将 handler 添加到 logger 中
  logger.addHandler(console_handler)
  logger.addHandler(file_handler)


def check_redis_data(list):
   global redisdb
   global DB_KEY
   date_list_str = redisdb.get(DB_KEY).decode('utf-8') 
   if date_list_str == None:
        return False,None,None
   
   date_list = ast.literal_eval(date_list_str)
   for account_data in list:
      for d in date_list:
         date = datetime.datetime.strptime(d, "%Y-%m-%d")
         date = date.date()
         if date >= account_data.start and date <= account_data.end:
            return True,account_data,date
         
   return False,None,None



if __name__ == "__main__":
  with sync_playwright() as playwright:
    init_log()
    pygame.init()
    if redisdb.ping() == False:
       logger.info('Could not establish Redis connection')
       sys.exit()
    list = read_config()
    if len(list) <= 0:
       sys.exit()

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    temp = context.new_page()
    round = 1
    index =0
    data = None
    find_db_data = False
    while(True):  
      if(find_db_data == False):
           data = list[index]
      logger.info('第%d轮,account=%s',round,data.account)
      round += 1    
      
      page = context.new_page()
      run(page,data,list)      
      page.close()
      TRY_DATE = None
      DATE_LIST.clear()
      find_db_data = False
      FINISH = False
      if(LIMIT_FLAG_IP):
        logger.info('IP limit Stop !!!')
        PlayMusic('提醒.mp3')
        break
      if(LIMIT_FLAG_VISIT):
        logger.info('visit limit Stop !!!')
        list.remove(data)
        PlayMusic('提醒.mp3')
      if len(list) <= 0:
        sys.exit()
      index += 1
      if index >= len(list):
         index = 0

      waitSecond =  WAIT_BASE * 60 / len(list)
      logger.info('%s',f'waiting {waitSecond}s {waitSecond / 60}min ...')

      while(waitSecond > 0):   
        time.sleep(1)
        waitSecond -= 1
        ret,data ,date= check_redis_data(list)
        if ret:
            logger.info("redisdb find date,account=%s,date=%s",data.account,date)
            find_db_data = True
            break
        
    time.sleep(60)      
    context.close()
    browser.close()
