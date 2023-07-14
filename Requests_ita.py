import requests

import cloudscraper
from urllib.parse import urljoin
import time
import sys



USERNAME ='SenGeMail@163.com'
PASSWORD = 'AG0Jca8WvS3kgh0B5lLhzWROqG5XEIN7rv4av55jQ+6+89/XVH5W0e9Vmn1+zZ30MYW7b7wT4daCHSreAMTEqCYJ0hufxQa5idZA7nKZ9JGBeap4DNM0D/5JvR1PjkEV0AlneknrT406pkh/ScBAFYmMpdo2scCOMpHcHHGroKc='

login_url = 'https://lift-apicn.vfsglobal.com/user/login'
data={ 'username':USERNAME,'password':PASSWORD,'missioncode':'ita','countrycode':'chn'}
login_headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Content-Length': '240',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://visa.vfsglobal.com',
    'Pragma': 'no-cache',
    'Referer': 'https://visa.vfsglobal.com/',
    'Route': 'chn/zh/ita',
    'Sec-Ch-Ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}


# 创建一个 CloudScraper 对象
scraper = cloudscraper.create_scraper()
response = scraper.post(login_url,headers=login_headers,data=data)
print('login', response.status_code)
#print(response.text)
if(response.status_code != 200):
    sys.exit()

time.sleep(3)

reservation_url = 'https://lift-apicn.vfsglobal.com/master/center/ita/chn/zh-CN'
reservation_headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Origin': 'https://visa.vfsglobal.com',
    'Pragma': 'no-cache',
    'Referer': 'https://visa.vfsglobal.com/',
    'Route': 'chn/zh/ita',
    'Sec-Ch-Ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

#response = requests.get(reservation_url, headers=reservation_headers)
#print('reservation',response.status_code)
#print('reservation',response.text)
#if(response.status_code != 200):
#    sys.exit()
#time.sleep(3)



check_url = 'https://lift-apicn.vfsglobal.com/appointment/CheckIsSlotAvailable'
check_data = {"countryCode":"chn","missionCode":"ita","vacCode":"GGH","visaCategoryCode":"D visa and Study visa","roleName":"Individual","loginUser":"SenGeMail@163.com","payCode":""}
check_headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Authorize': 'null',
    'Cache-Control': 'no-cache',
    'Content-Length': '169',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': 'https://visa.vfsglobal.com',
    'Pragma': 'no-cache',
    'Referer': 'https://visa.vfsglobal.com/',
    'Route': 'chn/zh/ita',
    'Sec-Ch-Ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}
#很抱歉，目前没有可预约时段。请稍后再试。
response = scraper.post(check_url,headers=check_headers,data=check_data)
print('check',response.status_code)
print('check',response.text)
if(response.status_code != 200):
    sys.exit()
