import requests
from bs4 import BeautifulSoup
import time
from time import sleep
from pprint import pprint
import pandas as pd

def question_text(url):
    my_data = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    quotes = soup.find_all('div', class_='question')
    for i in quotes:
        itemName = i.find('div', class_='s-prose js-post-body').text.strip()
        my_data.append(itemName)
    return (my_data)

def q_about_what(tag):
    url = "https://api.stackexchange.com/2.3/questions?page="
    page = 1
    count = 0
    links = []
    flag = True
    while page <= 1 and flag == True:
        need_url = f'{url}{page}&pagesize=100&fromdate={(int(time.time()) - 172800)}&order=asc&sort=creation&tagged={tag}&site=stackoverflow'
        resp = requests.get(need_url)
        some_list = resp.json()['items']
        flag = bool(some_list)
        for i in some_list:
            links.append(i['link'])
            count += 1
        page += 1
        sleep(2)
    return (links)
    print(f'Всего найдено {count} вопросов')


def question_text(tag):
    links = q_about_what(tag)
    my_data = []
    for url in links:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        quotes = soup.find_all('div', class_='question')
        for i in quotes:
            itemName = i.find('div', class_='s-prose js-post-body').text.strip()
            my_data.append(itemName)
    return (my_data)


def to_excel(tag):
    dict = {}
    links = q_about_what(tag)
    my_data = question_text(tag)
    dict['Вопросы'] = my_data
    dict['Ссылки'] = links
    df = pd.DataFrame(dict)
    df.to_excel('Excel.xlsx')

if __name__ == '__main__':
    to_excel('python')
