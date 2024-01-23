import requests
import psycopg2

from typing import Any


def get_hh_data(employers_ids: list[str]) -> list[dict[str, Any]]:
    """Получение данных о работодателях и вакансиях с помощью API HH."""

    data = []
    vacancies_list = []
    url = "https://api.hh.ru/"

    for employer_id in employers_ids:
        data_employer = requests.get(f'{url}employers/{employer_id}').json()
        data_vacancies = requests.get(f'{url}vacancies', params={'employer_id': employer_id}).json()

        for vacancy in data_vacancies['items']:
            if vacancy['salary'] is None:
                vacancies_list.append({
                    'id': vacancy['id'],
                    'name': vacancy['name'],
                    'city': vacancy['area']['name'],
                    'description': vacancy['snippet']['responsibility'],
                    'salary_from': None,
                    'salary_to': None,
                    'currency': None,
                    'url': vacancy['alternate_url']
                })
            elif vacancy['salary']['from'] is None and vacancy['salary']['to'] is not None:
                vacancies_list.append({
                    'id': vacancy['id'],
                    'name': vacancy['name'],
                    'city': vacancy['area']['name'],
                    'description': vacancy['snippet']['responsibility'],
                    'salary_from': None,
                    'salary_to': int(vacancy['salary']['to']),
                    'currency': vacancy['salary']['currency'],
                    'url': vacancy['alternate_url']
                })
            elif vacancy['salary']['to'] is None and vacancy['salary']['from'] is not None:
                vacancies_list.append({
                    'id': vacancy['id'],
                    'name': vacancy['name'],
                    'city': vacancy['area']['name'],
                    'description': vacancy['snippet']['responsibility'],
                    'salary_from': int(vacancy['salary']['from']),
                    'salary_to': None,
                    'currency': vacancy['salary']['currency'],
                    'url': vacancy['alternate_url']
                })
            elif vacancy['salary']['to'] is None and vacancy['salary']['from'] is None:
                vacancies_list.append({
                    'id': vacancy['id'],
                    'name': vacancy['name'],
                    'city': vacancy['area']['name'],
                    'description': vacancy['snippet']['responsibility'],
                    'salary_from': None,
                    'salary_to': None,
                    'currency': vacancy['salary']['currency'],
                    'url': vacancy['alternate_url']
                })
            else:
                vacancies_list.append({
                    'id': vacancy['id'],
                    'name': vacancy['name'],
                    'city': vacancy['area']['name'],
                    'description': vacancy['snippet']['responsibility'],
                    'salary_from': int(vacancy['salary']['from']),
                    'salary_to': int(vacancy['salary']['to']),
                    'currency': vacancy['salary']['currency'],
                    'url': vacancy['alternate_url']
                })

        data.append({
            "employer": {
                'id': data_employer['id'],
                'name': data_employer['name'],
                'city': data_employer['area']['name'],
                'description': data_employer['description'],
                'url': data_employer['alternate_url']
            },
            "vacancies": vacancies_list
        })

    return data


def create_database(database_name: str, params: dict):
    """Создание базы данных и таблиц для сохранения данных о каналах и видео."""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    try:
        cur.execute(f"CREATE DATABASE {database_name}")
    except psycopg2.errors.DuplicateDatabase:
        cur.execute(f"DROP DATABASE {database_name}")
        cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE employers (
                    employer_id SERIAL PRIMARY KEY,
                    external_id VARCHAR NOT NULL,
                    name VARCHAR,
                    city VARCHAR(255),
                    description TEXT,
                    url TEXT
                )
            """)

    with conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE vacancies (
                    vacancy_id SERIAL PRIMARY KEY,
                    employer_id INT REFERENCES employers(employer_id),
                    external_id VARCHAR NOT NULL,
                    name VARCHAR,
                    city VARCHAR(355),
                    description TEXT,
                    salary_from INT,
                    salary_to INT,
                    currency VARCHAR(25),
                    url TEXT
                )
            """)

    conn.commit()
    conn.close()


def save_data_to_database(data: list[dict[str, Any]], database_name: str, params: dict):
    """Сохранение данных о каналах и видео в базу данных."""

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for item in data:
            employer_data = item['employer']
            cur.execute(
                """
                INSERT INTO employers (external_id, name, city, description, url)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING employer_id
                """,
                (employer_data['id'], employer_data['name'], employer_data['city'], employer_data['description'],
                 employer_data['url'])
            )
            employer_id = cur.fetchone()[0]
            vacancies_data = item['vacancies']
            for vacancy in vacancies_data:
                cur.execute(
                    """
                    INSERT INTO vacancies (employer_id, external_id, name, city, description, salary_from, salary_to,
                    currency, url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (employer_id, vacancy['id'], vacancy['name'], vacancy['city'], vacancy['description'],
                     vacancy['salary_from'], vacancy['salary_to'], vacancy['currency'], vacancy['url'])
                )

    conn.commit()
    conn.close()
