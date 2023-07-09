import json
import re
from playwright.sync_api import Playwright, sync_playwright, expect
import time



def modify_post_request(route, request):
    # 获取原始请求的payload参数
    payload =  request.post_data
    # 判断是否为需要拦截的POST请求数据
    if request.method == 'POST' and payload and 'selectedDate' in payload:
        # 解析原始payload参数为字典
      #  payload_dict = json.loads(payload)
        # 修改指定字段的值
      #  payload_dict['selectedDate'] = '01/31/2024'

        # 将修改后的payload参数设置为请求的新payload
        #route.continue_(method=request.method, headers=request.headers, post_data=json.dumps(payload_dict))

        date = "11%2F01%2F2023"
        # 使用正则表达式匹配 selectedDate 的值，并将其替换为新的值
        payload = re.sub(r'(selectedDate=)[^&]+', r'\g<1>' + date, payload)
        route.continue_(method=request.method, headers=request.headers, post_data=payload)

        #No appointments are available for 11/01/2023.

    else:
        # 不需要拦截，直接继续请求
        route.continue_()



user = 'SenGeMail@163.com' 
password = 'qq734697554'

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    js = """
        Object.defineProperties(navigator, {webdriver:{get:()=>undefined}});
        """
    page.add_init_script(js)

    page.goto("https://portal.ustraveldocs.com/?language=Chinese%20(Simplified)&country=China")
    page.get_by_label("电子邮件").click()
    page.get_by_label("电子邮件").fill(user)
    time.sleep(2)
    page.get_by_label("密码").click()
    page.get_by_label("密码").fill(password)
    time.sleep(2)
    page.get_by_label("*我已经阅读并理解 隐私政策").check()
    time.sleep(1)
    page.get_by_role("button", name="登陆").click()   
    time.sleep(3)  
    page.get_by_text("重新预约").click()
    time.sleep(2)  

    page.route('https://portal.ustraveldocs.com/scheduleappointment', modify_post_request)
    page.get_by_role("link", name="30").click()
 
    time.sleep(100)
    # ---------------------
    page.close()
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)


  #1) <a href="#" class="ui-state-default">30</a> aka get_by_role("link", name="30")
  #  2) <span class="ui-state-default">30</span> aka get_by_role("row", name="24 25 26 27 28 29 30").get_by_text("30")
  #  3) <td>08:30</td> aka get_by_role("cell", name="08:30")
