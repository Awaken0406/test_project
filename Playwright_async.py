import asyncio
from playwright.async_api import async_playwright
from cloudscraper import create_scraper
import time


async def main():
    url = 'https://opensea.io/category/memberships/'
    scraper = create_scraper()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        #await page.goto(url)

        # 使用 CloudFlare Scraper 获取 CloudFlare 网站的真实内容
        content =  scraper.get(url).content

        # 将获取到的内容设置到 Playwright 的页面中
        await page.set_content(content.decode('utf-8'))

        # 在页面上执行一些操作，如点击、输入等
        #await page.click('#button')
       # await page.type('#input', 'Hello, World!')

        # 截取页面的屏幕截图并保存到本地
      #  await page.screenshot(path='screenshot.png')
        time.sleep(100)
        # 关闭浏览器
        await browser.close()

asyncio.run(main())


#pip install ndg-httpsclient
#pip install pyopenssl
#pip install pyasn1
