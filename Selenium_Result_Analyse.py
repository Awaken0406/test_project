from collections import OrderedDict, defaultdict
import Selenium_Result_Update
from Selenium_Result_Update import BallDataEx
from datetime import datetime, timedelta

class AnalyseData:
        ID = 0
        red = []
        blue = 0


if __name__ == "__main__":
    AllDataMap = Selenium_Result_Update.LoadFile('./OutPut/DoubleBallData.txt')

    keys_to_delete = []
    startDate = datetime.strptime('2024-01-01','%Y-%m-%d')
    for key, value in AllDataMap.items():
        date = datetime.strptime(value.date,'%Y-%m-%d')
        if date < startDate:
            keys_to_delete.append(key)

    for key in keys_to_delete:
        del AllDataMap[key]

    print('startDate',startDate.date()) 
    AnalyseMap =defaultdict(int)
    TotalCountMap =defaultdict(int)
    BlueCountMap = defaultdict(int)
    for key, value in AllDataMap.items():
        numList = [0,0,0,0]

        data = AnalyseData()
        data.ID = key
        data.red = []
    
        for num in value.red:
            if(num < 10):
                data.red.append(0)
                numList[0] += 1
            elif(num < 20):
                data.red.append(1)
                numList[1] += 1
            elif(num < 30):
                data.red.append(2)
                numList[2] += 1
            else:
                data.red.append(3)
                numList[3] += 1

        num = value.blue              
        if(num < 10):
            data.blue = 0
            BlueCountMap[0] += 1
            #numList[4] += 1
        elif(num < 20):
           data.blue = 1
           BlueCountMap[1] += 1
           #numList[5] += 1


        AnalyseMap[data.ID] = data
        TotalCountMap[tuple(numList)] += 1

    tupleCount =defaultdict(int)
    for key, value in AnalyseMap.items():
        newKey = tuple(value.red) 
        tupleCount[newKey] += 1

    #x[0]表示按key排序,x[1]表示按value排序
    sorted_items = sorted(tupleCount.items(), key=lambda x: x[1], reverse=True)
    tupleCount = OrderedDict(sorted_items)

    #组合
    #print('Red')
    #for k,count in tupleCount.items():
    #    print(k,count)

    #print('Blue')
    BlueCountMap = dict(sorted(BlueCountMap.items(), key=lambda x: x[1], reverse=True))
    #for k,count in BlueCountMap.items():
    #    print(k,count)  

    #组合的统计
    sorted_items = sorted(TotalCountMap.items(), key=lambda x: x[1], reverse=True)
    TotalCountMap = OrderedDict(sorted_items)  
    for k,count in TotalCountMap.items():
        print(k,count)
