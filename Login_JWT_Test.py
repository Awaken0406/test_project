import requests
from urllib.parse import urljoin

BASE_URL = 'https://login3.scrape.center/'
LOGIN_URL = urljoin(BASE_URL,'/api/login')
INDEX_URL = urljoin(BASE_URL,'/api/book')
USERNAME ='admin'
PASSWORD = 'admin'



response_login = requests.post(LOGIN_URL,json={'username':USERNAME,'password':PASSWORD})
data = response_login.json()
print('response JSON',data)
jwt = data.get('token')
print('JWT',jwt)

headers = {
    'Authorization':f'jwt {jwt}'
}

response_index = requests.get(INDEX_URL,params={'limit':18,'offset':0},headers=headers)
print('status',response_index.status_code)
print('url',response_index.url)
print('response data',response_index.json())
