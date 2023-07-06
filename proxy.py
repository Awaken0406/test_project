import requests

proxies = {
    'https': 'http://10.10.10.10:1080',
    'http':'https://user:pawssword@10.10.10.10:1080'#有些代理需要身份认证
}

r1 = requests.get('https://www.httpbin.org/get/',proxies=proxies)
print(r1.status_code)
