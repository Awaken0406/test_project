from selenium import webdriver
from time import sleep
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from lxml import etree

#有些网页是javaScript动态渲染的,直接获取只能得到一堆代码,而且有些Ajax请求接口有些参数是加密的，直接破解还不如让浏览器直接处理,只要能获取到生成后的页面数据即可
#selenium 可以启动浏览器并操作浏览器，并连接到浏览器的DevTool,这样就可以获取到javaScript动态渲染的页面数据,所见即//所爬。


class MatchData:
    date = '' #日期
    week = '' #星期
    matchName = ''#比赛名称
    team1 = ''
    team2 =''
    half = ''
    all = ''
    win = ''
    flat = ''
    lose = ''
    result = 0
    state = ''


option = ChromeOptions() 
option.add_argument('--headless')
option.add_experimental_option('excludeSwitches',['enable-automation'])
option.add_experimental_option('useAutomationExtension',False)

browser = webdriver.Chrome(option)
browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',{'source' : 'Object.defineProperty(navigator,"webdriver",{get:()=>undefined})'})
#browser.set_window_size(1366,768)
browser.get('https://www.lottery.gov.cn/jc/zqsgkj/')
#print(browser.page_source)
sleep(5)
html =etree.HTML(browser.page_source)

def GetWinType(index):
      str = ''
      if index == 7:
          str = '胜'
      elif index == 8:
            str = '平'
      elif index == 9:
            str = '负'
      return str

# 定义蓝色字体 ANSI 转义码
blue_color = "\033[34m"

# 恢复默认颜色 ANSI 转义码
reset_color = "\033[0m"


trList = html.xpath('//tr[@class="even" or @class="odd"]')
allMatch = []
for tdList in trList:
        cow = []
        index = 0
        for td in tdList:
                    index += 1
                    span = td.xpath('.//span')
                    if len(span) == 3:
                           str = td.xpath('.//span//text()')
                           cow += str
                    elif len(span) == 1:
                            winType = GetWinType(index)
                            type = td.xpath('.//span/@class')[0]
                            if type != '': 
                                if index == 5:
                                      cow.append("半场-"+ span[0].text) 
                                elif index == 6:
                                      cow.append("全场-"+ span[0].text) 
                                else:                                       
                                    cow.append("#"+winType+ span[0].text) 
                            else:
                                 cow.append(winType + span[0].text)
                    else:
                        if td.text != None:
                            cow.append(td.text)
        
                            

        match = MatchData()
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
        if '#' in cow[9]:
            match.result = 2
            match.flat = blue_color + cow[9] + reset_color
        if '#' in cow[10]:
            match.result = 3
            match.lose = blue_color + cow[10] + reset_color
        allMatch.append(match)
 

search = 'all'           
for match in allMatch:
     if match.matchName != search and search != 'all':
           continue
     print(match.date, match.week,match.matchName,match.team1," VS ",match.team2,match.half,match.all,match.win,match.flat,match.lose,match.state)
