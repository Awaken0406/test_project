from playwright.sync_api import Playwright, sync_playwright, expect
import time

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
    page.get_by_label("电子邮件").fill("SenGeMail@163.com")
    time.sleep(2)
    page.get_by_label("密码").click()
    page.get_by_label("密码").fill("qq734697554")
    time.sleep(2)
    page.get_by_label("*我已经阅读并理解 隐私政策").check()
    time.sleep(1)
    page.get_by_role("button", name="登陆").click()
    time.sleep(100)
    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)

