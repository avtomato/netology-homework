import requests
import json
from time import sleep

VERSION = '5.62'  # Версия API
TOKEN = ''  # Ваш access_token
params = {'v': VERSION, 'access_token': TOKEN}


def get_id():
    """Получаем список, содержащий id наших друзей."""
    r = requests.get('https://api.vk.com/method/friends.get', params=params)
    user_ids = r.json()['response']['items']
    return user_ids


def get_friends(user_ids):
    """Получаем словарь где ключом является id пользователя, а значением список его друзей."""
    friends = {}
    for user_id in user_ids:
        # тайм-аут между запросами (число запросов не должно превышать трех в секунду)
        sleep(2)
        # ловим исключения в случае если страница была удалена
        try:
            if user_id:
                params['user_id'] = user_id
            r = requests.get('https://api.vk.com/method/friends.get', params=params)
            friends[user_id] = (r.json()['response']['items'])
        except KeyError:
            continue
    return friends


def intersection_friends():
    """Получаем  список общих друзей у  двух пользователей из нашего списка друзей."""
    user_ids = get_id()
    friends = get_friends(user_ids)
    print('Done')
    # Вводим id пользователей
    x = int(input())
    y = int(input())
    intersection = set(friends[x]).intersection(set(friends[y]))
    return intersection


def write_json():
    """Записываем полученный словарь в json file."""
    user_ids = get_id()
    data = get_friends(user_ids)
    with open('friends.json', 'w') as json_file:
        json.dump(data, json_file, indent=2, ensure_ascii=False)
        print('Done')


def intersection_friends_from_file():
    """Получаем  список общих друзей у  двух пользователей из нашего списка друзей."""
    with open('friends.json', 'r') as json_file:
        friends = json.load(json_file)
        # Вводим id пользователей
        x = input()
        y = input()
        intersection = set(friends[x]).intersection(set(friends[y]))
        return intersection

intersection_friends()
