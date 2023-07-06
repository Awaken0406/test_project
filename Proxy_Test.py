import requests
proxy = '183.164.242.195:8089'
proxies = {
    'http':'http://' + proxy,
    'https':'https://' + proxy,
}

try:
    response = requests.get('https://www.httpbin.org/get',proxies=proxies)
    print(response)
except requests.exceptions.ConnectionError as e:
    print('Error',e.args)
