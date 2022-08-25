import configparser
import requests
from datetime import datetime
from PIL import Image
import sys
from pprint import pprint
import random
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from Vk_get import VkUsers
from sql import Sql_table

def write_msg(user_id, message):
    authorize.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.randint(0, 2048)})

tok = 'vk1.a.rcp2FueTHGts8y7r1dz9hefmlm1ot5rgiEsBWV52urMzufSBvaSBp7qk2BugAh1NaPly74Hli04pqL2zdUubI98-46ZT_H41i0p_hBIfJAM6mZhnXW_9ikYWLGUcFG6qKeMPDmzYm9OzCu04j-Mq1K3LUxdimqaeWcSUKp03h6Q27rnMDUc6VqGT6vPNHajq'
authorize = vk_api.VkApi(token=tok)

vku = VkUsers()
sql = Sql_table()

longpoll = VkLongPoll(authorize)
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            p_info = vku.get_person_info(event.user_id)
            print(p_info['response'])
            # sql.add_person(p_info['response'])
            sql.add_person(p_info['response'][0]['id'], p_info['response'][0]['first_name']+' '+p_info['response'][0]['last_name'], p_info['response'][0]['city']['id'], p_info['response'][0]['bdate'][-4:])
            # write_msg(event.user_id, "Хай")
            # print(p_info['response'])

