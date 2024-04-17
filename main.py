import requests
import logging
import json

from YANDEXAPIClient import YANDEXAPIClient
from VKAPIClient import VKAPIClient


if __name__ == '__main__':
    logging.basicConfig(filename="myapp.log", level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    logger = logging.getLogger("myapp.log")
    handler = logging.StreamHandler()
    logger.addHandler(handler)

    logger.info("Запуск программы")

    vk_access_token = input('Введите свой токен доступа для ВК: ')
    vk_user_id = int(input('Введите id пользователя ВК: '))
    yandex_access_token = input('Введите свой токен от Яндекс Полигон: ')

    data_json = []

    vk_client = VKAPIClient(token=vk_access_token)
    photos_info_items = vk_client.get_user_photos(vk_user_id)['response']['items']
    photos_list = vk_client.create_photos_info(photos_info_items)
    logger.info('Получили доступ к API VK')

    logger.info('Вывожу информацию о фотографиях профиля')
    logger.info(vk_client.create_photos_info(photos_info_items))

    ya_client = YANDEXAPIClient(yandex_access_token)
    logger.info('Получили доступ к API Yandex')

    ya_client.create_folder('Images')
    logger.info('Создаю папку с именем Images в Яндекс Диске')

    for photo in photos_list:
        logger.info('\n' * 2)
        logger.info('Считываю информацию о фотографии...')

        response = requests.get(photo['url'])
        image_name = f"{photo['likes']}.jpg"
        logger.info(f'Создаю файл с именем {image_name}')

        file_info = ya_client.get_file_info('Images', image_name)

        if file_info.json().get('error') == None:
            image_name = f"{photo['likes']}_{photo['date']}.jpg"
            logger.info('Внимание! Файл с таким именем уже существует! Добавляю к имени файла дату загрузки!')
            logger.info(f'Теперь файл называется {image_name}')

        with open(image_name, 'wb') as file:
            file.write(response.content)
            logger.info('Записываю файл на локальный компьютер...')

        yandex_response = ya_client.get_yandex_upload_photos_response('Images', image_name)
        logger.info('Получил ссылку на загрузку фотографии в Яндекс Диск...')

        with open(image_name, 'rb') as file:
            try:
                requests.put(yandex_response.json()['href'], files={'file': file})
                logger.info(f'Поздравляю! Фотография с именем {image_name} была загружена в папку Images')

                data_json.append(
                    {
                        'file_name': image_name,
                        'size': photo['size']
                    }
                )
            except:
                logger.info('Фото с таким именем уже существует! Вы загружаете фотографию, которая уже хранится в папке Images')
                logger.error('Отмена загрузки фото!')
                data_json.append(
                    {
                        'file_name': image_name,
                        'size': photo['size'],
                        'error': 'Файл уже загружен на Яндекс Диск'
                    }
                )

    logger.warning('\n')
    logger.warning('Программа завершила свою работу...')

    with open('data.json', 'w') as file:
        json.dump(data_json, file)