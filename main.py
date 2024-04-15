import requests
import json
from pprint import pprint
from datetime import datetime
#from config import vk_access_token, vk_user_id, yandex_access_token - импортирую отдельный файл с токенами, он находится в gitignore
#Ниже описал куда необходимо вставить токены и id пользователя


class YANDEXAPIClient:
    API_BASE_URL = 'https://cloud-api.yandex.net/v1/disk/'

    def __init__(self, token):
        self.token = token


    def create_folder(self, folder_name):
        url_resources = 'resources?'
        params = {
            'path': folder_name
        }
        headers = {
            'Authorization': f'OAuth {self.token}'
        }

        response = requests.put(self.API_BASE_URL + url_resources, params=params, headers=headers)

        return response


    def get_yandex_upload_photos_response(self, folder_name, image_name):
        url_resources = 'resources/upload'
        params = {
            'path': f"{folder_name}/{image_name}"
        }
        headers = {
            'Authorization': f'OAuth {self.token}'
        }

        response = requests.get(self.API_BASE_URL + url_resources, params=params, headers=headers)

        return response

    def get_file_info(self, folder_name, image_name):
        url_resources = 'resources?'
        params = {
            'path': f"{folder_name}/{image_name}"
        }
        headers = {
            'Authorization': f'OAuth {self.token}'
        }

        response = requests.get(self.API_BASE_URL + url_resources, params=params, headers=headers)

        return response


class VKAPIClient:
    API_BASE_URL = 'https://api.vk.com/method/'

    def __init__(self, token):
        self.token = token

    def get_api_method_url(self, api_method):
        return f'{self.API_BASE_URL}{api_method}?'

    def get_user_photos(self, user_id):
        params = {
            'access_token': self.token,
            'owner_id': user_id,
            'album_id': 'profile',
            'v': '5.199',
            'extended': 1
        }

        response = requests.get(self.get_api_method_url('photos.get'), params=params)

        return response.json()

    def create_photos_info(self, items_list):
        photos_info_list = []

        for photo in items_list:
            date = datetime.fromtimestamp(photo['date'])

            photo_info = {}
            photo_info['date'] = f'{date.day}.{date.month}.{date.year}'
            photo_info['likes'] = photo['likes']['count']

            size_type = ''
            photo_height = 0
            photo_width = 0
            photo_url = ''

            for size in photo['sizes']:
                if size['height'] > photo_height and size['width'] > photo_width:
                    size_type = size['type']
                    photo_width = size['width']
                    photo_height = size['height']
                    photo_url = size['url']

            photo_info['size'] = size_type
            photo_info['url'] = photo_url

            photos_info_list.append(photo_info)

        return photos_info_list



if __name__ == '__main__':
    # vk_access_token = Здесь вводите свой токен
    # vk_user_id = Здесь введите свой id пользователя
    # yandex_access_token = Здесь введите свой яндекс токен

    data_json = []

    vk_client = VKAPIClient(token=vk_access_token)
    photos_info_items = vk_client.get_user_photos(vk_user_id)['response']['items']
    photos_list = vk_client.create_photos_info(photos_info_items)
    print('Получили доступ к API VK')

    print('Вывожу информацию о фотографиях профиля')
    pprint(vk_client.create_photos_info(photos_info_items))

    ya_client = YANDEXAPIClient(yandex_access_token)
    print('Получили доступ к API Yandex')

    ya_client.create_folder('Images')
    print('Создаю папку с именем Images в Яндекс Диске', end='\n'*2)

    for photo in photos_list:
        print('Считываю информацию о фотографии...')

        response = requests.get(photo['url'])
        image_name = f"{photo['likes']}.jpg"
        print(f'Создаю файл с именем {image_name}')

        file_info = ya_client.get_file_info('Images', image_name)

        if file_info.json().get('error') == None:
            image_name = f"{photo['likes']}_{photo['date']}.jpg"
            print('Внимание! Файл с таким именем уже существует! Добавляю к имени файла дату загрузки!')
            print(f'Теперь файл называется {image_name}')

        with open(image_name, 'wb') as file:
            file.write(response.content)
            print('Записываю файл на локальный компьютер...')

        yandex_response = ya_client.get_yandex_upload_photos_response('Images', image_name)
        print('Получил ссылку на загрузку фотографии в Яндекс Диск...')

        with open(image_name, 'rb') as file:
            try:
                requests.put(yandex_response.json()['href'], files={'file': file})
                print(f'Поздравляю! Фотография с именем {image_name} была загружена в папку Images')
                data_json.append(
                    {
                        'file_name': image_name,
                        'size': photo['size']
                    }
                )
            except:
                print('Фото с таким именем уже существует! Вы загружаете фотографию, которая уже хранится в папке Images')
                data_json.append(
                    {
                        'file_name': image_name,
                        'size': photo['size'],
                        'error': 'Файл уже загружен на Яндекс Диск'
                    }
                )

        print('\n')

    with open('data.json', 'w') as file:
        json.dump(data_json, file)