import requests
from pprint import pprint
#disk_file_path - тут надо прописать, как будет называться файл на диске

class YaUploader:
    def __init__(self, token: str):
        self.token = token
        self.header = {
            'Content-Type': 'application/json', #себе: это обязательно, требование Яндекса!

            'Authorization': f'OAuth {token}'
        }

    def _get_upload_link(self, disk_file_path): #куда загружать, действительно 30 минут
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        param = {'path': disk_file_path, 'overwrite': 'true'}
        response = requests.get(upload_url, headers=self.header, params=param)
        return response.json()


    def upload(self, disk_file_path, file_name):
        href = self._get_upload_link(disk_file_path)['href']
        response = requests.put(href, data=open(file_name, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print('Ну, что-то получилось')



if __name__ == '__main__':
    token = input('Введите токен: ')
    file_name = input('Что загружаем? ')
    disk_file_path = input('А куда загружаем? ') + '/' + file_name
    uploader = YaUploader(token)
    result = uploader.upload(disk_file_path, file_name)

