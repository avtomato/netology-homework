#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import sys
import os
import argparse
import logging
from collections import defaultdict, OrderedDict
from time import sleep

import json

__title__ = "UniGrouper - finder of user's unique groups"
__author__ = 'Maksim Vasyunin'
__version__ = 'ver. 0.0.1'
__description__ = "Get a list of user's groups, that exclude user's friends"

# Версия API
_VERSION = '5.64'
# access_token
_TOKEN = 'd13e692be69592b09fd22c77a590dd34e186e6d696daa88d6d981e1b4e296b14acb377e82dcbc81dc0f22'


logger = logging.getLogger(__name__)


# Получаем список id друзей пользователя
def get_user_friends(params=None, **kwargs):
    r = requests.get('https://api.vk.com/method/friends.get', params=params, **kwargs)
    friends = r.json()['response']['items']
    return friends


# Получаем список id групп пользователя
def get_user_groups(params=None, **kwargs):
    r = requests.get('https://api.vk.com/method/groups.get', params=params, **kwargs)
    groups = r.json()['response']['items']
    return groups


# Получаем информацию о заданном пользователе
def get_info_user(params=None, **kwargs):
    r = requests.get('https://api.vk.com/method/users.get', params=params, **kwargs)
    user = r.json()['response'][0]
    return user


# Получаем информацию о заданном сообществе
def get_info_group(params=None, **kwargs):
    r = requests.get('https://api.vk.com/method/groups.getById', params=params, **kwargs)
    info = r.json()['response'][0]
    return info


# Получаем словарь где ключом является id группы, а значением список id друзей состоящих в ней
def collector(friends):
    length = len(friends)
    collection = defaultdict(list)
    logger.info('collecting started')
    for index, user in enumerate(friends, start=1):
        # ловим исключения в случае если страница была удалена или заблокирована
        try:
            groups = get_user_groups(
                {'user_id': user,
                 'v': _VERSION,
                 'access_token': _TOKEN
                 }
            )
            for group in groups:
                collection[group].append(user)
        except KeyError:
            pass
        # progressbar
        sys.stdout.write('\rCompleted %d of %d friends (%.2f%%)' % (index, length, index / length * 100))
        sys.stdout.flush()
        # тайм-аут между запросами (число запросов не должно превышать трех в секунду)
        sleep(1)
    sys.stdout.write('\rCompleted\n')
    logger.info('collecting completed')
    return collection


# Выбираем уникальные группы для пользователя или указанного количества друзей
def selector(user_group_list, collection, n=None):
    user_groups = set(user_group_list)
    friend_groups = set()
    if n is None:
        for group in collection:
            friend_groups.add(group)
        user_groups.difference_update(friend_groups)
        return user_groups
    else:
        for group, users in collection.items():
            if len(users) > n:
                friend_groups.add(group)
        user_groups.difference_update(friend_groups)
        return user_groups


# Формируем необходимые данные для выбраных id групп
def creator(groups):
    length = len(groups)
    data = list()
    logger.info('creating started')
    for index, group in enumerate(groups, start=1):
        # ловим исключения в случае если страница была удалена или заблокирована
        try:
            info = get_info_group(
                {'group_id': group,
                 'fields': 'members_count',
                 'v': _VERSION,
                 'access_token': _TOKEN,
                 }
            )
            # сохраняем порядок ключей в соответствии с указанным в примере
            temp = OrderedDict()
            temp['name'] = info['name']
            temp['gid'] = info['id']
            temp['members_count'] = info['members_count']
            data.append(temp)
        except KeyError:
            pass
        # progressbar
        sys.stdout.write('\rCompleted %d of %d groups (%.2f%%)' % (index, length, index / length * 100))
        sys.stdout.flush()
        # тайм-аут между запросами (число запросов не должно превышать трех в секунду)
        sleep(1)
    sys.stdout.write('\rCompleted\n')
    logger.info('creating completed')
    return data


# Записываем полученный список в json file.
def write_json(data, save_path):
    filename = 'groups.json'
    filename = os.path.join(save_path, filename)
    # ловим исключение если отсутствуют права на запись или нет файла/директории
    try:
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=2, ensure_ascii=False)
        logger.info(
            'recording completed: %(file)s',
            {'file': filename},
        )
    except (PermissionError, FileNotFoundError) as e:
        logger.error('recording error')
        sys.stdout.write('%s' % e)


# Получаем аргументы командной строки
def get_args():
    parser = argparse.ArgumentParser(
        prog=__title__,
        description=__description__
    )
    parser.add_argument(
        'user',
        type=str,
        help='username or user_id to search his unique groups',
        nargs='?'
    )
    parser.add_argument(
        '-n', '--numbers',
        type=int,
        default=None,
        help="allowable number of user's friends in group (positive integer, default n = 0)"
    )
    parser.add_argument(
        '-p', '--save-path',
        dest='path',
        default='.',
        help='path to directory where to save files'
    )
    parser.add_argument(
        '--debug', action='store_true',
        help='print debug log'
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='print a detailed log'
    )
    parser.add_argument(
        '-V', '--version', action='store_true',
        help='print version info and exit'
    )
    return parser.parse_args()


def main():
    args = get_args()

    if args.version:
        print('{} | {}'.format(__title__, __version__))
        raise SystemExit

    if args.debug:
        log_level = logging.DEBUG
    elif args.verbose:
        log_level = logging.INFO
    else:
        log_level = logging.WARNING

    logging.basicConfig(
        level=log_level,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%d-%m-%Y %H:%M:%S',
    )
    logging.debug('{} {}'.format(__title__, __version__))

    # Получаем id пользователя в случае если в аргументе передано короткое имя
    user = args.user
    user_info = get_info_user(
        {
            'user_ids': user,
            'v': _VERSION,
            'access_token': _TOKEN
        }
    )
    user_id = user_info['id']
    # Количество друзей, по умолчанию нет
    n = args.numbers
    # Путь к директории, в которой сохранятеся файл, по умолчанию текущая рабочия директория
    save_path = args.path

    params = {'v': _VERSION, 'access_token': _TOKEN, 'user_id': user_id}

    # Не вываливаемся при Ctrl+C :)
    try:
        friends_list = get_user_friends(params)
        user_groups_list = get_user_groups(params)
        collection = collector(friends_list)
        unique = selector(user_groups_list, collection, n)
        data = creator(unique)
        write_json(data, save_path)
    except KeyboardInterrupt:
        pass

    logging.debug('Done!')

if __name__ == '__main__':
    main()
