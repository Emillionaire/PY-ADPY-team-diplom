import requests
import time

def q_about_what(tag):
    url = "https://api.stackexchange.com/2.3/questions?fromdate="
    need_url = f'{url}{(int(time.time())-172800)}&todate={int(time.time())}&order=desc&sort=creation&tagged={tag}&site=stackoverflow'
    resp = requests.get(need_url)
    some_list = resp.json()['items']
    for i in some_list:
        print(i['link'])
q_about_what('Python')


