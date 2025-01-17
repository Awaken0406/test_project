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


def CulcStage(AllDataList,red,blue,redIndexCountMap,blueIndexCountMap):
    RedMap = defaultdict(int)
    BlueMap = defaultdict(int)
    for i in range(len(AllDataList)):
         info  = AllDataList[i]
         BlueMap[info.back[0]] += 1
         for d in range(len(info.front)):
              num = info.front[d]
              RedMap[num] += 1
    RedMap = dict(sorted(RedMap.items(), key=lambda x: x[1], reverse=True))
    BlueMap = dict(sorted(BlueMap.items(), key=lambda x: x[1], reverse=True))
    #print(f"RedSize:{len(RedMap)},RedMap:{RedMap}") 
    #print(f"BlueSize:{len(BlueMap)},BlueMap:{BlueMap}")
    redIndexMap =  defaultdict(int)

    for r in  red:
        index = 0
        for k,v in RedMap.items():
            index+=1
            if(k==r):
                redIndexMap[r] = index
                redIndexCountMap[index] += 1
                break

    bindex = 0
    for k,v in BlueMap.items():
        bindex+=1
        if(k==blue):
            blueIndexCountMap[bindex] += 1
            break

    #for k,v in redIndexMap.items():
    #    print(f'num:{k},index:{v}')



def TextEx(recommendCount,BallDataList,redIndexCountMap,blueIndexCountMap):
    legth = len(BallDataList)
    for i in range(legth - G_GroupCount, legth): 
          seed = int(time.time() * 10000000)
          random.seed(seed)    
          sliced_list = BallDataList[:i]
          redTopKeys,blueTopKeys = Selenium_DoubleBall.Analyse(sliced_list)
          AllDataList = Selenium_DoubleBall.DoRecommend(redTopKeys,blueTopKeys,G_exRed,G_exBlue,recommendCount,sliced_list,False,False)
          nextData = BallDataList[i]
          CulcStage(AllDataList,nextData.red,nextData.blue,redIndexCountMap,blueIndexCountMap)

def Test(count,recommendCount,BallDataList):

    legth = len(BallDataList)
    totalMoney = 0
    winCount = 0
    for i in range(legth - G_GroupCount, legth):
          #seed = int(time.time() * 10000000)
          #seed = 17339911835903144
          #seed = 17339917270329938
          #random.seed(seed)
          
          sliced_list = BallDataList[:i]
          redTopKeys,blueTopKeys = Selenium_DoubleBall.Analyse(sliced_list)
          AllDataList = Selenium_DoubleBall.DoRecommend(redTopKeys,blueTopKeys,G_exRed,G_exBlue,recommendCount,sliced_list,False,False)
          nextData = BallDataList[i]
          #print('nextID',nextData.ID)
          money = Selenium_Recommend_Analyse.Doit(AllDataList,nextData.red,[nextData.blue])
          totalMoney += money
          if(money >= recommendCount*G_cost):
              winCount += 1
          
    totalCost = recommendCount*G_GroupCount*G_cost
    isSuc = winCount >= int(G_GroupCount/2)
    print(f'{count} GroupCount:{G_GroupCount}, recommendCount:{recommendCount}, cost:{totalCost}, hit:{totalMoney}')
    return totalMoney,totalCost,isSuc



def CulcComb(red_chosen,blue_chosen):
    #count = C(m, 6) * C(n, 1)
    red_combinations = math.comb(red_chosen, 6)
    blue_combinations = math.comb(blue_chosen, 1)
    total_bets = red_combinations * blue_combinations

    return total_bets



if __name__ == "__main__":

    BallDataList = []
    AllDataMap = Selenium_Result_Update.GetFileDate('2022-01-01')#recommend number date
    for data in AllDataMap.values():
         BallDataList.append(data)

   
    #Test Recommend
    recommendCount = 10000
    times = 10
    G_exRed = 0
    G_exBlue = 0 
    G_GroupCount = 50
    G_cost = CulcComb(6+G_exRed,1+G_exBlue)*2
    allTotalMoney = 0
    alltotalCost = 0

    redIndexCountMap =  defaultdict(int)
    blueIndexCountMap =  defaultdict(int)
    for i in range(times):
       TextEx(recommendCount,BallDataList,redIndexCountMap,blueIndexCountMap)

    redIndexCountMap = dict(sorted(redIndexCountMap.items(), key=lambda x: x[1], reverse=True))
    blueIndexCountMap = dict(sorted(blueIndexCountMap.items(), key=lambda x: x[1], reverse=True))
    for k,v in redIndexCountMap.items():
        print(f'red index:{k},count:{v}')
    for k,v in blueIndexCountMap.items():
        print(f'blue index:{k},count:{v}')
    #seed = int(time.time() * 10000000)
    ##seed = 17339986740234198
    #random.seed(seed)

    '''
    seedList = []
    #(7,1)=7, (8,1)=28, (8,2)=56 (8,3)=64
    i=100000000
    for i in range(times):
    #while(True):
       i += 1
       seed = int(time.time() * 10000000)
       random.seed(seed)
       #start_time = time.perf_counter()
       totalMoney,totalCost,isSuc = Test(i,recommendCount,BallDataList)
       allTotalMoney += totalMoney
       alltotalCost += totalCost
       #end_time = time.perf_counter()
       #execution_time = end_time - start_time
       #print(f"time:{execution_time:.6f}")
       if isSuc:
            print('!!11suc!!!! seed:%d',i)
            break
    avgCost = alltotalCost / times / recommendCount / G_GroupCount
    avgWin = allTotalMoney / times / recommendCount / G_GroupCount
    print('loopTimes:',times,'avgCost:',avgCost,'avgWin:',avgWin)
'''
    
     
