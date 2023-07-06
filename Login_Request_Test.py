import requests
from urllib.parse import urljoin

BASE_URL = 'https://login2.scrape.center/'
LOGIN_URL = urljoin(BASE_URL,'/login')
INDEX_URL = urljoin(BASE_URL,'/page/1')
USERNAME ='admin'
PASSWORD = 'admin'

session =requests.Session()#使用同一个cookies

response_login = session.post(LOGIN_URL,data={  'username':USERNAME,'password':PASSWORD},allow_redirects=False)
cookies = session.cookies
print('Cookies',cookies)

response_index = session.get(INDEX_URL)
print('status',response_index.status_code)
print('url',response_index.url)
