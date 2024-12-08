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
import hashlib
import string
import Selenium_DoubleBall


def Test(count,redTopKeys,recommendCount,BallDataList):

    legth = len(BallDataList)
    totalMoney = 0
    GroupCount = 0
    for i in range(legth - 50, legth):#只遍历50期
          #sleep(0.1)
          random.seed(int(time.time() * 1000000))
          sliced_list = BallDataList[:i]
          #redTopKeys = Analyse(sliced_list)
          fileName = f'./OutPut/DoubleBall_{i}.txt'
          AllDataList = Selenium_DoubleBall.DoRecommend(G_exRed,G_exBlue,recommendCount,fileName,sliced_list,redTopKeys,False,False)
          nextData = BallDataList[i]
          #print('nextID',nextData.ID)
          money = Selenium_Recommend_Analyse.Doit(AllDataList,nextData.red,[nextData.blue])
          totalMoney += money
          GroupCount += 1
    totalCost = recommendCount*GroupCount*G_cost
    print(f'第{count}次循环','推测期数:',GroupCount,'每期组数:',recommendCount, '花费:',totalCost,'中奖金额:',totalMoney)
    return totalMoney,totalCost


if __name__ == "__main__":

    BallDataList = []
    AllDataMap = Selenium_Result_Update.GetFileDate('2023-01-01')
    for data in AllDataMap.values():
         BallDataList.append(data)

    redTopKeys = Selenium_DoubleBall.Analyse(BallDataList)

    #Test Recommend
    recommendCount = 10 #推荐组数
    times = 100
    allTotalMoney = 0
    alltotalCost = 0

    G_exRed = 4#加N个红球
    G_exBlue = 2#加N个篮球
    G_cost = 168#每注多少钱

    for i in range(times):
       start_time = time.perf_counter()
       totalMoney,totalCost = Test(i,redTopKeys,recommendCount,BallDataList)
       allTotalMoney += totalMoney
       alltotalCost += totalCost
       end_time = time.perf_counter()
       execution_time = end_time - start_time
       #print(f"time:{execution_time:.6f}")
    avgCost = alltotalCost / times
    avgWin = allTotalMoney / times
    print('循环次数:',times,'平均花费:',avgCost,'平均赚:',avgWin)
    
     
