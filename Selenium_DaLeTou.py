from selenium import webdriver
from time import sleep
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from lxml import etree
import re
from selenium.webdriver.common import by
from datetime import datetime, timedelta
from collections import defaultdict
import time

class BallData:
     ID = ''
     date = ''
     front = []
     after = []
     hit = 0
     hitAdd = 0

BallDataMap = {}



    
 
def PrintResult():
     RedStatistic = defaultdict(int)
     BlueStatistics = defaultdict(int)
     endDate = datetime.now().date()
     with open(f'./OutPut/DaLeTou_{startDate}_{endDate}.txt', "w",encoding="utf-8") as file:
          for data in BallDataMap.values():
               info = f'期数:{data.ID},时间:{data.date},前区:{data.front},后区:{data.after},基本注数:{data.hit},追加注数:{data.hitAdd}'
               print(info)
               file.write(info+'\n')
               for num in data.front:
                    RedStatistic[num] += 1
               for num in data.after:
                    BlueStatistics[num] += 1

          RedStatistic = sorted(RedStatistic.items(), key=lambda x: x[1], reverse=True)
          BlueStatistics = sorted(BlueStatistics.items(), key=lambda x: x[1], reverse=True)
          for num, count in RedStatistic:
               info = f"前区:{num} 次数:{count}"
               print(info)
               file.write(info+'\n')
          print("***********************************")
          file.write("***********************************"+'\n')
          for num, count in BlueStatistics:        
               info = f"后区:{num} 次数:{count}"
               print(info)
               file.write(info+'\n')
     file.close()
      


def ParseSource(html):   
    dataList = html.xpath('//*[@id="historyData"]/tr')
    tempDate = datetime.now().date()
    skip_remaining = False
    for data in dataList:

         if skip_remaining == True:
               skip_remaining = False
               continue
         
         text = data.xpath('.//text()')
         ball = BallData()
         ball.front = []
         ball.after = []
         ball.ID = text[0]
         ball.date = text[1]

         if text[2] == '派奖':
               skip_remaining = True
               continue

         for i in range(2,7):
              ball.front.append(int(text[i]))
         ball.after.append(int(text[7]))
         ball.after.append(int(text[8]))
         ball.hit = int(text[9])
         ball.hitAdd = int(text[11])
         BallDataMap[ball.ID] = ball
         tt = datetime.strptime(ball.date,'%Y-%m-%d').date()
         if tt < tempDate:
              tempDate = tt
    return tempDate


if __name__ == "__main__":
    
    option = ChromeOptions() 
    option.add_argument('--headless')
    option.add_experimental_option('excludeSwitches',['enable-automation'])
    option.add_experimental_option('useAutomationExtension',False)

    browser = webdriver.Chrome(option)
    browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',{'source' : 'Object.defineProperty(navigator,"webdriver",{get:()=>undefined})'})
    #browser.set_window_size(1366,768)
    browser.maximize_window()
    browser.get('https://www.lottery.gov.cn/kj/kjlb.html?dlt')
    sleep(2)
 
    startDate = '2024-01-01'

    start = datetime.strptime(startDate,'%Y-%m-%d').date()
    child_frame = browser.find_element(by.By.XPATH,'//*[@id="iFrame1"]')
    browser.switch_to.frame(child_frame)


    while True:
          sleep(1)

          html =etree.HTML(browser.page_source)
          tt = ParseSource(html)
          if tt <= start:
               break
          nextBtn = browser.find_element(by.By.XPATH,'/html/body/div/div/div[3]/ul/li[13]')
          nextBtn.click()

    PrintResult()
    sleep(2)
