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
from collections import defaultdict, OrderedDict
#import V3.mysql_db as db




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
     return redTopKeys,blueTopKeys
   
'''
(2, 2, 2, 0) 47
(2, 2, 1, 1) 36
(2, 1, 2, 1) 32
(2, 3, 1, 0) 29
(1, 2, 2, 1) 28

(2, 2, 2, 0) 9
(2, 2, 1, 1) 8
(2, 3, 1, 0) 8
(2, 0, 3, 1) 7
(3, 2, 1, 0) 6
(1, 2, 2, 1) 6
(2, 1, 3, 0) 6
(1, 2, 3, 0) 6
(2, 1, 1, 2) 6

(1, 1, 3, 1) 5
(1, 3, 2, 0) 4
(3, 1, 2, 0) 4
(1, 1, 2, 2) 4
(3, 3, 0, 0) 4
(1, 3, 1, 1) 4
'''
def DoCombinationAnalyse(number,red):
     numList  =[0,0,0,0]
     #0,10,20,30
     Array = [[2, 2, 2, 0],[2, 2, 1, 1],[2, 1, 2, 1],[2, 3, 1, 0],[1, 2, 2, 1],[2, 0, 3, 1],[3, 2, 1, 0],[2, 1, 3, 0],[2, 1, 1, 2],[1, 2, 3, 0],
              (1, 1, 3, 1),(1, 3, 2, 0),(3, 1, 2, 0), (1, 1, 2, 2),(3, 3, 0, 0),(1, 3, 1, 1)]
     for num in red:
            i = int(num / 10)
            numList[i] += 1

     #十位还是各位
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


# 生成随机字符串
def generate_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))



def generate_md5_hashed_integer(maxValue):

    value = 0
    while(True):
          if value > 0:
              break        
          random_chars = generate_random_string(10)
          current_time = str(int(time.time()))
          random_number = str(random.randint(1, 2000))
  

          input_data = random_chars  + current_time + random_number
          md5_hash = hashlib.md5(input_data.encode()).hexdigest()
          hashed_integer = str(int(md5_hash, 16))
          start_index = int(len(hashed_integer) / 2)
          middle_substring = hashed_integer[start_index:start_index + 6]

          result = int(middle_substring)
          value = (result)%maxValue
    #print("value:",value)
    return int(value)


def RecommendRed(redTopKeys,redFilterNumber,mustFilter, count, continuous,IsString):
     recommend_red = []
     isContinuous = False
     while True:
               if(len(recommend_red) >= count):
                    break
               if IsString == True:
                    num = generate_md5_hashed_integer(34)
               else:
                    num = random.randint(1, 33)
               if num not in recommend_red:
                  if num not in mustFilter:
                    isOk = DoCombinationAnalyse(num,recommend_red)
                    if isOk == False:
                         continue
                    
                    isOK = False
                    if num in redTopKeys:
                         isOK = True     
                    elif num in redFilterNumber:
                         boolNum = random.randint(1,2)
                         if boolNum == 2:
                              isOK = True    
                    else:                           
                         boolNum = random.randint(1,2)
                         if boolNum == 2:
                              isOK = True     

                    if isOk == True:
                         recommend_red.append(num) 
                         if continuous == True and isContinuous == False and len(recommend_red) + 1 < count and num > 10 and num < 30:
                            if num +  1 not in recommend_red:
                              boolNum = random.randint(1,5)
                              if boolNum == 5:
                                   ok = DoCombinationAnalyse(num +  1,recommend_red)
                                   if ok == True:
                                        recommend_red.append(num +  1) 
                                        isContinuous = True
                                        
                         

     return recommend_red

def DoRecommend(redTopKeys,blueTopKeys,G_exRed,G_exBlue,recommendCount,sliced_list,IsString,isPrint,isWrite):
     redFilterNumber = []
     blueFilterNumber = []
     filterCount = 3
     for ball in reversed(sliced_list):    
          if filterCount == 0:
               break
          filterCount -= 1
          redFilterNumber += ball.red

     bluefilterCount = 3#最近3期
     for ball in reversed(sliced_list):    
          if bluefilterCount == 0:
               break
          bluefilterCount -= 1
          blueFilterNumber.append(ball.blue)
     redFilterNumber = list(set(redFilterNumber))
     blueFilterNumber = list(set(blueFilterNumber))
    
     recommend_red = []
     recommend_blue = []
     current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

     AllDataList = []



     for i in range(recommendCount):
          recommend_red = []
          recommend_blue = []
          
          redList = RecommendRed(redTopKeys,redFilterNumber,[],6,True,IsString)
          #额外
          redEx = RecommendRed(redTopKeys , redFilterNumber,redList,G_exRed,False,IsString)
          recommend_red = redList + redEx
          
          while True: 
               if(len(recommend_blue) == 1 + G_exBlue):
                         break
               if IsString == True:
                    num = generate_md5_hashed_integer(17)
               else:
                    num = random.randint(1, 16)
               if num not in recommend_blue:
                    if num in blueTopKeys:
                         recommend_blue.append(num)
                    elif num in blueFilterNumber:
                         boolNum = random.randint(1,5)
                         if boolNum == 5:
                              recommend_blue.append(num)
                         
                    else:
                         boolNum = random.randint(1,2)
                         if boolNum == 2:
                              recommend_blue.append(num)

          recommend_red.sort()
          #recommend_blue.sort()
          if isPrint == True:
               print(f"{recommend_red}--{recommend_blue}")

          dd = Selenium_Recommend_Analyse.DataList()
          dd.front = recommend_red
          dd.back = recommend_blue
          AllDataList.append(dd)

     if isWrite == True: 
          db.SaveDoubleBall(AllDataList)

          '''file = open(fileName, "w",encoding="utf-8") 
          file.write(f'recommend:{current_time_str}\n')
          for d in AllDataList:    
               file.write(f"{d.front}--{d.back}\n")
          file.write("\n")
          file.close()'''
     return AllDataList

