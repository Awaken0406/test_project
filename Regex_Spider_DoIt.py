import requests
import logging
import re
from urllib.parse import urljoin
from requests.packages import urllib3

import json
from os import makedirs
from os.path import exists

import multiprocessing

urllib3.disable_warnings()#忽略验证警告

logging.basicConfig(level=logging.INFO,format='%(asctime)s -%(levelname)s:%(message)s')
BASE_URL = 'https://ssr1.scrape.center'
TOTAl_PAGE = 10


def scrape_page(url):
    logging.info('scraping %s...',url)
    try:
        response = requests.get(url,verify=False)
        if response.status_code == 200:
            return response.text
        else:
            logging.error('get invalid status code %s while scraping %s',response.status_code,url)
    except requests.RequestException:
        logging.error('error occurred while scraping %s',url,exc_info=True)


def scrape_index(page):
    index_url = f'{BASE_URL}/page/{page}'
    return scrape_page(index_url)

#解析列表页
def parse_index(html):
    pattern = re.compile('<a.*?href="(.*?)".*?class="name">')
    items = re.findall(pattern,html)
    if not items:
        return []
    for item in items:
        detail_url = urljoin(BASE_URL,item)
        logging.info('get detail url %s',detail_url)
        yield detail_url



#获取详情页
def scrape_detail(url):
    return scrape_page(url)

#解析详情页
def parse_detail(html):
    cover_pattern = re.compile('class="item.*?<img.*?src="(.*?)".*?class="cover">',re.S)#获取封面url
    name_pattern = re.compile('<h2.*?>(.*?)</h2>')#电影名字
    categories_pattern = re.compile('class="categories".*?<span>(.*?)</span>',re.S)#标签
    published_at_pattern = re.compile('(\d{4}-\d{2}-\d{2})\s?上映')#上映时间
    drama_pattern = re.compile('<div.*?drama.*?>.*?<p.*?>(.*?)</p>',re.S)#剧情
    score_pattern = re.compile('<p.*?score.*?>(.*?)</p>',re.S)#评分
    
    cover = re.search(cover_pattern,html)
    name = re.search(name_pattern,html)
    categories = re.findall(categories_pattern,html)
    published = re.search(published_at_pattern,html)
    score = re.search(score_pattern,html)
    drama = re.search(drama_pattern,html)
    
    if cover:
            cover = cover.group(1).strip() 
    if name:
         name = name.group(1).strip()
    if categories:
         categories = categories
    if published:
         published = published.group(1).strip()
    if score:
         score = score.group(1).strip()   
    if drama:
         drama = drama.group(1).strip()   

    return {
        'cover':cover,
        'name':name,
        'categories':categories,
        'published':published,
        'drama':drama,
        'score':score
    }


RESULT_DIR = 'results'
exists(RESULT_DIR) or makedirs(RESULT_DIR)

def save_data(data):
    name = data.get('name')
    data_path = f'{RESULT_DIR}/{name}.json'
    json.dump(data,open(data_path,'w',encoding='utf-8'), ensure_ascii=False,indent=2)

    




def main(page):

    index_html = scrape_index(page)#获取列表页面网页
    detail_urls = parse_index(index_html)#解析出每部电影的连接
     #logging.info('detail urls %s', list(detail_urls))
    for detail_url in detail_urls:
        detail_html = scrape_detail(detail_url)
        data = parse_detail(detail_html)
        #logging.info('get detail data %s', data)
        save_data(data)

    logging.info('over !!!')

if __name__ =='__main__':
    pool = multiprocessing.Pool()
    pages = range(1,TOTAl_PAGE+1)
    pool.map(main,pages)
    pool.close()
    pool.join()
