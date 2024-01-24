coursework_5

Код для программы, которая получает информацию о вакансиях с платформы hh.ru, создает БД PostgreSQL и загружает полученные данные в созданные таблицы.
Так же в рамках программы можно получать следующие данные о вакансиях:
- Список всех компаний и количество вакансий у каждой компании;
- Список всех вакансий;
- Среднюю зарплату по вакансиям;
- Список всех вакансий, у которых зарплата выше средней по всем вакансиям;
- Список всех вакансий, в названии которых содержится переданное слово.

Технологии:
- python 3.11

Используемые библиотеки:

- requests 2.31.0
- psycopg2 2.9.9
- psycopg2-binary 2.9.9

Инструкция для развертывания проекта:
1. Клонировать проект

https://github.com/AlinaMordovina/postgres-coursework.git

2. Создать виртуальное окружение

Находясь в директории проекта запустить в терминале команды:

python -m venv venv

source venv/bin/activate

3. Установить зависимости

Все зависимости указаны в файле requirements.txt

Для установки всех зависимостей из файла необходимо запустить в терминале команду:

pip install -r requirements.txt

4. Создать файл конфигурации database.ini с указанием параметров:

[postgresql]
- host=
- user=
- password=
- port=

Пример файла приложен к проекту database_example.ini

5. Запустить main.py




Автор проекта: Мордовина Алина