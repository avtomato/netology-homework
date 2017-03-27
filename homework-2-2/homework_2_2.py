import json
import re
from collections import Counter


def get_data(name, code):
    """
    Читаем файл в ссответствующей кодировке.
    newsafr.json --- 'utf-8'
    newscy.json --- 'koi8-r'
    newsfr.json --- 'iso-8859-5'
    newsit.json --- 'cp1251'
    """
    with open(name, 'r', encoding=code) as file_json:
        data = json.load(file_json)
        return data


def get_clear_data(data):
    """
    Избавляемся от мусора в виде html тегов. Добавляем в список все слова, содержащиеся в заголовке и описании новости.
    У файла newsit.json другой формат хранения данных, обрабатываем условие.
    """
    clear_data = []
    regexp = re.compile(r'<.*?>')
    if data['rss']['channel']['title'] == 'Новости Италия':
        for i in range(len(data['rss']['channel']['item'])):
            clear_data += regexp.sub('', data['rss']['channel']['item'][i]['title'].strip()).split()
        for i in range(len(data['rss']['channel']['item'])):
            clear_data += regexp.sub('', data['rss']['channel']['item'][i]['description'].strip()).split()
    else:
        for i in range(len(data['rss']['channel']['item'])):
            clear_data += regexp.sub('', data['rss']['channel']['item'][i]['title']['__cdata'].strip()).split()
        for i in range(len(data['rss']['channel']['item'])):
            clear_data += regexp.sub('', data['rss']['channel']['item'][i]['description']['__cdata'].strip()).split()
    return clear_data


def get_words(cleardata):
    """
    Отбираем из полученных данных слова длиной более 6 символов и считаем количество их вхождений в тексте.
    Возвращаем отсортированный по значениям словарь.
    """
    top_word = []
    big_data = [x.strip() for x in cleardata if len(x) > 6]
    word_list = Counter(big_data)
    for i in sorted(word_list.items(), key=lambda x: x[1])[::-1]:
        top_word.append(i)
    return top_word


def top_word(topword):
    """
    Выводим пронумерованный Топ-10 самых часто встречающихся в новостях слов.
    """
    print('\n***Топ-10 самых часто встречающихся в новостях слов***')
    for i, occurrence in enumerate(topword[:10]):
        print("{0}. {1} ({2})".format(i+1, occurrence[0], occurrence[1]))


top_word(get_words(get_clear_data(get_data('newsafr.json', 'utf-8'))))
