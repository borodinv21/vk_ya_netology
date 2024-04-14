import requests
from pprint import pprint
from datetime import datetime


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
    vk_client = VKAPIClient(token=vk_access_token)
    photos_info_items = vk_client.get_user_photos(user_id)['response']['items']

    pprint(vk_client.create_photos_info(photos_info_items))