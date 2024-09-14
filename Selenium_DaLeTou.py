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
import random

class BallData:
     ID = ''
     date = ''
     front = []
     after = []
     hit = 0
     hitAdd = 0
     duplicates_red = {}
     duplicates_blue = {}

BallDataMap = {}
BallDataList = []

RedTotalTimes = defaultdict(int)
BlueTotalTimes = defaultdict(int)

    
 
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
         BallDataList.append(ball)
         tt = datetime.strptime(ball.date,'%Y-%m-%d').date()
         if tt < tempDate:
              tempDate = tt
    return tempDate



def Analyse():
     global RedTotalTimes
     global BlueTotalTimes
     global BallDataList
     BallDataList = BallDataList[::-1]
     redExistCount = 0
     blueExistCount = 0
     for i in range(len(BallDataList)):
          ball = BallDataList[i]
          id = 0
          ball.duplicates_red = {}
          ball.duplicates_blue = {}
          for num in range(i+1,i+1+nearNum):
                    if(num >= len(BallDataList)):
                         break
                    id += 1
                    set1 = set(ball.front)
                    set2 = set(BallDataList[num].front)
                    duplicates = set1.intersection(set2)
                    if len(duplicates) > 0:
                         ball.duplicates_red[id] = list(duplicates)
                         redExistCount += 1
                    set1 = set(ball.after)
                    set2 = set(BallDataList[num].after)
                    duplicates = set1.intersection(set2)
                    if len(duplicates) > 0:
                         ball.duplicates_blue[id] = list(duplicates)
                         blueExistCount += 1

     
     redNum = defaultdict(int)
     redTimes = defaultdict(int)
     blueTimes = defaultdict(int)
     for data in BallDataList:    
          for k,numList in data.duplicates_red.items():
               redNum[len(numList)]+=1
               redTimes[k]+=1
          for k,numList in data.duplicates_blue.items():
               blueTimes[k]+=1

          #print(f'ID:{data.ID},date:{data.date},red:{data.red},blue:[{data.blue}]')
          #print('red',data.duplicates_red)
          print('blue',data.duplicates_blue)
     
          for num in data.front:
               RedTotalTimes[num] += 1
          for num in data.after:
               BlueTotalTimes[num] += 1
     print(f'Total:{len(BallDataList)},redExistCount:{redExistCount},blueExistCount:{blueExistCount}')
     RedTotalTimes = sorted(RedTotalTimes.items(), key=lambda x: x[1], reverse=True)
     BlueTotalTimes = sorted(BlueTotalTimes.items(), key=lambda x: x[1], reverse=True)

     len1 = int(len(RedTotalTimes)/2)
     len2 = int(len(BlueTotalTimes)/2)
     index1 = 0
     index2 = 0
     for num, count in RedTotalTimes: 
          index1+=1
          if index1 > len1:
               break
          redTopKeys.append(num)
     for num, count in BlueTotalTimes: 
          index2+=1
          if index2 > len2:
               break
          blueTopKeys.append(num)

     print(f'total:{len(BallDataList)},nearNum:{nearNum},redNum:{redNum},redTimes:{redTimes},blueTimes:{blueTimes}')
     print("RedTotalTimes:",RedTotalTimes)
     print("BlueTotalTimes:",BlueTotalTimes)
     print("redTopKeys:",redTopKeys)     
     print("blueTopKeys:",blueTopKeys)   
   


def Recommend():
     redFilterNumber = []
     blueFilterNumber = []
     filterCountTT = filterCount = 3
     recommendCount = 3

     for ball in BallDataList:    
          if filterCount == 0:
               break
          filterCount -= 1
          redFilterNumber += ball.front

     bluefilterCountTT = bluefilterCount = 2
     for ball in BallDataList:    
          if bluefilterCount == 0:
               break
          bluefilterCount -= 1
          blueFilterNumber += ball.after
     redFilterNumber = list(set(redFilterNumber))
     blueFilterNumber = list(set(blueFilterNumber))
     print(f'RedfilterCount:{filterCountTT},BluefilterCount:{bluefilterCountTT},filter_red:{redFilterNumber},filter_blue:{blueFilterNumber}')

     recommend_red = []
     recommend_blue = []
     current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
     with open(f'./OutPut/DaLeTou_Recommend.txt', "a",encoding="utf-8") as file:
           
       print(f'recommend:{current_time_str}')    
       file.write(f'recommend:{current_time_str}\n')
       for i in range(recommendCount):
          recommend_red = []
          recommend_blue = []
          while True:
               sleep(0.2)
               t = int(time.time() * 10000000)
               random.seed(t)
               num = random.randint(1, 35)
               if num not in recommend_red: #and num in redTopKeys:
                    if len(redFilterNumber)+len(recommend_red) <  len(redTopKeys):
                         if num not in redFilterNumber:
                              recommend_red.append(num)
                    else:
                         recommend_red.append(num)
               if(len(recommend_red) == 5):
                    break

          while True:
               sleep(0.2)
               t = int(time.time() * 10000000)
               random.seed(t)
               num = random.randint(1, 12)
               if num not in recommend_blue:
                    if num not in blueFilterNumber:
                         recommend_blue.append(num)
                    if(len(recommend_blue) == 2):
                         break
          recommend_red.sort()
          recommend_blue.sort()
          print(f"{recommend_red}--{recommend_blue}")
          file.write(f"{recommend_red}--{recommend_blue}\n")
       file.write("\n")
     file.close()

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
    nearNum = 5
    redTopKeys = []
    blueTopKeys = []

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

    #PrintResult()
    Analyse()
    Recommend()
