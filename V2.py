import datetime
import re
import sys
from playwright.sync_api import Playwright, sync_playwright
import time
import pygame
import os
import random
import logging



#新增监听响应并获取日期，并选择日期
USER = ''
PASSWORD = ''  
START_DATE = '' 
END_DATE = '' 
CONFIRM_COUNT = 0
LIMIT_FLAG_IP = False
LIMIT_FLAG_VISIT = False
DATE_LIST = []
TRY_DATE = None
logger = {}
WAIT_BASE = 20



def parse_date(from_date,to_date):
  from_obj = datetime.datetime.strptime(from_date, "%Y-%m-%d")
  to_obj = datetime.datetime.strptime(to_date, "%Y-%m-%d")

  start_date = datetime.date(from_obj.year, from_obj.month, from_obj.day)
  end_date = datetime.date(to_obj.year, to_obj.month, to_obj.day)
  delta = end_date - start_date
  if(delta.days <= 0):
     logger.info('时间区间错误date error!!!')
     sys.exit()

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




def Login(page): 
    page.goto("https://portal.ustraveldocs.com/?language=Chinese%20(Simplified)&country=China")
    page.wait_for_load_state('networkidle', timeout=30000)
    page.get_by_label("电子邮件",).click()
    page.get_by_label("电子邮件").fill(USER)
    time.sleep(1)
    page.get_by_label("密码").click()
    page.get_by_label("密码").fill(PASSWORD)
    time.sleep(1)
    page.get_by_label("*我已经阅读并理解 隐私政策").check()
    time.sleep(1)
    page.get_by_role("button", name="登陆").click()   
    time.sleep(5)  
    page.wait_for_event('domcontentloaded')
    if(CONFIRM_COUNT == 0):#第一次预约还没预约到时间的
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
      text = response.text()
      # 匹配日期字符串
      date_pattern = re.compile(r"\d{1,2}-\d{1,2}-\d{4}")
      date_list = date_pattern.findall(text)
      global DATE_LIST
      for date in date_list:
        time = datetime.datetime.strptime(date, "%d-%m-%Y")
        DATE_LIST.append(time)
        logger.info("%s",time.date())


#检查时间
def check_time(html):
    global START_DATE
    global END_DATE
    global USER
      
    start_obj = datetime.datetime.strptime(START_DATE, '%Y-%m-%d')
    end_obj = datetime.datetime.strptime(END_DATE, '%Y-%m-%d')
      
    com = re.compile('<td><input type="checkbox" name="thePage:SiteTemplate.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(\d+)',re.S)
    result = re.findall(com,html)
    for date_str in result:
        date_obj = datetime.datetime.strptime(date_str[1], '%A %B %d, %Y')
        if date_obj >= start_obj and date_obj <= end_obj:
            logger.info('%s',f'恭喜:"{USER}"抢到号!!!,时间{date_obj.date()}')
            return 1
        if date_obj < start_obj:
            logger.info('有更早的日期:%s',date_obj.date())
            return 2
    return 0

#检查日期
def check_date(page):  
    global START_DATE
    global END_DATE
    global DATE_LIST
    global TRY_DATE
    start = datetime.datetime.strptime(START_DATE, "%Y-%m-%d")
    end = datetime.datetime.strptime(END_DATE, "%Y-%m-%d")
    for date in DATE_LIST:
       if(date >= start and date <= end):
            logger.info("有想要的时间了!!! %s",date.date())
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
def Confirm(page):
    try:
        link_elements = page.query_selector_all('input[type="checkbox"][name*="thePage:SiteTemplate:theForm:"]')   
        for link in reversed(link_elements):
           link.click()
           break
        time.sleep(1) 
        global CONFIRM_COUNT
        if(CONFIRM_COUNT == 0):
           page.get_by_role("button", name="安排面谈时间").click()   
        PlayMusic('星辰大海.mp3')
        time.sleep(10000)
    except Exception as e:
        PlayMusic('错误.mp3')
        logger.info('other error %s',e)
        time.sleep(300)

def run(page) -> None:
   # page = context.new_page()
    js = """
        Object.defineProperties(navigator, {webdriver:{get:()=>undefined}});
        """
    page.add_init_script(js)
     # 监听响应事件
    page.on("response", lambda response: response_event(response,page))
    try:
      Login(page)
    except Exception as e:
       logging.info('error login : %s',e)
       return

    page.route('https://portal.ustraveldocs.com/scheduleappointment',lambda route: modify_post_request(route,route.request))

    global DATE_LIST

    html = page.content()
    ret = check_time(html)
    if(ret == 1): #有就直接确认  
        Confirm(page)
        logger.info('流程1')
    elif(ret == 2): 
        while(len(DATE_LIST) <= 0):
            logger.info('wait DATE_LIST')
            time.sleep(1)
        #再往后检查一下
        logger.info('流程2')
        if(check_date(page)):
            logger.info('流程3')
            html = page.content()
            #再次检查时间
            s = check_time(html)
            if(s == 1):
                logger.info('流程4')
                Confirm(page)
        else:
            PlayMusic('提醒.mp3')
            time.sleep(10000)
         
    check_html(html)      
   




def read_config():
  with open('./config.ini', 'r') as f:
      g_config = f.read()
  user_match = re.search(r"USER\s*=\s*'(.*)'", g_config)
  password_match = re.search(r"PASSWORD\s*=\s*'(.*)'", g_config)
  start_date_match = re.search(r"START_DATE\s*=\s*'(.*)'", g_config)
  end_date_match = re.search(r"END_DATE\s*=\s*'(.*)'", g_config)
  CONFIRM_COUNT_match = re.search(r"CONFIRM_COUNT\s*=\s*'(.*)'", g_config)
  WAIT_BASE_match = re.search(r"WAIT_BASE\s*=\s*'(.*)'", g_config)

  global USER
  global PASSWORD
  global START_DATE
  global END_DATE
  global CONFIRM_COUNT
  global WAIT_BASE

  USER = user_match.group(1)
  PASSWORD = password_match.group(1)
  START_DATE = start_date_match.group(1)
  END_DATE = end_date_match.group(1)
  CONFIRM_COUNT = int(CONFIRM_COUNT_match.group(1))
  WAIT_BASE = int(WAIT_BASE_match.group(1))
  if(WAIT_BASE < 6):
     WAIT_BASE = 6
  logger.info('%s %s %s %s %s,%s', USER, PASSWORD, START_DATE, END_DATE, CONFIRM_COUNT,WAIT_BASE)



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


if __name__ == "__main__":
  with sync_playwright() as playwright:
    init_log()
    pygame.init()
    read_config()
    parse_date(START_DATE,END_DATE)
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    round = 1
    while(True):  
      logger.info('第%d轮...',round)
      round += 1    
      page = context.new_page()
      run(page)      
      page.close()
      DATE_LIST.clear()
      TRY_DATE = None

      if(LIMIT_FLAG_IP):
        logger.info('IP limit Stop !!!')
        break
      if(LIMIT_FLAG_VISIT):
        logger.info('visit limit Stop !!!')
        break
      waitStart = int(random.uniform(WAIT_BASE,WAIT_BASE+5))
      logger.info('%s',f'waiting {waitStart}min ...')
      time.sleep(waitStart * 60)

    

    context.close()
    browser.close()