#随意的
def DoRecommendPass(recommendCount,redTopKeys,sliced_list):
     redFilterNumber = []
     blueFilterNumber = []
     filterCount = 3
     for ball in reversed(sliced_list):    
          if filterCount == 0:
               break
          filterCount -= 1
          redFilterNumber += ball.red

     bluefilterCount = 3#最近3期
     for ball in reversed(sliced_list):    
          if bluefilterCount == 0:
               break
          bluefilterCount -= 1
          blueFilterNumber.append(ball.blue)
     redFilterNumber = list(set(redFilterNumber))
     blueFilterNumber = list(set(blueFilterNumber))

     AllDataList = []
     for i in range(recommendCount):
          recommend_red = []
          recommend_blue = []

          while(True):
                if len(recommend_red) >= 6:
                      break          
                number = random.randint(1, 33)
                if number not in redTopKeys and  number in redFilterNumber :
                    recommend_red.append(number)
                else:
                      r = random.randint(1, 2)
                      if r == 2:
                         recommend_red.append(number)
          while(True):
                    buleNumber = random.randint(1, 16)
                    if buleNumber in blueFilterNumber:             
                         recommend_blue.append(buleNumber)
                         break
                    else:
                         r = random.randint(1, 2)
                         if r == 2:
                              recommend_blue.append(buleNumber)
                              break
          
          recommend_red.sort()
          dd = Selenium_Recommend_Analyse.DataList()
          dd.front = recommend_red
          dd.back = recommend_blue
          AllDataList.append(dd)

     return AllDataList

def Doit(fileName):
     RedMap = defaultdict(int)
     BlueMap = defaultdict(int)
     for t in range(loopTimes):
          seed = int(time.time() * 10000000)
          random.seed(seed)
          AllDataList = DoRecommend(redTopKeys,blueTopKeys,G_exRed,G_exBlue,recommendCount,BallDataList,IsString,False,False)
          for i in range(len(AllDataList)):
               info  = AllDataList[i]
               BlueMap[info.back[0]] += 1
               for d in range(len(info.front)):
                    num = info.front[d]
                    RedMap[num] += 1

     RedMap = dict(sorted(RedMap.items(), key=lambda x: x[1], reverse=True))
     BlueMap = dict(sorted(BlueMap.items(), key=lambda x: x[1], reverse=True))
     current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
     file = open(fileName, "a",encoding="utf-8") 
     if(IsString == True):
               info = f'random string:{current_time_str},IsString:{IsString},loopTimes:{loopTimes},recommendCount:{recommendCount}\n'
               file.write(info)
               print(info,end='')
     else:
               info = f'random number:{current_time_str},IsString:{IsString},loopTimes:{loopTimes},recommendCount:{recommendCount}\n'
               file.write(info)
               print(info,end='')

     index = 0
     strinfo =''
     print('Red:')
     file.write('Red:\n')
     for k,v in RedMap.items():
          index+=1
          strinfo += f'index:{index},number:{k},count:{v}   '
          if (index % 5) == 0 :
                    print(strinfo)
                    file.write(f'{strinfo}\n')
                    strinfo = ''
     print(strinfo)
     file.write(f'{strinfo}\n')


     index = 0
     strinfo = ''
     print('Blue:')
     file.write('Blue:\n')
     for k,v in BlueMap.items():
          index+=1
          strinfo += f'index:{index},number:{k},count:{v}   '
          if (index % 5) == 0 :
                    print(strinfo)
                    file.write(f'{strinfo}\n')
                    strinfo = ''
     print(strinfo)
     file.write(f'{strinfo}\n')
     file.write("\n")
    
     print('筛选:')
     file.write("筛选:\n")
     if(IsString == True):
          redList = redStringList
          blueList = blueStringList
     else:
          redList = redNumberList
          blueList = blueNumberList

     outRed = []
     outBlue =[]
     for idIndex in redList:
          index =0
          strinfo = ''
          for k,v in RedMap.items():
               index += 1
               if index == idIndex:
                         strinfo = f'red index:{index},number:{k}  '
                         print(strinfo)
                         file.write(f'{strinfo}\n')
                         outRed.append(k)
               

     print('-----------------------')
     file.write(f'-----------------------\n')
     for idIndex in blueList:
          index =0
          strinfo = ''
          for k,v in BlueMap.items():
               index += 1
               if index == idIndex:
                         strinfo = f'blue index:{index},number:{k}  '
                         print(strinfo)
                         file.write(f'{strinfo}\n')
                         outBlue.append(k)

     outRed = list(set(outRed))
     outBlue = list(set(outBlue))
     print('-----------------------')
     file.write(f'-----------------------\n')
     print(f'Result:{outRed}--{outBlue}')
     print('-----------------------')
     file.write(f'Result:{outRed}--{outBlue}')
     file.write(f'-----------------------\n')
     file.write(f'\n')
     file.close()

     return outRed,outBlue



