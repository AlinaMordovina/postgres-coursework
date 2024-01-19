import psycopg2


class DBManager:
    """Класс для работы с данными, полученными из базы данных."""

    def __init__(self, database_name: str, params: dict):
        self.db_name = database_name
        self.params = params

    def get_companies_and_vacancies_count(self) -> list:
        """Получает список всех компаний и количество вакансий у каждой компании."""
        pass

    def get_all_vacancies(self) -> list:
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию."""
        pass

    def get_avg_salary(self) -> int:
        """Получает среднюю зарплату по вакансиям."""
        pass

    def get_vacancies_with_higher_salary(self) -> list:
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        pass

    def get_vacancies_with_keyword(self, words: list) -> list:
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова."""
        pass
