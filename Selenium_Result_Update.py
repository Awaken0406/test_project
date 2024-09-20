from collections import defaultdict
import re
import Selenium_DoubleBall

class BallDataEx:
        ID = 0
        date = ''
        red = []
        blue = 0

        def __init__(self, ID, date, red, blue):
            self.ID = ID
            self.date = date
            self.red = red
            self.blue = blue
        def __lt__(self, other):
            return (self.ID) < (other.ID)

def create_ball_data_from_string(data_str):
   
    match = re.match( r'(\d+)\s(\d{4}-\d{2}-\d{2})\s\[(\d+(?:,\s\d+)*)\]--\[(\d+)\]', data_str)
    if match:
        ID = int(match.group(1))
        date = match.group(2)
        red = [int(num) for num in match.group(3).split(',')]
        blue = int(match.group(4))
        return BallDataEx(ID, date, red, blue)
    else:
        return None

def remove_chinese_chars(input_str):
    # 使用正则表达式匹配中文字符
    chinese_pattern = re.compile("[\u4e00-\u9fa5（）]+")
    # 使用 sub 方法替换中文字符为空字符串
    result = chinese_pattern.sub('', input_str)
    
    return result


def LoadFile(fileName):
    AllDataMap ={}
    with open(fileName, 'r',encoding="utf-8") as file:
        content = file.readlines()
    
    for line in content:
        if 'recommend' in line or line == '\n':
            continue

        data = create_ball_data_from_string(line)
        AllDataMap[data.ID] =data
    file.close()
    return AllDataMap

if __name__ == "__main__":
    
    AllDataMap = LoadFile('./OutPut/DoubleBallData.txt')
    DataList = Selenium_DoubleBall.GetHtml('2024-09-20')
    for data in DataList:
        data.date = remove_chinese_chars(data.date)
        AllDataMap[data.ID] = data
        #AllDataMap[data.ID] = BallDataEx(data.ID,data.date,data.red,data.blue)
    
    AllDataMap = dict(sorted(AllDataMap.items(), key=lambda x: x[1]))
    with open('./OutPut/DoubleBallData.txt', 'w',encoding="utf-8") as file:
        for key, value in AllDataMap.items(): 
            file.write(f'{value.ID} {value.date} {value.red}--[{value.blue}]\n')

