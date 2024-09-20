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
import Selenium_Recommend_Analyse

class BallData:
     ID = 0
     date = ''
     red = []
     blue = 0
     duplicates_red = {}
     duplicates_blue = {}

     def __lt__(self, other):
          return (self.ID) < (other.ID)



'''
在 Python 中，类的数据成员（类属性）在类定义中被初始化为可变对象（如列表）时，
这些对象会被所有该类的实例共享。这可能导致在实例化新对象时，类属性的可变对象并不会被重置为空，
而是保留了上一个实例的值。
'''

def ParseSource(html,BallDataList):   
    dataList = html.xpath('/html/body/div[2]/div[3]/div[3]/div/table/tbody/tr')
    for data in reversed(dataList):
         text = data.xpath('.//text()')
         ball = BallData()
         ball.red = []
         ball.ID = int(text[0])
         ball.date = text[1]
         for i in range(2,8):
              ball.red.append(int(text[i]))
         ball.blue = int(text[8])
         BallDataList.append(ball)#默认升序


def Analyse(sliced_list):
     RedTotalTimes = defaultdict(int)
     BlueTotalTimes = defaultdict(int)
     nearNum = 5
   
     for i in range(len(sliced_list)):#默认升序
          ball = sliced_list[i]
          id = 0
          ball.duplicates_red = {}
          for num in range(i+1,i+1+nearNum):
                    if(num >= len(sliced_list)):
                         break
                    id += 1
                    set1 = set(ball.red)
                    set2 = set(sliced_list[num].red)
                    duplicates = set1.intersection(set2)
                    if len(duplicates) > 0:
                         ball.duplicates_red[id] = list(duplicates)

     blueExistCount = 0
     for i in range(len(sliced_list)):
          ball = sliced_list[i]
          id = 0
          ball.duplicates_blue = {}
          for num in range(i+1,i+1+nearNum):
                    if(num >= len(sliced_list)):
                         break
                    id += 1
                    if ball.blue == sliced_list[num].blue:
                         ball.duplicates_blue[id] = ball.blue
                         blueExistCount += 1
     
     redNum = defaultdict(int)
     redTimes = defaultdict(int)
     blueTimes = defaultdict(int)
     for data in sliced_list:    
          for k,numList in data.duplicates_red.items():
               redNum[len(numList)]+=1
               redTimes[k]+=1
          for k,numList in data.duplicates_blue.items():
               blueTimes[k]+=1

          #print(f'ID:{data.ID},date:{data.date},red:{data.red},blue:[{data.blue}]')
          #print('red',data.duplicates_red)
          #print('blue',data.duplicates_blue)
     
          for num in data.red:
               RedTotalTimes[num] += 1
          BlueTotalTimes[data.blue] += 1
     #print(f'Total:{len(sliced_list)},blueExistCount:{blueExistCount}')
     RedTotalTimes = sorted(RedTotalTimes.items(), key=lambda x: x[1], reverse=True)
     BlueTotalTimes = sorted(BlueTotalTimes.items(), key=lambda x: x[1], reverse=True)

     len1 = int(len(RedTotalTimes)/2)
     len2 = int(len(BlueTotalTimes)/2)
     index1 = 0
     index2 = 0

     redTopKeys = []
     blueTopKeys = []
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

     #print(f'total:{len(sliced_list)},nearNum:{nearNum},redNum:{redNum},redTimes:{redTimes},blueTimes:{blueTimes}')
     #print("RedTotalTimes:",RedTotalTimes)
     #print("BlueTotalTimes:",BlueTotalTimes)
     #print("redTopKeys:",redTopKeys)     
     #print("blueTopKeys:",blueTopKeys)
     return redTopKeys 
   


def DoRecommend(fileName,sliced_list,redTopKeys):
     redFilterNumber = []
     blueFilterNumber = []
     filterCountTT = filterCount = 3
     recommendCount = 100

     for ball in reversed(sliced_list):    
          if filterCount == 0:
               break
          filterCount -= 1
          redFilterNumber += ball.red

     bluefilterCountTT = bluefilterCount = 5
     for ball in reversed(sliced_list):    
          if bluefilterCount == 0:
               break
          bluefilterCount -= 1
          blueFilterNumber.append(ball.blue)
     redFilterNumber = list(set(redFilterNumber))
     blueFilterNumber = list(set(blueFilterNumber))
     #print(f'RedfilterCount:{filterCountTT},BluefilterCount:{bluefilterCountTT},filter_red:{redFilterNumber},filter_blue:{blueFilterNumber}')

     recommend_red = []
     recommend_blue = []
     current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
     with open(fileName, "a",encoding="utf-8") as file:
           
       #print(f'recommend:{current_time_str}')    
       file.write(f'recommend:{current_time_str}\n')
       for i in range(recommendCount):
          recommend_red = []
          recommend_blue = []
          while True:
               #sleep(0.1)
               #t = int(time.time() * 10000000)
               #random.seed(t)
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
               #sleep(0.1)
               #t = int(time.time() * 10000000)
               #random.seed(t)
               num = random.randint(1, 16)
               if num not in recommend_blue:
                    if num not in blueFilterNumber:
                         recommend_blue.append(num)
                    if(len(recommend_blue) == 2):
                         break
          recommend_red.sort()
          #recommend_blue.sort()
          #print(f"{recommend_red}--{recommend_blue}")
          file.write(f"{recommend_red}--{recommend_blue}\n")
       file.write("\n")
     file.close()





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

if __name__ == "__main__":
    
      
    BallDataList = GetHtml('2024-01-01')
    redTopKeys = Analyse(BallDataList)
    fileName = f'./OutPut/DoubleBall_senge.txt'
    DoRecommend(fileName,BallDataList,redTopKeys)
'''
    startID = BallDataList[0].ID
    endID = BallDataList[len(BallDataList)-1].ID
    legth = len(BallDataList)
    for i in range(legth-(legth-50), legth):
          sleep(0.1)
          random.seed(int(time.time() * 1000000))
          sliced_list = BallDataList[:i]
          redTopKeys = Analyse(sliced_list)
          fileName = f'./OutPut/DoubleBall_{i}.txt'
          DoRecommend(fileName,sliced_list,redTopKeys)
          nextData = BallDataList[i]
          #print('nextID',nextData.ID)
          Selenium_Recommend_Analyse.Doit(fileName,nextData.red,[nextData.blue])

'''
