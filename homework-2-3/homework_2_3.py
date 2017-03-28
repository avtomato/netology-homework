import re
import json


def get_dish_txt():
    with open('dish.txt', 'r', encoding='utf-8') as fr:
        regexp1 = re.compile(r'\D+$')
        regexp2 = re.compile(r'\|')
        cook_book = {}
        for line in fr:
            line = line.lower().strip()
            if re.match(regexp1, line):
                k = line
                cook_book[k] = []
            elif re.search(regexp2, line):
                ingridient_name, quanity, measure = line.split(' | ')
                cook_book[k] += [
                    {'ingridient_name': str(ingridient_name),
                     'quanity': int(quanity),
                     'measure': str(measure)}]
    return cook_book


def create_json():
    data = get_dish_txt()
    with open('dish.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)


def get_dish_json():
    with open('dish.json', 'r', encoding='utf-8') as json_file:
        cook_book = json.load(json_file)
    return cook_book


def get_shop_list_by_dishes(dishes, person_count, file):
    if 'txt' in file:
        cook_book = get_dish_txt()
    if 'json' in file:
        cook_book = get_dish_json()
    shop_list = {}
    for dish in dishes:
        for ingridient in cook_book[dish]:
            new_shop_list_item = dict(ingridient)
            new_shop_list_item['quanity'] *= person_count
            if new_shop_list_item['ingridient_name'] not in shop_list:
                shop_list[new_shop_list_item['ingridient_name']] = new_shop_list_item
            else:
                shop_list[new_shop_list_item['ingridient_name']]['quanity'] += new_shop_list_item['quanity']
    return shop_list


def print_shop_list(shop_list):
    for shop_list_item in shop_list.values():
        print('{ingridient_name} {quanity} {measure}'.format(**shop_list_item))


def create_shop_list():
    file = input('Введите формат хранения данных (txt, json): ')
    person_count = int(input('Введите количество человек: '))
    dishes = input('Введите блюда в расчете на одного человека (через запятую): ').lower().split(', ')
    shop_list = get_shop_list_by_dishes(dishes, person_count, file)
    print_shop_list(shop_list)

create_shop_list()
