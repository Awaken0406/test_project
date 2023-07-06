import requests
import re
from requests.packages import urllib3

urllib3.disable_warnings()#忽略验证警告

r = requests.get('https://www.baidu.com/')
print(type(r))
print(r.status_code)
print(r.cookies)
#print(r.text)#返回结果


r1 = requests.get('https://ssr1.scrape.center/',verify=False)
#pattern = re.compile('<h2.*?>(.*?)</h2>',re.S)
#titles = re.findall(pattern, r1.text)
#print(titles)

#r2 = requests.get('https://scrape.center/favicon.ico',verify=False)
#with open('favicon.ico','wb') as f:
#    f.write(r2.content)

#上传文件
#files = {'file':open('favicon.ico','rb')}
#r3 = requests.post('https://www.httpbin.org/post',files=files)
#print(r3.status_code)
#print(r3.text)

#设置cookie访问可以获取到登录后的页面信息
headers = {
    'Cookie':'_octo=GH1.1.1676448341.1680257918; _device_id=0d38131fa0bf0411049ce1323483ff5f; preferred_color_mode=light; tz=Asia%2FShanghai; has_recent_activity=1; user_session=zii5ybaxgZv69vT1Ax_C7tOSyHCSEX5xzqAZKp3DHRQ9lIwG; __Host-user_session_same_site=zii5ybaxgZv69vT1Ax_C7tOSyHCSEX5xzqAZKp3DHRQ9lIwG; tz=Asia%2FShanghai; color_mode=%7B%22color_mode%22%3A%22auto%22%2C%22light_theme%22%3A%7B%22name%22%3A%22light%22%2C%22color_mode%22%3A%22light%22%7D%2C%22dark_theme%22%3A%7B%22name%22%3A%22dark%22%2C%22color_mode%22%3A%22dark%22%7D%7D; logged_in=yes; dotcom_user=Awaken0406; _gh_sess=go05GmI161zDXRYhQChg1LtdLMayHp2efDG9xNJUWuuciKJRcjHfk9InsrKIi0efKcH3pQHkBLaAasa4CfCfmDyXPYEQmpU%2FpqeXLefwelOfCSXWdxJ4BfIhVQ0PHmxszXKfXC8hnMwnVNzYQL7NYsTL4aysgHnKSFmSU6mFGiRuTtob%2B4K%2BJFz2NqeNdc5b3ZtzajhTztEDkN8ydlImNrUcG615o7IiXuD8mBPHNii9s9%2F002iv1ewhsvrmjL93kflbgu%2BcEFZyzyIZWls8n4VpdfRb2UUbyl4Jx%2F39jXTdv%2B1KF6%2FmWEE%3D--%2BcvwWD7o0MmqDSG7--r1bpliW6rYyHlk7g67BgzA%3D%3D'
}
#r4 = requests.get('https://github.com',headers=headers)
#print(r4.text)

#session 维持
#不同的session获取到的cookie
#requests.get('https://www.httpbin.org/cookies/set/number/123456789')
#r5 = requests.get('https://www.httpbin.org/cookies/')
#print(r5.text)

#同个的session获取到的cookie
#Session模拟一个浏览器中打开同一站点的不同页面
s = requests.Session()
s.get('https://www.httpbin.org/cookies/set/number/123456789',timeout=2)
r6 = s.get('https://www.httpbin.org/cookies/',timeout=2)
print(r6.text)


