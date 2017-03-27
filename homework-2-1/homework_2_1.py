import re


def get_dish():
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


def get_shop_list_by_dishes(dishes, person_count):
    shop_list = {}
    cook_book = get_dish()
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
    person_count = int(input('Введите количество человек: '))
    dishes = input('Введите блюда в расчете на одного человека (через запятую): ').lower().split(', ')
    shop_list = get_shop_list_by_dishes(dishes, person_count)
    print_shop_list(shop_list)

create_shop_list()
