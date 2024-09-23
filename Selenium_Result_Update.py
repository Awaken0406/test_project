from collections import defaultdict
import re
import Selenium_DoubleBall
import math
from selenium import webdriver
from time import sleep
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from lxml import etree
import re
from selenium.webdriver.common import by
from datetime import datetime, timedelta
from collections import defaultdict
import random
import time

class BallData:
        ID = 0
        date = ''
        red = []
        blue = 0
        duplicates_red = {}
        duplicates_blue = {}

        def __init__(self, ID, date, red, blue):
            self.ID = ID
            self.date = date
            self.red = red
            self.blue = blue
        def __lt__(self, other):
            return (self.ID) < (other.ID)

def create_ball_data_from_string(data_str):
   
    match = re.match( r'(\d+)\s(\d{4}-\d{2}-\d{2})\s\[(\d+(?:,\s\d+)*)\]--\[(\d+)\]', data_str)
    if match:
        ID = int(match.group(1))
        date = match.group(2)
        red = [int(num) for num in match.group(3).split(',')]
        blue = int(match.group(4))
        return BallData(ID, date, red, blue)
    else:
        return None

def remove_chinese_chars(input_str):
    # 使用正则表达式匹配中文字符
    chinese_pattern = re.compile("[\u4e00-\u9fa5（）]+")
    # 使用 sub 方法替换中文字符为空字符串
    result = chinese_pattern.sub('', input_str)
    
    return result


def LoadFile(fileName):
    AllDataMap ={}
    with open(fileName, 'r',encoding="utf-8") as file:
        content = file.readlines()
    
    for line in content:
        if 'recommend' in line or line == '\n':
            continue

        data = create_ball_data_from_string(line)
        AllDataMap[data.ID] =data
    file.close()
    return AllDataMap




def SearchDate(browser,start,end,BallDataList):
    custom = browser.find_element(by.By.XPATH,'/html/body/div[2]/div[3]/div[2]/div[1]/div/div[1]/strong')
    custom.click()
    sleep(1)
    t = browser.find_element(by.By.XPATH,'/html/body/div[2]/div[3]/div[2]/div[1]/div/div[2]/div[1]/div[3]')
    t.click()
    sleep(1)

    starInput = browser.find_element(by.By.XPATH,'//*[@id="startC"]')
    starInput.clear()
    starInput.send_keys(start.strftime('%Y-%m-%d'))
    endInput =  browser.find_element(by.By.XPATH,'//*[@id="endC"]')
    endInput.clear()
    endInput.send_keys(end.strftime('%Y-%m-%d'))
    search = browser.find_element(by.By.XPATH,'/html/body/div[2]/div[3]/div[2]/div[1]/div/div[2]/div[4]/div[2]/div[2]')
    search.click()
    sleep(2) 
    html =etree.HTML(browser.page_source)
    ParseSource(html,BallDataList)

def ParseSource(html,BallDataList):   
    dataList = html.xpath('/html/body/div[2]/div[3]/div[3]/div/table/tbody/tr')
    for data in reversed(dataList):
         text = data.xpath('.//text()')
         ball = BallData(int(text[0]), text[1], [], 0)
         for i in range(2,8):
              ball.red.append(int(text[i]))
         ball.blue = int(text[8])
         BallDataList.append(ball)#默认升序
   
def GetHtml(startDate):
    option = ChromeOptions() 
    option.add_argument('--headless')
    option.add_experimental_option('excludeSwitches',['enable-automation'])
    option.add_experimental_option('useAutomationExtension',False)

    browser = webdriver.Chrome(option)
    browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',{'source' : 'Object.defineProperty(navigator,"webdriver",{get:()=>undefined})'})
    #browser.set_window_size(1366,768)
    browser.maximize_window()
    browser.get('https://www.zhcw.com/kjxx/ssq/')
    sleep(2)

    
    endDate = datetime.now().date().strftime('%Y-%m-%d')

    start = datetime.strptime(startDate,'%Y-%m-%d')
    end = datetime.strptime(endDate,'%Y-%m-%d')
    delta = end - start
    diff = delta.days

    BallDataList = []
    while diff > 90:
            newDate = start + timedelta(days=90)
            SearchDate(browser,start,newDate,BallDataList)
            start = newDate + timedelta(days=1)
            delta = end - start
            diff =  delta.days 

    SearchDate(browser,start,end,BallDataList)
    return BallDataList


def GetFileDate(dateStr):
    AllDataMap = LoadFile('./OutPut/DoubleBallData.txt')

    keys_to_delete = []
    startDate = datetime.strptime(dateStr,'%Y-%m-%d')
    for key, value in AllDataMap.items():
        date = datetime.strptime(value.date,'%Y-%m-%d')
        if date < startDate:
            keys_to_delete.append(key)

    for key in keys_to_delete:
        del AllDataMap[key]
    return AllDataMap

if __name__ == "__main__":
    
    AllDataMap = LoadFile('./OutPut/DoubleBallData.txt')
    DataList = GetHtml('2024-09-20')
    for data in DataList:
        data.date = remove_chinese_chars(data.date)
        AllDataMap[data.ID] = data
        #AllDataMap[data.ID] = BallData(data.ID,data.date,data.red,data.blue)
    
    AllDataMap = dict(sorted(AllDataMap.items(), key=lambda x: x[1]))
    with open('./OutPut/DoubleBallData.txt', 'w',encoding="utf-8") as file:
        for key, value in AllDataMap.items(): 
            file.write(f'{value.ID} {value.date} {value.red}--[{value.blue}]\n')

