from selenium import webdriver
from time import sleep
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from lxml import etree
import re
from selenium.webdriver.common import by

GUID = 1000  
search = 'all' 
exceptionValue = 1 #异常值 
startMonth = 8
startDay  = 6 
matchMap = {}

class MatchData:
    ID = 0
    date = '' 
    week = '' 
    matchName = ''
    team1 = ''
    team2 =''
    half = ''
    all = ''
    win = ''
    flat = ''
    lose = ''
    result = 0
    state = ''
    exception = False


def GetWinType(index):
      data = ''
      if index == 7:
          data = '胜'
      elif index == 8:
            data = '平'
      elif index == 9:
            data = '负'
      return data

# 定义蓝色字体 ANSI 转义码
blue_color = "\033[34m"

# 恢复默认颜色 ANSI 转义码
reset_color = "\033[0m"


chinese_month_dict = {
    '一月': 1,
    '二月': 2,
    '三月': 3,
    '四月': 4,
    '五月': 5,
    '六月': 6,
    '七月': 7,
    '八月': 8,
    '九月': 9,
    '十月': 10,
    '十一月': 11,
    '十二月': 12
}

def IsException(str1,str2,str3):
    result1 = re.sub(r'[^\d.]+', '', str1)
    result2 = re.sub(r'[^\d.]+', '', str2)
    result3 = re.sub(r'[^\d.]+', '', str3)
    number1 = float(result1)
    number2 = float(result2)
    number3 = float(result3)
    e = False
    if number1 - 1 > number2 or number1 - 1 > number3:
          e = True
    return e

def AddToMap(match):
    global matchMap
    if match.matchName in matchMap:
        matchMap[match.matchName].append(match)
    else:
        matchMap[match.matchName] = [match]


def ParseSource(html):
    global GUID

    trList = html.xpath('//tr[@class="even" or @class="odd"]')
    for tdList in trList:
        cow = []
        index = 0
        for td in tdList:
                    index += 1
                    span = td.xpath('.//span')
                    if len(span) == 3:
                           data = td.xpath('.//span//text()')
                           cow += data
                    elif len(span) == 1:
                            winType = GetWinType(index)
                            type = td.xpath('.//span/@class')[0]
                            if type != '': 
                                if index == 5:
                                      cow.append("半场"+ span[0].text) 
                                elif index == 6:
                                      cow.append("全场"+ span[0].text) 
                                else:                                       
                                    cow.append("#"+winType+ span[0].text) 
                            else:
                                 cow.append(winType + span[0].text)
                    else:
                        if td.text != None:
                            cow.append(td.text)
        
                            
        GUID += 1
        match = MatchData()
        match.ID = GUID
        match.date = cow[0]
        match.week = cow[1]
        match.matchName = cow[2]
        match.team1 = cow[3]
        match.team2 = cow[5]
        match.half = cow[6]
        match.all = cow[7]
        match.win = cow[8]
        match.flat = cow[9]
        match.lose = cow[10]
        match.state = cow[11]
        if '#' in cow[8]:
            match.result = 1
            match.win = blue_color + cow[8] + reset_color
            match.exception = IsException(cow[8],cow[9],cow[10])
        if '#' in cow[9]:
            match.result = 2
            match.flat = blue_color + cow[9] + reset_color
            match.exception = IsException(cow[9],cow[8],cow[10])
        if '#' in cow[10]:
            match.result = 3
            match.lose = blue_color + cow[10] + reset_color
            match.exception = IsException(cow[10],cow[8],cow[9])
        AddToMap(match)

def PrintResult():
    for name, matchList in matchMap.items():
     for match in matchList:
        if match.matchName != search and search != 'all':
           continue
        print(match.ID,match.date, match.week,match.matchName,match.team1," VS ",match.team2,match.half,match.all,"【"+ match.win,match.flat,match.lose+"】",match.state)
      
    print("异常值=",exceptionValue)
    for name, matchList in matchMap.items():
     for match in matchList:
        if match.matchName != search and search != 'all':
           continue
        if match.exception == True:
            print("异常",match.ID,match.date,match.matchName, match.team1," VS ",match.team2,match.all,"【"+ match.win,match.flat,match.lose+"】")

    for name, matchList in matchMap.items():
     total = len(matchList)
     num = 0
     for match in matchList:
          if match.exception == True:
               num += 1
     if(num > 0):
        print(name,"总场数="+str(total), "异常数="+str(num),"异常率="+str((num / total)*100)+"%")

    for name, matchList in matchMap.items():
     total = len(matchList)
     num = 0
     for match in matchList:
          if match.exception == True:
               num += 1
     if(num == 0):
        print("无异常赛事",name,"总场次="+str(total),"异常数=0")

     

if __name__ == "__main__":
    
    option = ChromeOptions() 
    #option.add_argument('--headless')
    option.add_experimental_option('excludeSwitches',['enable-automation'])
    option.add_experimental_option('useAutomationExtension',False)

    browser = webdriver.Chrome(option)
    browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',{'source' : 'Object.defineProperty(navigator,"webdriver",{get:()=>undefined})'})
    #browser.set_window_size(1366,768)
    browser.get('https://www.lottery.gov.cn/jc/zqsgkj/')
    #print(browser.page_source)
    sleep(1)

    start_element = browser.find_element(by.By.ID,"start_date")
    start_element.click()
    html =etree.HTML(browser.page_source)
    monthText = html.xpath('//*[@id="ui-datepicker-div"]/div/div//text()')[2]
    monthNum = chinese_month_dict[monthText]
    if monthNum > startMonth :
        btn = browser.find_element(by.By.XPATH,'//*[@id="ui-datepicker-div"]/div/a[1]')
        btn.click()
        html =etree.HTML(browser.page_source)

    dayRow = html.xpath('//*[@id="ui-datepicker-div"]/table/tbody/tr')#加上'/td'的话可以直接获取所有td,也就是每个日期
    dayXpathStr = ''
    r = 0
    for row in dayRow:
        for day in row:
            t = day.xpath('.//a//text()')
            if len(t) > 0 and t[0] == str(startDay):
                dayXpathStr = day.getroottree().getpath(day)
                break
    dayBtn = browser.find_element(by.By.XPATH,dayXpathStr)
    dayBtn.click()

    search = browser.find_element(by.By.XPATH,'//*[@id="headerTr"]/div[1]/div[1]/div/a')
    search.click()
    html = etree.HTML(browser.page_source)

    pageList = html.xpath('//*[@id="matchList"]/div/div/ul/li/a')
    #需要去除尾页
    for page in pageList:
        

    #//*[@id="headerTr"]/div[1]/div[1]/div/a

    #//*[@id="ui-datepicker-div"]/table/tbody/tr[5]/td[1]
    #<input id="start_date" name="start_date" type="text" value="" class="hasDatepicker">
    #<a class="ui-datepicker-prev ui-corner-all" data-handler="prev" data-event="click" title="Prev"><span class="ui-icon ui-icon-circle-triangle-w">Prev</span></a>

    #ParseSource(browser)
    #PrintResult()
    sleep(100)
