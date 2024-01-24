import psycopg2


class DBManager:
    """Класс для работы с данными, полученными из базы данных."""

    def __init__(self, database_name: str, params: dict):
        self.conn = psycopg2.connect(dbname=database_name, **params)
        self.conn.autocommit = True

    def __del__(self):
        self.conn.close()

    def get_companies_and_vacancies_count(self) -> list:
        """Получает список всех компаний и количество вакансий у каждой компании."""

        with self.conn.cursor() as cur:
            cur.execute("""
                    SELECT employers.name, COUNT(vacancies.vacancy_id) as count_vacancies FROM employers
                    JOIN vacancies USING(employer_id)
                    GROUP BY employers.name
                    ORDER BY count_vacancies
                """)
            data = cur.fetchall()

        return data

    def get_all_vacancies(self) -> list:
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию."""

        with self.conn.cursor() as cur:
            cur.execute("""
                    SELECT employers.name, vacancies.name, vacancies.salary_from, vacancies.salary_to, vacancies.url FROM employers
                    JOIN vacancies USING(employer_id)
                    ORDER BY vacancies.salary_from, vacancies.salary_to
                """)
            data = cur.fetchall()

        return data

    def get_avg_salary(self) -> float:
        """Получает среднюю зарплату по вакансиям."""

        with self.conn.cursor() as cur:
            cur.execute("""
                    SELECT AVG(salary_from) as avg_salary from vacancies
                """)
            data = cur.fetchone()[0]

        return data

    def get_vacancies_with_higher_salary(self) -> list:
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""

        with self.conn.cursor() as cur:
            cur.execute("""
                    SELECT employers.name, vacancies.name, vacancies.salary_from, vacancies.url FROM vacancies
                    JOIN employers USING(employer_id)
                    WHERE vacancies.salary_from > (SELECT AVG(salary_from) from vacancies)
                    ORDER BY vacancies.salary_from DESC
                """)
            data = cur.fetchall()

        return data

    def get_vacancies_with_keyword(self, word: str) -> list:
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова."""

        with self.conn.cursor() as cur:
            cur.execute(f"""
                    SELECT employers.name, vacancies.name, vacancies.salary_from, vacancies.url FROM vacancies
                    JOIN employers USING(employer_id)
                    WHERE vacancies.name LIKE '%{word}%'
                    ORDER BY vacancies.salary_from
                """)
            data = cur.fetchall()

        return data
