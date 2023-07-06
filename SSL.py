import requests
import re
from requests.packages import urllib3

#urllib3.disable_warnings()#忽略验证警告




#r1 = requests.get('https://ssr2.scrape.center/',cert=('/path/server.crt','/path/server.key'))
r1 = requests.get('https://ssr2.scrape.center/',verify=False)
print(r1.text)
