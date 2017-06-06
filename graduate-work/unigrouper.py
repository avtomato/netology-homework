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
__version__ = 'ver. 0.0.2'
__description__ = "Get a list of user's groups, that exclude user's friends"

# Версия API
_VERSION = '5.64'
# access_token
_TOKEN = 'd13e692be69592b09fd22c77a590dd34e186e6d696daa88d6d981e1b4e296b14acb377e82dcbc81dc0f22'


logger = logging.getLogger(__name__)

s = requests.Session()


class UserDeactivated(Exception):
    pass


def make_request(url=None, params=None, timeout=None, **kwargs):
    """With a specified time interval sends a GET request.

    :param url: URL for the new :class:`Request` object.
    :param params: (optional) Dictionary or bytes to be sent in the query string for the :class:`Request`.
    :param timeout: (optional) How long to wait for the server to send data
    :rtype: dict
    """
    sleep(0.4)
    r = s.get(url=url, params=params, timeout=timeout, **kwargs)
    if r.json().get('error'):
        raise UserDeactivated('{}'.format(r.json().get('error').get('error_msg')))
    else:
        return r.json()


def collector(friends):
    """ Get dictionary, where the key is the group id, and the value of the list of id users included in it

    :param friends: List user's friends
    :rtype: dict
    """
    length = len(friends)
    collection = defaultdict(list)
    logger.info('collecting started')
    url = 'https://api.vk.com/method/groups.get'
    for index, user in enumerate(friends, start=1):
        # ловим исключения в случае если страница пользователя была удалена или заблокирована
        try:
            response = make_request(
                url=url,
                timeout=13,
                params={
                    'user_id': user,
                    'v': _VERSION,
                    'access_token': _TOKEN
                }
            )
            groups = response['response']['items']
            for group in groups:
                collection[group].append(user)
        except UserDeactivated:
            pass
        # progressbar
        sys.stdout.write('\rCompleted %d of %d friends (%.2f%%)' % (index, length, index / length * 100))
        sys.stdout.flush()
    sys.stdout.write('\rCompleted\n')
    logger.info('collecting completed')
    return collection


def selector(user_group_list, collection, n=None):
    """Get a set of user's groups, that exclude user's friends

    :param user_group_list: List user's groups
    :param collection: Dictionary, where the key is the group id, and the value of the list of id users included in it
    :param n: Allowable number of user's friends in group (default 0)
    :rtype: set
    """
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


def creator(groups):
    """Get the necessary data for selected unique id groups

    :param groups: Set of unique user's groups
    :rtype: dict
    """
    length = len(groups)
    data = list()
    logger.info('creating started')
    url = 'https://api.vk.com/method/groups.getById'
    for index, group in enumerate(groups, start=1):
        response = make_request(
            url=url,
            timeout=13,
            params={
                'group_id': group,
                'fields': 'members_count',
                'v': _VERSION,
                'access_token': _TOKEN
            }
        )
        # Заблокированные страницы групп пропускаем, api не отдает их members_count
        if 'deactivated' in response['response'][0]:
            continue
        info = response['response'][0]
        # сохраняем порядок ключей в соответствии с указанным в примере
        temp = OrderedDict({
            'name': info['name'],
            'gid': info['id'],
            'members_count': info['members_count']
        })
        data.append(temp)
        # progressbar
        sys.stdout.write('\rCompleted %d of %d groups (%.2f%%)' % (index, length, index / length * 100))
        sys.stdout.flush()
    sys.stdout.write('\rCompleted\n')
    logger.info('creating completed')
    return data


def write_json(data, save_path):
    """Write the data to a json file

    :param data: Dictionary, with data from unique groups
    :param save_path: Path to directory where to save files (default current work directory)
    """
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


def get_args():
    """Get command-line arguments

    :rtype: <class 'argparse.Namespace'>
    """
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
        help='path to directory where to save files (default current work directory)'
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
        sys.exit()

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
    url = 'https://api.vk.com/method/users.get'
    response = make_request(
        url=url,
        params={
            'user_ids': user,
            'v': _VERSION,
            'access_token': _TOKEN
        }
    )
    user_info = response['response'][0]
    user_id = user_info['id']
    # Количество друзей, по умолчанию нет
    n = args.numbers
    # Путь к директории, в которой сохранятеся файл, по умолчанию текущая рабочия директория
    save_path = args.path

    params = {'v': _VERSION, 'access_token': _TOKEN, 'user_id': user_id}

    # Не вываливаемся при Ctrl+C :)
    try:
        friends_list = make_request(
            url='https://api.vk.com/method/friends.get',
            params=params
        )['response']['items']
        user_groups_list = make_request(
            url='https://api.vk.com/method/groups.get',
            params=params
        )['response']['items']
        collection = collector(friends_list)
        unique = selector(user_groups_list, collection, n)
        data = creator(unique)
        write_json(data, save_path)
    except KeyboardInterrupt:
        pass

    logging.debug('Done!')

if __name__ == '__main__':
    main()
