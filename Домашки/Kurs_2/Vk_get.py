import vk_api
import configparser
import requests

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

