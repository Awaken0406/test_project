from playwright.sync_api import Playwright, sync_playwright
import time

import requests

# 通过API获取代理
def get_proxy(api, params):
    r = requests.get(api,params)
    if r.status_code == 200:
        return r.text
    else:
        return None


# 使用Playwright添加私密代理
def playwright_use_proxy(proxy_server):
    if not proxy_server:
        print('获取代理失败')
        return
    with sync_playwright() as p:

        proxy = {
            "server": f'http://{proxy_server}',
            "username": "d2304848217",
            "password": "9an858x3",
        } 
        browser = p.chromium.launch(headless=False,proxy=proxy)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://dev.kdlapi.com/testproxy")
        content = page.content()
        time.sleep(50)
        browser.close()
        return content


def main():
    # 定义API配置
    params = {
        'num': 1,
        'pt': 1,
        'sep': 1,
        'dedup':1,
        'secret_id': 'oo28ceg7wvkkb7dcaxxx',
        'signature': 'cqve9xl1u4vpyqq677g1a4j313qno16u',
    }
    api = 'https://dps.kdlapi.com/api/getdps/'
   # proxy = get_proxy(api, params)
   # print("proxy=",proxy)
    proxy = '198.211.117.231:80'
    content = playwright_use_proxy(proxy)
    print(content)


if __name__ == '__main__':
    main()
