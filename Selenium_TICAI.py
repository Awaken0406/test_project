from selenium import webdriver
from time import sleep
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from lxml import etree
import re
from selenium.webdriver.common import by
from datetime import datetime, timedelta

'''
Python 中的函数是可以访问其定义范围内(作用域)的变量，这种行为与 Python 的作用域规则(LEGB 规则)有关。
LEGB 表示 Local(局部)、Enclosing(嵌套)、Global(全局)和 Built-in(内建)四种作用域。

当函数内部引用一个变量时,Python 解释器会按照 LEGB 的顺序查找该变量：

Local(局部)：函数内部定义的局部变量。
Enclosing(嵌套)：包含当前函数的外层函数中的变量。
Global(全局)：模块级别的变量。
Built-in(内建):Python 语言内置的变量。
因此，当函数在嵌套的情况下，内部函数可以访问外部函数中的局部变量，这是因为 Python 的作用域规则允许函数访问其外部的作用域中的变量。
这种特性称为闭包(Closure)，即内部函数可以访问外部函数的变量和参数，这使得 Python 中的函数更加灵活和功能强大。
'''

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
    if number1 - exceptionValue > number2 or number1 - exceptionValue > number3:
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
 fileName = f'./OutPut/{searchName}_{startMonth}-{startDay}_{endMonth}-{endDay}.txt'
 with open(fileName, "w",encoding="utf-8") as file:
    for name, matchList in matchMap.items():
        for match in matchList:
          if match.exception == False:
            info_str = f"无异常 {match.ID} {match.date} {match.week} {match.matchName} {match.team1} VS {match.team2} {match.half} {match.all} 【{match.win}, {match.flat}, {match.lose}】 {match.state}\n"
            print(info_str,end='')
            cleaned_str = re.sub(r'\033\[34m|\033\[0m', '', info_str)
            file.write(cleaned_str)
        
    print("异常值=",exceptionValue)
    for name, matchList in matchMap.items():
        for match in matchList:
            if match.exception == True:
                info_str = f"异常 {match.ID} {match.date} {match.matchName} {match.team1} VS {match.team2} {match.all} 【{match.win}, {match.flat}, {match.lose}】\n"
                print(info_str,end='')
                cleaned_str = re.sub(r'\033\[34m|\033\[0m', '', info_str)
                file.write(cleaned_str)

    for name, matchList in matchMap.items():
        total = len(matchList)
        num = 0
        for match in matchList:
            if match.exception == True:
                num += 1
        
        float_num = (num / total)*100
        fstr = "{:.2f}".format(float_num)
        info_str = f"{name} 总场数={total}, 异常数={num}, 异常率={fstr}%\n"
        print(info_str,end='')
        file.write(info_str)      
        
    file.close()
      


def LoopPage(html):
    pageList = html.xpath('/html/body/div[3]/div[5]/div[2]/div/div/ul/li/a')
   #<div class="m-page"><ul><li class="u-pg4">首页</li><li class="u-pg3"><span>1</span></li><li class="u-pg2"><a onclick="jcSgkj.getDataClickPage(2)">2</a></li><li class="u-pg2"><a onclick="jcSgkj.getDataClickPage(3)">3</a></li><li class="u-pg2"><a onclick="jcSgkj.getDataClickPage(4)">4</a></li><li class="u-pg4"><a onclick="jcSgkj.getDataClickPage(4)">尾页</a></li><li>查询结果：有<span class="u-org">104</span>场赛事符合条件</li></ul></div> 
    #需要去除尾页
    #/html/body/div[3]/div[5]/div[2]/div/div/ul
    pageLen = len(pageList)
    i =0
    for page in pageList:
        i += 1
        if i == pageLen:
            break
        pagePathStr = page.getroottree().getpath(page)
        pageBtn = browser.find_element(by.By.XPATH,pagePathStr)
        pageBtn.click()
        sleep(1)
        html = etree.HTML(browser.page_source)
        ParseSource(html)


