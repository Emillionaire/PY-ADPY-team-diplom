import requests
from bs4 import BeautifulSoup

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Cookie': '_ym_d=1648243538; _ym_uid=16482435381034256811; _ga=GA1.2.1456918074.1648243538; hl=ru; fl=ru; visited_articles=480838:488054:478934:470828:210420:534250:535156:280238:555028:442800; _ym_isad=2; _gid=GA1.2.42061408.1659463597; habr_web_home_feed=/all/; _gat_gtag_UA_726094_1=1',
'Host': 'habr.com',
'Referer': 'https://github.com/netology-code/py-homeworks-advanced/blob/master/6.Web-scrapping/README.md',
'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
'sec-ch-ua-mobile': '?0',
'sec-ch-ua-platform': '"Windows"',
'Sec-Fetch-Dest': 'document',
'Sec-Fetch-Mode': 'navigate',
'Sec-Fetch-Site': 'same-origin',
'Sec-Fetch-User': '?1',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
res = requests.get('https://habr.com/ru/all/', headers=headers)
soup = BeautifulSoup(res.text, 'html.parser')
KEYWORDS = ['дизайн', 'фото', 'web', 'python']
texts = soup.findAll(class_='tm-article-snippet')
for text in texts:
    url = text.find(class_='tm-article-snippet__readmore')
    res2 = requests.get('https://habr.com'+ url.get('href'), headers=headers)
    soup2 = BeautifulSoup(res2.text, 'html.parser')
    resres = soup2.find(class_='tm-article-body').find_all('div')
    for i in resres:
        a = i.get_text()
        flag = False
        for i in KEYWORDS:
            if i in a:
                url2 = 'https://habr.com'+ url.get('href')
                name = text.find(class_='tm-article-snippet__title-link').get_text()
                time = (BeautifulSoup(str(text.find(class_='tm-article-snippet__datetime-published').find('time')), 'lxml').time.attrs['title'])
                flag = True
                print(f'{time} - {name} - {url2}')
                break
        if flag:
            break
