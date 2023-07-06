import requests
import logging
import pymongo

url = 'https://spa1.scrape.center/'
html = requests.get(url).text
#print(html)


logging.basicConfig(level=logging.INFO,format='%(asctime)s -%(levelname)s:%(message)s')
INDEX_URL = 'https://spa1.scrape.center/api/movie/?limit={limit}&offset={offset}'


def scrape_api(url):
    logging.info('scrape url:%s',url)
    try:
        response = requests.get(url)#其实就是请求Ajax的API
        if response.status_code == 200:
            return response.json()
    except response.RequestExcception:
        logging.error('error occurred while scraping %s',url,exc_info=True)



































































        

#爬取一页
LIMIT = 10
def scrape_index(page):
    url = INDEX_URL.format(limit=LIMIT,offset=LIMIT*(page - 1))
    return scrape_api(url)

DETAIL_URL = 'https://spa1.scrape.center/api/movie/{id}'

def scrape_detail(id):
    url = DETAIL_URL.format(id=id)
    return scrape_api(url)



client = pymongo.MongoClient("mongodb://root:root@192.168.20.5:28001/")
try:
    client.admin.command('ping')
    logging.info("连接成功")
except:
    logging.info("连接失败")

db = client['movies']
collection = db['movies']

def save_data(data):
    collection.update_one({'name':data.get('name')},{'$set':data},upsert=True)



TOTAL_PAGE = 10
def main():
    for page in range(1,TOTAL_PAGE+1):
        index_data = scrape_index(page)
        for item in index_data.get('results'):
            id = item.get('id')
            detail_data = scrape_detail(id)
            save_data(detail_data)
            logging.info('detail data %s',detail_data)



if __name__ == '__main__':
    main()
