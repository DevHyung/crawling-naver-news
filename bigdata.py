import time
from bs4 import BeautifulSoup
import requests
import json
""" 전역변수 AREA START"""
NEWS_PARSING_DELAY = 1 # 1초간격으로 가져온다는뜻 너무빨리가져오면 벤당함
header = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3239.132 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
}
url_r = "http://sports.news.naver.com/wfootball/news/index.nhn?date=20180601&type=latest"
url_p = "http://sports.news.naver.com/wfootball/news/index.nhn?date=20180601&type=popular"
output_r = open('./result_r.txt', 'w',encoding='UTF8')
output_p = open('./result_p.txt', 'w',encoding='UTF8')

url_base = 'https://sports.news.naver.com/wfootball/news/read.nhn?oid={}&aid={}' #기사상세정보 URL포맷
""" 전역변수 AREA END"""

response_r = requests.get(url_r,headers=header)
response_p = requests.get(url_p,headers=header)

soup_r = BeautifulSoup(response_r.text, 'lxml')
soup_p = BeautifulSoup(response_p.text, 'lxml')

### 인기순 파싱부분
url_list_p = []
result_p = soup_p.find_all("script")
script_p = result_p[-8].get_text().split('newsListModel:')[1][:-4]
json_r = json.loads(script_p)
print('[INFO] 파싱결과 인기순')
for article in json_r['list']:
    print(article['title'],url_base.format(article['oid'],article['aid']))
    url_list_p.append(url_base.format(article['oid'],article['aid']))
print("___"*30)
for url in url_list_p:
    html_p = requests.get(url,headers=header)
    bs4_p = BeautifulSoup(html_p.text,'lxml')
    content_p = bs4_p.find('div',id='newsEndContents')
    output_p.write(content_p.get_text().strip())
    time.sleep(NEWS_PARSING_DELAY)
output_p.close()
### 최신순 파싱부분
url_list_r = []
result_r = soup_r.find_all("script")
script_r = result_r[-8].get_text().split('newsListModel:')[1][:-4]
json_r = json.loads(script_r)
print('[INFO] 파싱결과 최신순')
for article in json_r['list']:
    print(article['title'],url_base.format(article['oid'],article['aid']))
    url_list_r.append(url_base.format(article['oid'],article['aid']))
print("___"*30)

for url in url_list_r:
    html_r = requests.get(url,headers=header)
    bs4_r = BeautifulSoup(html_r.text,'lxml')
    content_r = bs4_r.find('div',id='newsEndContents')
    output_r.write(content_r.get_text().strip())
    #print(content_r.get_text().strip())#TEST
    time.sleep(NEWS_PARSING_DELAY)
output_r.close()
