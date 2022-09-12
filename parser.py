import configparser
import traceback
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

settings = dict(one_time=True, inline=False)
keyboard = VkKeyboard(**settings) #клавиатура из одной кнопки
keyboard.add_button('Next', color=VkKeyboardColor.PRIMARY)

full_kb = VkKeyboard(**settings) #полная клавиатура
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
                if not item['is_closed']:
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
                rel_foto = vku.get_photos(collection[coll_i][0])
                photos = []
                if rel_foto:
                    for foto in rel_foto[0:3]:
                        photos.append(f'photo{foto[4]}_{foto[3]}_{vk_tok}')
                    vk.messages.send(
                        random_id=random.randint(0, 2048),
                        peer_id=event.peer_id,
                        attachment=photos,
                        message=f'{collection[coll_i][1]}\nhttps://vk.com/id{collection[coll_i][0]}')
                    coll_i += 1
                    button('Жми кнопки и будет тебе счастье', full_kb)
                else:
                    vk.messages.send(
                        random_id=random.randint(0, 2048),
                        peer_id=event.peer_id,
                        attachment=photos,
                        message=f'Фотографий у этого пользователя нет\n{collection[coll_i][1]}\nhttps://vk.com/id{collection[coll_i][0]}')
                    coll_i += 1
                    button('Жми кнопки и будет тебе счастье', full_kb)
            except KeyError:
                traceback.print_exc()
                write_msg(event.user_id, 'Люди кончились, иди работать')
                coll_i = 0
        elif event.to_me and event.text.lower() == 'like':
            sql.make_favorite(event.user_id, collection[coll_i-1][0])
            button('Добавлено, продолжаем?', keyboard)

        elif event.to_me and event.text.lower() == 'избранное':
            fav = sql.show_favorites(event.user_id)
            fav_list = ''
            for i in fav:
                fav_list += (f'{i[1]}: https://vk.com/id{i[0]}\n')
            pprint(fav_list)
            vk.messages.send(
                random_id=random.randint(0, 2048),
                peer_id=event.peer_id,
                message=fav_list)


