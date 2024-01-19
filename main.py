from utils import get_hh_data, create_database, save_data_to_database
from db_manager import DBManager
from config import config


def main():
    database_name = 'hh_data'
    params = config()
    employers_ids = [
        '1740', # Яндекс
        '1122462', # Skyeng
        '1541784', # STM
        '1375441', # Okko
        '3529', # Сбер
        '78638', # Тинек
        '2059150', # Айти-услуги
        '1755416', # Appbooster
        '36486', # Magenta
        '668019' # СимбирСофт
    ]
    words = []

    data = get_hh_data(employers_ids)
    create_database(database_name, params)
    save_data_to_database(data, database_name, params)

    data_manager = DBManager(database_name, params)
    data_manager.get_companies_and_vacancies_count()
    data_manager.get_all_vacancies()
    data_manager.get_avg_salary()
    data_manager.get_vacancies_with_higher_salary()
    data_manager.get_vacancies_with_keyword(words)


if __name__ == '__main__':
    main()
