
from selenium import webdriver
from time import sleep
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait

#有些网页是javaScript动态渲染的,直接获取只能得到一堆代码,而且有些Ajax请求接口有些参数是加密的，直接破解还不如让浏览器直接处理,只要能获取到生成后的页面数据即可
#selenium 可以启动浏览器并操作浏览器，并连接到浏览器的DevTool,这样就可以获取到javaScript动态渲染的页面数据,所见即所爬。




option = ChromeOptions() 
#option.add_argument('--headless')
option.add_experimental_option('excludeSwitches',['enable-automation'])
option.add_experimental_option('useAutomationExtension',False)

browser = webdriver.Chrome(option)
browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',{'source' : 'Object.defineProperty(navigator,"webdriver",{get:()=>undefined})'})
#browser.set_window_size(1366,768)
browser.get('https://antispider1.scrape.center/')
print(browser.page_source)


#browser.get_screenshot_as_file('preview.png')
sleep(20)
browser.close
