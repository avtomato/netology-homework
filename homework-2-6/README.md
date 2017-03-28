# README #
Задание к занятию «Вызов других программ»

Домашнее задание к лекции 2.4 «Вызов внешних программ»

Задача №1

Установить [Pycharm Community Edition](https://www.jetbrains.com/pycharm/download/#section=windows)

Задача №2

Нужные для домашней работы файлы находятся на [GitHub.](https://github.com/netology-code/Python_course/tree/master/PY1_Lesson_2.5/homework)

Есть программа ([Image Magick](http://www.imagemagick.org/script/index.php) для Windows и Linux, либо встроенная утилиту sips для mac), которая сжимает фотографии, и есть папка «Source» с самими фотографиями. Каждую фотографию мы хотим уменьшить до 200px в ширину (высота меняется пропорционально). Нужно для каждой фотографии запустить программу и результат работы положить в папку «Result».

Пример (ImageMagic):

convert input.jpg -resize 200 output.jpg
Пример (sips):

sips --resampleWidth 200 input.jpg
Внимание! sips меняет исходную фотографию. Используйте команду cp для того чтобы переместить фотографию из папки в папку

Задача №3. Дополнительная (не обязательная)

Реализовать 4 параллельных процесса и разделить фотографии между ними.