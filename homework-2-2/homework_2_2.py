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
    У файла newsit.json другая структура хранения данных, обрабатываем условие.
    """
    clear_data = []
    regexp = re.compile(r'<.*?>')
    news_list = data['rss']['channel']['item']
    for news in news_list:
        if isinstance(news['title'], str):
            clear_data += regexp.sub('', news['title'].strip()).split()
            clear_data += regexp.sub('', news['description'].strip()).split()
    else:
        clear_data += regexp.sub('', news['title']['__cdata'].strip()).split()
        clear_data += regexp.sub('', news['description']['__cdata'].strip()).split()
    return clear_data


def get_words(cleardata):
    """
    Отбираем из полученных данных слова длиной более 6 символов и считаем количество их вхождений в тексте.
    Возвращаем отсортированный по значениям словарь.
    """
    top_list = []
    big_data = [x.strip() for x in cleardata if len(x) > 6]
    word_list = Counter(big_data)
    for i in sorted(word_list.items(), key=lambda x: x[1], reverse=True):
        top_list.append(i)
    return top_list


def top_word(top_list):
    """
    Выводим пронумерованный Топ-10 самых часто встречающихся в новостях слов.
    """
    print('\n***Топ-10 самых часто встречающихся в новостях слов***')
    for i, occurrence in enumerate(top_list[:10]):
        print("{0}. {1} ({2})".format(i+1, occurrence[0], occurrence[1]))


def print_top():
    top_word(get_words(get_clear_data(get_data('newsafr.json', 'utf-8'))))
    top_word(get_words(get_clear_data(get_data('newscy.json', 'koi8-r'))))
    top_word(get_words(get_clear_data(get_data('newsfr.json', 'iso-8859-5'))))
    top_word(get_words(get_clear_data(get_data('newsit.json', 'cp1251'))))

print_top()
