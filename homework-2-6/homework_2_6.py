import os


def template():
    currentdir = 'Source'
    destinationdir = 'Result'
    # проверяем существование папки, если нет создаем
    if not os.path.exists(destinationdir):
        os.mkdir(destinationdir)
    # читаем каталог 'Source', конвертируем файлы и складываем их в 'Result'
    for file in os.listdir(currentdir):
        path1 = os.path.join(currentdir, file)
        path2 = os.path.join(destinationdir, file)
        template = 'convert ' + path1 + ' -resize 200 ' + path2
        os.popen(template)

template()
