import requests


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