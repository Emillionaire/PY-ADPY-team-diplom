import configparser
import requests
from datetime import datetime
import sys
from pprint import pprint
import random
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from Vk_get import VkUsers
from sql import Sql_table
import re

def write_msg(user_id, message):
    authorize.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.randint(0, 2048)})

def sql_add():
    sql.add_person(p_info['response'][0]['id'],
                   p_info['response'][0]['first_name'] + ' ' + p_info['response'][0]['last_name'],
                   p_info['response'][0]['city']['id'], b_date, p_info['response'][0]['sex'])


path = 'settings.ini'
config = configparser.ConfigParser()
config.read(path)
tok = config.get("Tokens", "bot_token")

authorize = vk_api.VkApi(token=tok)

vku = VkUsers()
sql = Sql_table()

longpoll = VkLongPoll(authorize)
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        p_info = vku.get_person_info(event.user_id)
        if event.to_me and event.text.lower() == 'привет':
            b_date = p_info['response'][0]['bdate'][-4:]
            print(b_date)
            if not b_date.isdigit():
                write_msg(event.user_id, 'Укажите год рождения')
            else:
                sql_add()
        if event.to_me and event.text.isdigit():
            b_date = event.text
            print(b_date)
            sql_add()



