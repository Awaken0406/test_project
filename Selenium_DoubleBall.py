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
     ID = ''
     date = ''
     red = []
     blue = 0
     duplicates_red = {}
     duplicates_blue = {}

BallDataMap = {}
BallDataList = []
RedTotalTimes = defaultdict(int)
BlueTotalTimes = defaultdict(int)

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
         BallDataList.append(ball)#默认升序


def Analyse():
     global RedTotalTimes
     global BlueTotalTimes
     for i in range(len(BallDataList)):#默认升序
          ball = BallDataList[i]
          id = 0
          ball.duplicates_red = {}
          for num in range(i+1,i+1+nearNum):
                    if(num >= len(BallDataList)):
                         break
                    id += 1
                    set1 = set(ball.red)
                    set2 = set(BallDataList[num].red)
                    duplicates = set1.intersection(set2)
                    if len(duplicates) > 0:
                         ball.duplicates_red[id] = list(duplicates)

     blueExistCount = 0
     for i in range(len(BallDataList)):
          ball = BallDataList[i]
          id = 0
          ball.duplicates_blue = {}
          for num in range(i+1,i+1+nearNum):
                    if(num >= len(BallDataList)):
                         break
                    id += 1
                    if ball.blue == BallDataList[num].blue:
                         ball.duplicates_blue[id] = ball.blue
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

          print(f'ID:{data.ID},date:{data.date},red:{data.red},blue:[{data.blue}]')
          #print('red',data.duplicates_red)
          print('blue',data.duplicates_blue)
     
          for num in data.red:
               RedTotalTimes[num] += 1
          BlueTotalTimes[data.blue] += 1
     print(f'Total:{len(BallDataList)},blueExistCount:{blueExistCount}')
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
     recommendCount = 100

     for ball in reversed(BallDataList):    
          if filterCount == 0:
               break
          filterCount -= 1
          redFilterNumber += ball.red

     bluefilterCountTT = bluefilterCount = 5
     for ball in reversed(BallDataList):    
          if bluefilterCount == 0:
               break
          bluefilterCount -= 1
          blueFilterNumber.append(ball.blue)
     redFilterNumber = list(set(redFilterNumber))
     blueFilterNumber = list(set(blueFilterNumber))
     print(f'RedfilterCount:{filterCountTT},BluefilterCount:{bluefilterCountTT},filter_red:{redFilterNumber},filter_blue:{blueFilterNumber}')

     recommend_red = []
     recommend_blue = []
     current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
     with open(f'./OutPut/DoubleBall_Recommend_V2.txt', "a",encoding="utf-8") as file:
           
       print(f'recommend:{current_time_str}')    
       file.write(f'recommend:{current_time_str}\n')
       for i in range(recommendCount):
          recommend_red = []
          recommend_blue = []
          while True:
               sleep(0.2)
               t = int(time.time() * 10000000)
               random.seed(t)
               num = random.randint(1, 33)
               if num not in recommend_red:
                    if num in redTopKeys:
                         recommend_red.append(num)         
                    else:           
                         if num in redFilterNumber:
                              boolNum = random.randint(1,2)
                              if boolNum == 2:
                                  recommend_red.append(num)    
                         else:
                              recommend_red.append(num)   
                         
               if(len(recommend_red) == 6):
                    break

          while True:
               sleep(0.2)
               t = int(time.time() * 10000000)
               random.seed(t)
               num = random.randint(1, 16)
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

def PrintResult():
     global RedTotalTimes
     global BlueTotalTimes
     with open(f'./OutPut/DoubleBall_{startDate}_{endDate}.txt', "w",encoding="utf-8") as file:
          for data in BallDataMap.values():
               info = f'ID:{data.ID},date:{data.date},red:{data.red},blue:[{data.blue}]'
               print(info)
               file.write(info+'\n')

          for num, count in RedTotalTimes:
               info = f"rd:{num} times:{count}"
               file.write(info+'\n')
          print("***********************************")
          file.write("***********************************"+'\n')
          for num, count in BlueTotalTimes:        
               info = f"blue:{num} times:{count}"
               file.write(info+'\n')
     file.close()
      





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
    browser.maximize_window()
    browser.get('https://www.zhcw.com/kjxx/ssq/')
    sleep(2)
    t = int(time.time() * 10000000)
    random.seed(t)

    redTopKeys = []
    blueTopKeys = []

    nearNum = 5
    startDate = '2024-01-01'
    endDate = datetime.now().date().strftime('%Y-%m-%d')

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
    #PrintResult()
    Analyse()
    Recommend()
    for i in range(3):
         index = random.randint(2, 101)
         print("index",index)
