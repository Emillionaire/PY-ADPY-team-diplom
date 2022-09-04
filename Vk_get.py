import configparser
from pprint import pprint

import requests

from sql import Sql_table

sql = Sql_table()

class VkUsers:

    def __init__(self):
        self.path = 'settings.ini'
        self.config = configparser.ConfigParser()
        self.config.read(self.path)
        self.token = self.config.get("Tokens", "vk_token")

    def get_person_info(self, id):
        URL = 'https://api.vk.com/method/users.get'
        params = {
            'fields': 'interests, books, bdate, city, sex',
            'user_ids': id,
            'access_token': self.token,
            'v': '5.89'
        }
        res = requests.get(URL, params=params)
        return res.json()

    def get_another_people(self, user_id):
        URL = 'https://api.vk.com/method/users.search'
        result = sql.take_user_data(user_id)
        vk_id = result['vk_id']
        name = result['name']
        city = result['city']
        bdate = result['bdate']
        sex = result['sex']
        if sex == 1:
            target_sex = 2
        else:
            target_sex = 1

        params = {
            'sort': 0,
            'count': 100,
            'city': city,
            'birth_year': bdate,
            'sex': target_sex,
            'access_token': self.token,
            'v': '5.89',
            'fields': 'city, relation, bdate'
        }

        result = requests.post(URL, params=params)

        return result.json()
        # pprint(result.json())

    def get_photos(self, relevant_id):
        URL = 'https://api.vk.com/method/photos.get'
        user_id = relevant_id
        params = {
            'user_ids': user_id,
            'access_token': self.token,
            'v':'5.131',
            'owner_id': user_id,
            'album_id': 'profile',
            'extended' : '1',
            'count': '999',
        }
        res = requests.get(URL, params=params)
        photo_dict = {}
        photo_list = []
        result = res.json()['response']['items']
        # pprint(result)
        for photos in result:
            like = photos['likes']['count']
            for photo in photos['sizes']:
                photo['likes'] = like
                photo['id'] = photos['id']
                photo['owner_id'] = photos['owner_id']
                f_photo = {key: photo[key] for key in photo if key not in ['height', 'width']}
                photo_dict = {**photo_dict, **f_photo}
            photo_list.append([*photo_dict.values()])
            photo_list.sort(key=lambda i: i[2], reverse=True)
        return photo_list

        # pprint(photo_list)



vvv = VkUsers()
vvv.get_another_people(197865810)