def SelectDate(month,day,element):
    date_element = browser.find_element(by.By.ID,element)
    date_element.click()
    html =etree.HTML(browser.page_source)

    monthText = html.xpath('//*[@id="ui-datepicker-div"]/div/div//text()')[2]
    monthNum = chinese_month_dict[monthText]

    if monthNum > month:
        btn = browser.find_element(by.By.XPATH,'//*[@id="ui-datepicker-div"]/div/a[1]') 
        for i in range(monthNum - month):
            btn.click()
            sleep(1) 
            html =etree.HTML(browser.page_source)
            btn = browser.find_element(by.By.XPATH,'//*[@id="ui-datepicker-div"]/div/a[1]')           
        html =etree.HTML(browser.page_source)
    elif month > monthNum:
        btn = browser.find_element(by.By.XPATH,'//*[@id="ui-datepicker-div"]/div/a[2]') 
        for i in range(month - monthNum):
            btn.click()
            sleep(1)
            html =etree.HTML(browser.page_source)
            btn = browser.find_element(by.By.XPATH,'//*[@id="ui-datepicker-div"]/div/a[2]')                
        html =etree.HTML(browser.page_source)

    dayRow = html.xpath('//*[@id="ui-datepicker-div"]/table/tbody/tr')#加上'/td'的话可以直接获取所有td,也就是每个日期
    dayXpathStr = ''
    r = 0
    for row in dayRow:
        for d in row:
            t = d.xpath('.//a//text()')
            if len(t) > 0 and t[0] == str(day):
                dayXpathStr = d.getroottree().getpath(d)
                break
    dayBtn = browser.find_element(by.By.XPATH,dayXpathStr)
    dayBtn.click()
   

def SearchDate(start_month,start_day,end_month,end_day):

    SelectDate(start_month,start_day,"start_date") 
    SelectDate(end_month,end_day,"end_date")
    searchElement = browser.find_element(by.By.XPATH,'//*[@id="headerTr"]/div[1]/div[1]/div/a')
    searchElement.click()
    sleep(2)
    html = etree.HTML(browser.page_source)
    ParseSource(html)
    LoopPage(html)


if __name__ == "__main__":
    
    option = ChromeOptions() 
    option.add_argument('--headless')
    option.add_experimental_option('excludeSwitches',['enable-automation'])
    option.add_experimental_option('useAutomationExtension',False)

    browser = webdriver.Chrome(option)
    browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',{'source' : 'Object.defineProperty(navigator,"webdriver",{get:()=>undefined})'})
    #browser.set_window_size(1366,768)
    browser.get('https://www.lottery.gov.cn/jc/zqsgkj/')
    sleep(2)

    GUID = 1000  
    searchName = '欧国联' #英锦标赛
    exceptionValue = 0 #异常值  
    SearchYear = 2024
    matchMap = {}



    startMonth = 7
    startDay  = 1 
    endMonth = 9
    endDay = 7
 

    if(searchName != 'all'):
        nameBtn =  browser.find_element(by.By.XPATH,'//*[@id="div_sel_competition"]')
        nameBtn.click()
        sleep(1) 
        html =etree.HTML(browser.page_source)
        nameList = html.xpath('//*[@id="div_league_list"]/a')
        for name in nameList:
            if name.text == searchName:
                namePathStr = name.getroottree().getpath(name)
                btn = browser.find_element(by.By.XPATH,namePathStr)
                btn.click()
                break
        

    smonth = startMonth
    sday = startDay
    emonth = endMonth
    eday = endDay

    startDate = datetime(year=SearchYear, month=smonth, day=sday)
    endDate = datetime(year=SearchYear, month=emonth, day=eday)
    delta = endDate - startDate
    day_difference =  delta.days 
    while day_difference > 18:
            newDate = startDate + timedelta(days=18)
            SearchDate(startDate.month,startDate.day,newDate.month,newDate.day)
            startDate = newDate + timedelta(days=1)
            delta = endDate - startDate
            day_difference =  delta.days 

    SearchDate(startDate.month,startDate.day,endMonth,endDay)
    
    #//*[@id="headerTr"]/div[1]/div[1]/div/a

    #//*[@id="ui-datepicker-div"]/table/tbody/tr[5]/td[1]
    #<input id="start_date" name="start_date" type="text" value="" class="hasDatepicker">
    #<a class="ui-datepicker-prev ui-corner-all" data-handler="prev" data-event="click" title="Prev"><span class="ui-icon ui-icon-circle-triangle-w">Prev</span></a>
    PrintResult()
    sleep(10)
