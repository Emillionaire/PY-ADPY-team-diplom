import configparser
import requests
from datetime import datetime
import sys
import json
from pprint import pprint
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
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
vk = authorize.get_api()

vku = VkUsers()
sql = Sql_table()
settings = dict(one_time=False, inline=True)
keyboard = VkKeyboard(**settings)
keyboard.add_button('Привет', color=VkKeyboardColor.NEGATIVE)

longpoll = VkLongPoll(authorize) #Слушаем чат
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW: #Вот нам написали
        if not sql.we_know_him(event.user_id): #Если его id ет в таблице person, то:
            p_info = vku.get_person_info(event.user_id)  # дёргаем о пользователе информацию
            if event.to_me and event.text.lower() == 'начать': #"начать" появляется по кнопке
                b_date = p_info['response'][0]['bdate'][-4:] #проверяем, указан ли у него год рождения
                if not b_date.isdigit():  #Если года рождения нет
                    write_msg(event.user_id, 'Укажите год рождения') #спрашиваем его
                else:
                    sql_add() #если всё ок, сразу добавляем в БД
            if event.to_me and event.text.isdigit(): #это он пишет нам год
                b_date = event.text
                sql_add() #и мы добавляем человека в БД
        elif event.to_me:
            write_msg(event.user_id, 'Lhfnenb') #на это пока не обращай внимание, это я кнопки пытаюсь сделать
            vk.messages.send(
                keyboard=keyboard.get_keyboard(),
                random_id=random.randint(0, 2048),
                key=('d888bf02174ccfde5be21361b1fbe65490434c8b'),
                server=("https://lp.vk.com/wh72316872"),
                ts=('1'),
                message='Держи',
                user_id=event.user_id
            )



