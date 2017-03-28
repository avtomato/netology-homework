import re
import json
from xml.etree import ElementTree


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
                ingridient, quanity, measure = line.split(' | ')
                cook_book[k] += [
                    {'ingridient': str(ingridient),
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


def create_xml():
    with open('dish.txt', 'r', encoding='utf-8') as fr:
        regexp1 = re.compile(r'\D+$')
        regexp2 = re.compile(r'\|')
        root = ElementTree.Element('dishes')
        for line in fr:
            line = line.lower().strip()
            if re.match(regexp1, line):
                dish = ElementTree.SubElement(root, 'dish')
                dish.text = line
            elif re.search(regexp2, line):
                ingridient, quanity, measure = line.split(' | ')
                params = {'ingridient': ingridient, 'quanity': int(quanity), 'measure': measure}
                content = ElementTree.SubElement(dish, 'content', attrib=params)
                content.text = ''
        tree = ElementTree.ElementTree(root)
        tree.write('dish.xml', encoding='utf-8')


def get_dish_xml():
    tree = ElementTree.parse('dish.xml')
    root = tree.getroot()
    cook_book = {}
    for dish in root.iter('dish'):
        cook_book[dish.text.strip()] = []
        for content in dish:
            content.attrib['quanity'] = int(content.attrib['quanity'])
            cook_book[dish.text.strip()].append(content.attrib)
    return cook_book


def get_shop_list_by_dishes(dishes, person_count, file):
    if 'txt' in file:
        cook_book = get_dish_txt()
    if 'xml' in file:
        cook_book = get_dish_xml()
    if 'json' in file:
        cook_book = get_dish_json()
    shop_list = {}
    for dish in dishes:
        for ingridient in cook_book[dish]:
            new_shop_list_item = dict(ingridient)
            new_shop_list_item['quanity'] *= person_count
            if new_shop_list_item['ingridient'] not in shop_list:
                shop_list[new_shop_list_item['ingridient']] = new_shop_list_item
            else:
                shop_list[new_shop_list_item['ingridient']]['quanity'] += new_shop_list_item['quanity']
    return shop_list


def print_shop_list(shop_list):
    for shop_list_item in shop_list.values():
        print('{ingridient} {quanity} {measure}'.format(**shop_list_item))


def create_shop_list():
    file = input('Введите формат хранения данных (txt, xml, json): ')
    person_count = int(input('Введите количество человек: '))
    dishes = input('Введите блюда в расчете на одного человека (через запятую): ').lower().split(', ')
    shop_list = get_shop_list_by_dishes(dishes, person_count, file)
    print_shop_list(shop_list)

create_shop_list()
