import requests
import json
import io

IP_DETECT_HTTP_SERVICE = 'https://api.ipify.org?format=json'
GEO_DETECT_SERVICE = 'https://ipinfo.io/'
YD_API_URL = 'https://cloud-api.yandex.net/v1/disk/resources'
YD_FOLDER_PATH = 'PY-148/Karandakov_JSON_IP_GEO_DETECT'

class IPDetector:
    """Класс определения IP и местонахождения"""

    def detect_ip(self):
        try:
            response = requests.get(IP_DETECT_HTTP_SERVICE)
            response.raise_for_status()
            ip_detected = response.json()
            print(f'Ваш IP:{ip_detected}')
            return ip_detected['ip']

        except requests.exceptions.RequestException as e:
            print(f'Не удалось определить IP из-за ошибки:{e}')
            return None

    def detect_geo(self, ip):
        try:
            url = f'{GEO_DETECT_SERVICE}{ip}/geo'
            response = requests.get(url)
            geo_detected = response.json()
            print(f'Ваше местонахождение:{geo_detected}')
            return geo_detected
        except requests.exceptions.RequestException as e:
            print(f'Не удалось определить местонахождение из-за ошибки:{e}')

class YandexDiskUploader:
    """работаем с яндекс диском"""
    def __init__(self, yd_token):
        self.headers = {'Authorization': f'OAuth {yd_token}'}

    def create_folder(self, path):
        """создаем папку на диске"""
        params = {'path': path}
        response = requests.put(YD_API_URL, headers=self.headers, params=params)
        if response.status_code == 201:
            print(f'Папка {YD_FOLDER_PATH} создана!')
        elif response.status_code == 409:
            print('Папка уже существует.')
        else:
            print(f'Ошибка: {response.status_code}, {response.json().get('message')}')

    def upload_json_file(self, temp_file):
        """загружаем файл в яндекс диск"""
        params = {'path': f'{YD_FOLDER_PATH}/geoinfo.json',
                  'overwrite': True}
        res = requests.get(YD_API_URL, headers=self.headers, params=params)
        upload_url = res.json().get('href')
        if upload_url:
            json_as_bytes = json.dumps(temp_file, ensure_ascii=False, indent=4).encode('utf-8')
            temp_file_in_memory = io.BytesIO(json_as_bytes)
            response = requests.put(upload_url, files={'file': ('geoinfo.json', temp_file_in_memory)})
            # with open ('info.json', 'rb') as f:
            #     response = requests.put(upload_url, files={'file':f})
            if response.status_code == 201:
                print('JSON успешно записан в папку на Яндекс диск')
            else:
                print(f'Ошибка: {response.status_code}')


def main():
    """Вызов методов у класса происходит в функции main - как скажете"""

    ip_detector = IPDetector()
    yd_token = input('Введите Ваш токен Яндекс Диска: ')
    yd_uploader = YandexDiskUploader(yd_token)
    got_ip = ip_detector

    #получаем ip и местонахождение
    got_ip = ip_detector.detect_ip()
    if got_ip:
        got_geo = ip_detector.detect_geo(ip=got_ip)
        if got_geo:
            geo_ip_info = {'ip': got_ip,
                   'geo': got_geo}
            yd_uploader.create_folder(YD_FOLDER_PATH)
            yd_uploader.upload_json_file(geo_ip_info)
    else:
        print('IP не определен, анонимус!')

if __name__ == "__main__":
    main()


    # #запишем на яндекс диск
    # yd_token = input(f'Введите Ваш токен Яндекс Диска:')
    # headers = {'Authorization': f'OAuth {yd_token}'}
    # params = {'path': YD_FOLDER_PATH}
    #
    # # создаем папку
    # response = requests.put(YD_API_URL, headers=headers, params=params)
    # if response.status_code == 201:
    #     print(f'Папка {YD_FOLDER_PATH} создана!')
    # elif response.status_code == 409:
    #     print('Папка уже существует.')
    # else:
    #     print(f'Ошибка: {response.status_code}, {response.json().get('message')}')
    #получаем ссылку для загрузки:


