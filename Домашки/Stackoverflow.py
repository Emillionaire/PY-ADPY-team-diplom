import requests
import time
from time import sleep


def q_about_what(tag):
    url = "https://api.stackexchange.com/2.3/questions?page="
    page = 1
    count = 0
    flag = True
    while page <= 25 and flag == True:
      need_url = f'{url}{page}&pagesize=100&fromdate={(int(time.time()) - 172800)}&order=asc&sort=creation&tagged={tag}&site=stackoverflow'
      resp = requests.get(need_url)
      some_list = resp.json()['items']
      flag = bool(some_list)
      for i in some_list:
        print(i['link'])
        count +=1
      page += 1
      sleep(2)
    print(f'Всего найдено {count} вопросов')


if __name__ == '__main__':
  q_about_what('python')


