import configparser
import requests
from datetime import datetime
import sys
import json
import vk
from pprint import pprint
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import random
import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from Vk_get import VkUsers
from sql import Sql_table


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
vk_tok = config.get("Tokens", "vk_token")

authorize = vk_api.VkApi(token=tok)
vk = authorize.get_api()
upload = VkUpload(authorize)


vku = VkUsers()
sql = Sql_table()
settings = dict(one_time=False, inline=True)
keyboard = VkKeyboard(**settings)
keyboard.add_button('Next', color=VkKeyboardColor.PRIMARY)

full_kb = VkKeyboard(**settings)
full_kb.add_button('Like', color=VkKeyboardColor.POSITIVE)
full_kb.add_button('В ЧС', color=VkKeyboardColor.NEGATIVE)
full_kb.add_button('Избранное', color=VkKeyboardColor.POSITIVE)
full_kb.add_button('Next', color=VkKeyboardColor.PRIMARY)

def button(message, kb):
    vk.messages.send(
        keyboard=kb.get_keyboard(),
        random_id=random.randint(0, 2048),
        key=(config.get("Buttons", "key")),
        server=(config.get("Buttons", "server")),
        ts=(config.get("Buttons", "ts")),
        message=message,
        user_id=event.user_id)



coll_i = 0

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
        elif event.to_me and event.text.lower() == 'начать':
            one_list = []
            person_list = vku.get_another_people(event.user_id)['response']['items']
            # pprint(person_list)
            for item in  person_list:
                name = item['first_name']+' '+ item['last_name']
                if 'city' in item.keys() and item['city']['id'] == int(sql.take_user_data(event.user_id)['city']):
                    if 'relation' in item.keys() and item['relation'] not in (2,3,4,7,8):
                        one_list.append((item['id'], name))
                    elif 'relation' not in item.keys():
                        one_list.append((item['id'], name))
            for i in one_list:
                sql.add_relevant_persons(event.user_id, int(i[0]), i[1]) #добавили всех релевантных в таблицу
            button('Ну, погнали, жми кнопку', keyboard)

        elif event.to_me and event.text.lower() == 'next':
            collection = sql.take_relevant_user(event.user_id)
            try:
                peer_id = event.peer_id
                rel_foto = vku.get_photos(collection[coll_i])
                photos = []
                for foto in rel_foto[0:3]:
                    photos.append(f'photo{foto[4]}_{foto[3]}_{vk_tok}')
                vk.messages.send(
                    random_id=random.randint(0, 2048),
                    peer_id=peer_id,
                    attachment=photos,
                    message=None)
                coll_i += 1
                button('Жми кнокпи и будет тебе счастье', full_kb)
            except KeyError:
                write_msg(event.user_id, 'Люди кончились, иди работать')
                coll_i = 0





