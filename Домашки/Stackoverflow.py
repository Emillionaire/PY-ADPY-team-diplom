import requests
import time
from datetime import date

def q_about_what(tag):
    d = date.today()
    url = "https://api.stackexchange.com/2.3/questions?fromdate="
    need_url = f'{url}{(int(time.mktime(d.timetuple()))-172800+10800)}&todate={int(time.mktime(d.timetuple()))+10800}&order=desc&sort=creation&tagged={tag}&site=stackoverflow'
    resp = requests.get(need_url)
    some_list = resp.json()['items']
    for i in some_list:
        print(i['link'])
q_about_what('Python')


