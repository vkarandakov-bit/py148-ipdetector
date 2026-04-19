import requests
import json

IP_DETECT_HTTP_SERVICE = 'https://api.ipify.org?format=json'
GEO_DETECT_SERVICE = 'https://ipinfo.io/'
YD_API_URL = 'https://cloud-api.yandex.net/v1/disk/resources'
YD_FOLDER_PATH = 'PY-148/Karandakov_JSON_IP_GEO_DETECT'

def detect_ip():
    try:
        response = requests.get(IP_DETECT_HTTP_SERVICE)
        response.raise_for_status()
        ip_detected = response.json()
        print(f'Ваш IP:{ip_detected}')
        return ip_detected['ip']

    except requests.exceptions.RequestException as e:
        print(f'Не удалось определить IP из-за ошибки:{e}')
        return None

def detect_geo(ip):
    try:
        url = f'{GEO_DETECT_SERVICE}{ip}/geo'
        response = requests.get(url)
        geo_detected = response.json()
        print(f'Ваше местонахождение:{geo_detected}')
        return geo_detected
    except requests.exceptions.RequestException as e:
        print(f'Не удалось определить местонахождение из-за ошибки:{e}')

#получаем ip и местонахождение
got_ip = detect_ip()
got_geo = detect_geo(ip=got_ip)

if got_ip:

    geo_ip_info = {'ip': got_ip,
                   'geo': got_geo}
    with open('info.json', 'w', encoding='utf-8') as f:
        json.dump(geo_ip_info, f, ensure_ascii=False, indent=4)
    print('JSON сохранен')
    print(json.dumps(geo_ip_info, ensure_ascii=False, indent=4))

    #запишем на яндекс диск
    yd_token = input(f'Введите Ваш токен Яндекс Диска:')
    headers = {'Authorization': f'OAuth {yd_token}'}
    params = {'path': YD_FOLDER_PATH}

    # создаем папку
    response = requests.put(YD_API_URL, headers=headers, params=params)
    if response.status_code == 201:
        print(f'Папка {YD_FOLDER_PATH} создана!')
    elif response.status_code == 409:
        print('Папка уже существует.')
    else:
        print(f'Ошибка: {response.status_code}, {response.json().get('message')}')
    #получаем ссылку для загрузки:

    params = {'path': f'{YD_FOLDER_PATH}/geoinfo.json',
            'overwrite': True}
    #res = requests.get(YD_API_URL, headers=headers, params=params)
    upload_url = requests.get(f'{YD_API_URL}/upload', headers=headers, params=params).json().get('href')
    with open ('info.json', 'rb') as f:
        response = requests.put(upload_url, files={'file':f})
    if response.status_code == 201:
        print('JSON успешно записан в папку на Яндекс диск')
    else:
        print(f'Ошибка: {response.status_code}')
