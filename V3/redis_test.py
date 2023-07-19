import ast
from redis import StrictRedis
import re
import datetime
import time

import pickle
from datetime import date
from playwright.sync_api import Playwright, sync_playwright
#https://github.com/tporadowski/redis/releases

response = """        var myDayHash = new Array();
            myDayHash['16-1-2023'] = true;
            myDayHash['19-1-2024'] = true;
            myDayHash['24-1-2024'] = true;
            myDayHash['25-1-2024'] = true;
            myDayHash['26-1-2024'] = true;

        var ofcAptDateStr = null;ofcAptDateStr = ''; """
regex = r'\d{1,2}-\d{1,2}-\d{4}'
dates = re.findall(regex,   response)
#if(len(dates) > 0):
  #  print('响应',dates)

list = []
for d in dates:
    obj = datetime.datetime.strptime(d, "%d-%m-%Y")
    print(obj.date())
    list.append((obj.date()))

redis = StrictRedis(host='localhost',port=6379,db=0,password=None)
redis.set('name','Bob')
serialized_dates = pickle.dumps(list)
redis.set('date',serialized_dates)

#serialized_dates2 = redis.get('name2')
#my_dates = pickle.loads(serialized_dates2)
#print('name2',my_dates)




my_dict = {'key1': 'value1', 'key2': 'value2'}
my_dict['key3'] = 'value3'





# 将字符串转换为 Python 对象

with open('D:/code/V3/config.ini','r') as f:
    my_string = f.read()

config = ast.literal_eval(my_string)
print(config['account'])

date_pattern = re.compile("{(.*?)}",re.S)
date_list = date_pattern.findall(my_string)
print(date_list)




for i in range(2):
     with sync_playwright() as playwright:
      browser = playwright.chromium.launch(headless=False)
      context = browser.new_context()
      page = context.new_page()
      page.goto("https://www.baidu.com")
      time.sleep(3)
   
      page.close()
      context.close()
      browser.close()
