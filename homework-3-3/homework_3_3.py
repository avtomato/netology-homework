import os
import requests


KEY = ''  # Ваш API-ключ
URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'


# task1
def to_translate(sourcefile, resultfile, lang, to_lang='ru'):
    """Переводчик; принимает путь к файлу с текстом, путь к файлу с результатом,
        язык с которого перевести, язык на который перевести (по-умолчанию русский)."""
    source = os.path.abspath(sourcefile)
    # обрабатывем исключение в случае если файл отсутствует
    try:
        # читаем текст который нужно перевести
        with open(source, 'r') as file_object:
            text = file_object.read()
        # формируем запрос
        params = {
            'key': KEY,
            'lang': '{}-{}'.format(lang, to_lang),
            'text': text
        }
        r = requests.get(URL, params=params)
        # получаем список переведенных слов
        text = r.json()['text']
        # собираем полученный список в текст
        translate = ''.join(text)
        # записываем полученный текст и сохраняем в файл
        with open(resultfile, 'w', encoding='utf-8') as file_object:
            file_object.write(translate)
        print('Done')
    except FileNotFoundError:
        print('No such file or directory')

"""
# task2
filelist = ['DE.txt', 'ES.txt', 'FR.txt']
for i in filelist:
    to_translate(i, 'translate2_{}'.format(i), '{}'.format(i.split('.')[0].lower()))
"""
if __name__ == '__main__':
    import sys
    args = sys.argv[1:]
    to_translate(*args)
