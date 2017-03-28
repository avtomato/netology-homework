import os

currdir = 'Migrations'


def files_in_dir(currdir):
    """Получаем список файлов с расширением sql из указаной папки"""
    matches = []
    for file in os.listdir(currdir):
        if file.endswith('sql'):
            path = os.path.join(currdir, file)
            matches.append(path)
    return matches


def query_files(query, filelist):
    """Получаем список файлов, содержащих строки с вхождением запроса, и выводим имена найденных файлов построчно"""
    temp = []
    i = 0
    for file in filelist:
        with open(file, 'r') as file_object:
            if query in file_object.read():
                print(file)
                i += 1
                temp.append(file)
    print('Всего: {}'.format(i))
    return temp


def lister():
    """Поиск происходит только среди отобранных на предыдущем этапе файлов."""
    temp = files_in_dir(currdir)
    while True:
        command = input('Введите строку: ')
        temp = query_files(command, temp)
        if len(temp) is 1:
            break
        if len(temp) is 0:
            print('Совпадений не найдено')
            break
lister()
