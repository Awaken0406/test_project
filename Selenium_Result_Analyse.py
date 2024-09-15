
# 定义蓝色字体 ANSI 转义码
blue_color = "\033[34m"
# 恢复默认颜色 ANSI 转义码
reset_color = "\033[0m"



def Print_Double():
    one=two=three=four=five=six=0
    for data in AllDataList:
        if data.front_hit_count == 6 and data.back_hit_count == 1:
            one += 1
        elif data.front_hit_count == 6 and data.back_hit_count == 0:
            two += 1
        elif data.front_hit_count == 5 and data.back_hit_count == 1:
            three += 1
        elif (data.front_hit_count == 5 and data.back_hit_count == 0) or (data.front_hit_count == 4 and data.back_hit_count == 1):
             four += 1
        elif (data.front_hit_count == 4 and data.back_hit_count == 0) or (data.front_hit_count == 3 and data.back_hit_count == 1):
             five += 1
        if (data.front_hit_count == 2 or data.front_hit_count == 1 or data.front_hit_count == 0) and data.back_hit_count == 1:
             six += 1

    money = one*6000000 + two*100000 + three*3000 + four*200 + five*10 + six*5   
    print(f'Total:{len(AllDataList)}')
    print(f'{blue_color}one:{one},two:{two},three:{three},four:{four},five:{five},six:{six}{reset_color}')
    print(f'{blue_color}money:{money}{reset_color}')

def Print_DaLeTou():
    pass

if __name__ == "__main__":
    

    with open('./OutPut/DoubleBall_Recommend.txt', 'r') as file:
        content = file.readlines()

    find_front = [6, 18, 19, 20, 22, 32]
    find_back = [6]

    class DataList:
        front = []
        back = []
        front_hit_count = 0
        back_hit_count = 0
        frontStr=''
        backStr=''
        allHit = False

    AllDataList = []
    for line in content:
        if 'recommend' in line or line == '\n':
            continue
        parts = line.strip().split('--')       
        front_str, back_str = parts
        front_array = list(map(int, front_str.strip('[]').split(', ')))
        back_array = list(map(int, back_str.strip('[]').split(', ')))


        data = DataList()
        data.front = front_array
        data.back = back_array
        AllDataList.append(data)
    
    for data in AllDataList:
        front_hit_count = 0
        back_hit_count = 0
        frontStr = ''
        backStr = ''
        allHit = True

        for num in  data.front:
            if num in find_front:
                front_hit_count += 1
                frontStr += blue_color + str(num) + reset_color
            else:  
                allHit = False
                frontStr += str(num)
            frontStr +=  ' '

        for num in  data.back:
            if num in find_back:
                back_hit_count += 1
                backStr += blue_color + str(num) + reset_color 
            else:            
                allHit = False
                backStr += str(num)
            backStr += ' '
        
        data.front_hit_count = front_hit_count
        data.back_hit_count = back_hit_count
        data.frontStr = frontStr
        data.backStr = backStr
        data.allHit = allHit

    for data in AllDataList:
        print(f'[{data.frontStr}]--[{data.backStr}], hitCount : {blue_color}{data.front_hit_count + data.back_hit_count}{reset_color}')

    for data in AllDataList:
        if data.allHit == True:
            print(f'All Hit :[{data.frontStr}]--[{data.backStr}]')
    Print_Double()
    #Print_DaLeTou()
