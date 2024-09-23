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
import Selenium_Result_Update
import Selenium_Recommend_Analyse




'''
在 Python 中，类的数据成员（类属性）在类定义中被初始化为可变对象（如列表）时，
这些对象会被所有该类的实例共享。这可能导致在实例化新对象时，类属性的可变对象并不会被重置为空，
而是保留了上一个实例的值。
'''


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
   
'''
(2, 2, 2, 0) 47
(2, 2, 1, 1) 36
(2, 1, 2, 1) 32
(2, 3, 1, 0) 29
(1, 2, 2, 1) 28
'''
def DoCombinationAnalyse(number,red):
     numList  =[0,0,0,0]
     Array = [[2, 2, 2, 0],[2, 2, 1, 1],[2, 1, 2, 1],[2, 3, 1, 0],[1, 2, 2, 1]]
     #Array = [[2, 2, 2, 0],[2, 2, 1, 1]]
     for num in red:
            i = int(num / 10)
            numList[i] += 1

   
     index = int(number / 10)

     for data in Array:
          if numList[index] < data[index]:
               ret = True
               for i in range(len(data)):
                    if numList[i] > data[i]:
                         ret = False
               if ret == True:
                    return True
                    
     return False


def DoRecommend(recommendCount,fileName,sliced_list,redTopKeys,isPrint):
     redFilterNumber = []
     blueFilterNumber = []
     filterCountTT = filterCount = 3

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
                    isOk = DoCombinationAnalyse(num,recommend_red)
                    if isOk == False:
                         continue

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
          if isPrint == True:
               print(f"{recommend_red}--{recommend_blue}")

          file.write(f"{recommend_red}--{recommend_blue}\n")
       file.write("\n")
     file.close()



if __name__ == "__main__":

    BallDataList = []
    AllDataMap = Selenium_Result_Update.GetFileDate('2024-01-01')
    for data in AllDataMap.values():
         BallDataList.append(data)

    redTopKeys = Analyse(BallDataList)
    fileName = f'./OutPut/DoubleBall_senge.txt'
    recommendCount = 100
    #DoRecommend(recommendCount,fileName,BallDataList,redTopKeys,True)

    #Test Recommend
    startID = BallDataList[0].ID
    endID = BallDataList[len(BallDataList)-1].ID
    legth = len(BallDataList)
    for i in range(legth-(legth-50), legth):
          sleep(0.1)
          random.seed(int(time.time() * 1000000))
          sliced_list = BallDataList[:i]
          redTopKeys = Analyse(sliced_list)
          fileName = f'./OutPut/DoubleBall_{i}.txt'
          DoRecommend(recommendCount,fileName,sliced_list,redTopKeys,False)
          nextData = BallDataList[i]
          #print('nextID',nextData.ID)
          Selenium_Recommend_Analyse.Doit(fileName,nextData.red,[nextData.blue])