def CrazyCompression():
     fileName = f'./OutPut/CrazyCompression.txt'
     SelectCount = 100
     RMap = defaultdict(int)
     BMap = defaultdict(int)
     for i in range(SelectCount):
          outRed,outBlue = Doit(fileName)
          for v in outRed:
               RMap[v] += 1
          for v in outBlue:
               BMap[v] += 1

     RMap = dict(sorted(RMap.items(), key=lambda x: x[1], reverse=True))
     BMap = dict(sorted(BMap.items(), key=lambda x: x[1], reverse=True))

     file = open(fileName, "a",encoding="utf-8")
     print(f'疯狂压缩:')
     file.write(f'疯狂压缩:\n')
     index =0
     for k,v in RMap.items():
          index += 1
          if(index > 7):
               break
          print(f'{k},',end='')
          file.write(f'{k},')

     print(f'  --  ',end='')
     file.write(f'  --  ')
     index = 0
     for k,v in BMap.items():
          index += 1
          if(index > 2):
               break
          print(f'{k},',end='')
          file.write(f'{k},')
     print(f'\n',end='')
     file.write(f'\n')
     file.close()


def GetRandomTimestamp(date_string):
     #date_string = '2022-01-01'
     timestamp = datetime.strptime(date_string, '%Y-%m-%d').timestamp()
     rand = random.randint(43200, 86400)
     return timestamp + rand
   
#排除法模型
def RunExcludeModel(BallDataList):
     RMap = defaultdict(int)
     legth = len(BallDataList)
     loopTimes = 10
     G_GroupCount = 100
     for loop in range(loopTimes): 
          for i in range(legth - G_GroupCount, legth): 
               #RMap.clear()
               nextData = BallDataList[i]
               Timestamp = GetRandomTimestamp(nextData.date) - 86400
               seed = int(Timestamp * 10000000)
               random.seed(seed)    
               sliced_list = BallDataList[:i]
               redTopKeys,blueTopKeys = Analyse(sliced_list)
               AllDataList = DoRecommendPass(PassRecommendCount,redTopKeys,sliced_list)
          
               Selenium_Recommend_Analyse.AnalyseFile(AllDataList,nextData.red,[nextData.blue])
               for data in AllDataList:
                    num = data.front_hit_count #+ data.back_hit_count
                    RMap[num] += 1

     sorted_keys = sorted(RMap.keys(), key=lambda x: x, reverse=True)
     sorted_RMap = OrderedDict()
     for key in sorted_keys:
               value = RMap[key]
               percent = (value/(PassRecommendCount * G_GroupCount * loopTimes)) * 100
               sorted_RMap[key] = RMap[key]
               print(f'hitCount:--{key},times:{value},percent:{percent}%')
     #print(sorted_RMap)


def DoitPass(sliced_list): 
     AllDataList = DoRecommendPass(PassRecommendCount,redTopKeys,sliced_list)
     redList = []
     blueList = []
     for data in AllDataList:
          redList += data.front
          blueList += data.back
     redList = list(set(redList))
     blueList = list(set(blueList))
     print(f'pass red{redList},blue:{blueList}')
     print('-----------------------')


if __name__ == "__main__":
     
     BallDataList = []
     AllDataMap = Selenium_Result_Update.GetFileDate('2022-01-01')
     for data in AllDataMap.values():
          BallDataList.append(data)
     redTopKeys,blueTopKeys = Analyse(BallDataList)

     G_exRed = 0
     G_exBlue = 0
     recommendCount = 10000   #默认10000
     IsString = False          #默认True
     loopTimes = 1            #默认1
     redStringList = [25,16,28,19,18,27,9]
     blueStringList = [15,9]

     redNumberList = [20,2,26,28,19,22,12]
     blueNumberList = [3,8]

     PassRecommendCount = 1
     name = f'./OutPut/DoubleBall_Recommend_Log.txt'
     Doit(name)
     #DoitPass(BallDataList) #just once
     #RunExcludeModel(BallDataList)
