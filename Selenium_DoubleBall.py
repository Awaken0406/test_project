from selenium import webdriver
from time import sleep
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from lxml import etree
import re
from selenium.webdriver.common import by
from datetime import datetime, timedelta
from collections import defaultdict

class BallData:
     ID = ''
     date = ''
     red = []
     blue = ''

BallDataMap = {}

'''
在 Python 中，类的数据成员（类属性）在类定义中被初始化为可变对象（如列表）时，
这些对象会被所有该类的实例共享。这可能导致在实例化新对象时，类属性的可变对象并不会被重置为空，
而是保留了上一个实例的值。
'''

def ParseSource(html):   
    dataList = html.xpath('/html/body/div[2]/div[3]/div[3]/div/table/tbody/tr')
    for data in reversed(dataList):
         text = data.xpath('.//text()')
         ball = BallData()
         ball.red = []
         ball.ID = text[0]
         ball.date = text[1]
         for i in range(2,8):
              ball.red.append(int(text[i]))
         ball.blue = int(text[8])
         BallDataMap[ball.ID] = ball
    
    
 
def PrintResult():
    RedStatistic = defaultdict(int)
    BlueStatistics = defaultdict(int)

    for data in BallDataMap.values():
         print(f'期数:{data.ID},时间:{data.date},红:{data.red},蓝:[{data.blue}]')
         for num in data.red:
              RedStatistic[num] += 1
         BlueStatistics[data.blue] += 1

    RedStatistic = sorted(RedStatistic.items(), key=lambda x: x[1], reverse=True)
    BlueStatistics = sorted(BlueStatistics.items(), key=lambda x: x[1], reverse=True)
    for num, count in RedStatistic:
        print(f"红:{num} 次数:{count}")
    for num, count in BlueStatistics:
        print(f"蓝:{num} 次数:{count}")
      



def SearchDate(start,end):
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
    ParseSource(html)
   


if __name__ == "__main__":
    
    option = ChromeOptions() 
    option.add_argument('--headless')
    option.add_experimental_option('excludeSwitches',['enable-automation'])
    option.add_experimental_option('useAutomationExtension',False)

    browser = webdriver.Chrome(option)
    browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',{'source' : 'Object.defineProperty(navigator,"webdriver",{get:()=>undefined})'})
    #browser.set_window_size(1366,768)
    #browser.maximize_window()
    browser.get('https://www.zhcw.com/kjxx/ssq/')
    sleep(2)

    GUID = 1000  
    startDate = '2024-01-01'
    endDate = '2024-09-06'

    start = datetime.strptime(startDate,'%Y-%m-%d')
    end = datetime.strptime(endDate,'%Y-%m-%d')
    delta = end - start
    diff = delta.days


    while diff > 90:
            newDate = start + timedelta(days=90)
            SearchDate(start,newDate)
            start = newDate + timedelta(days=1)
            delta = end - start
            diff =  delta.days 

    SearchDate(start,end)
    PrintResult()
    sleep(10)
