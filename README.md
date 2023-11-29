# Тестовое задание. Бот формирует БД из полученных данных от пользователя.
#### Работа бота заключается в получении файла с расширением xlsx от пользователя и последующей загрузки его в БД sqlite3 по одноимённым столбцам.
##### БД имеет следующие поля:
- title
- url
- xpath

##### При запуске, бот приветствует пользователя по имени и предлагает начать с ним работу с нажатия на кнопку "download". Только после этого будет возможность произвести загрузку файла. Так же бот проверяет расширение файла, если оно не соответствует требуемому, то попросит проверить загрузить файл с нужным расширением. После загрузки первого файла, загрузить второй можно только после повторного нажатия на кнопку "download".


### Стек технологии:
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/) [![SQLite](https://img.shields.io/badge/-SQLite-464646?style=flat-square&logo=SQLite)](https://www.sqlite.org/) [![OpenPyXL](https://img.shields.io/badge/-OpenPyXL-464646?style=flat-square&logo=OpenPyXL)](https://openpyxl.readthedocs.io/) [![pandas](https://img.shields.io/badge/-pandas-464646?style=flat-square&logo=pandas)](https://pandas.pydata.org//)

## Установка
### Клонировать репозиторий: https://github.com/VRN-lab/test_bot_table.git

### Cоздать и активировать виртуальное окружение:
- python -m venv venv
- source venv/Scripts/activate
- python -m pip install --upgrade pip

### Установить зависимости из файла requirements.txt: 
- pip install -r requirements.txt

### Создать файл .env и записать токен своего бота, пример: 
- TOKEN = 56594756739:AA1223242353446iISIDP--nq96YKHGmnb706xQLmM

### Запустить основной код:
- main.py

### Автор:
#### Назипов Виктор