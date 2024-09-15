
# 定义蓝色字体 ANSI 转义码
blue_color = "\033[34m"
# 恢复默认颜色 ANSI 转义码
reset_color = "\033[0m"


if __name__ == "__main__":
    

    with open('./OutPut/DaLeTou_Recommend.txt', 'r') as file:
        content = file.readlines()

    find_front = [1,8,13,14,32]
    find_back = [1, 7]

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
        if data.allHit == True:
            print(f'All Hit :[{data.frontStr}]--[{data.backStr}]')

    for data in AllDataList:
        print(f'[{data.frontStr}]--[{data.backStr}], hitCount : {blue_color}{data.front_hit_count + data.back_hit_count}{reset_color}')
