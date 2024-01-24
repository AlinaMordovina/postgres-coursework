from utils import get_hh_data, create_database, save_data_to_database
from db_manager import DBManager
from config import config


def main():
    """Функция для взаимодействия с пользователем."""

    database_name = 'hh_data'
    params = config()
    employers_ids = [
        '1740',
        '1122462',
        '1541784',
        '1375441',
        '3529',
        '78638',
        '2059150',
        '1755416',
        '36486',
        '668019'
    ]

    data = get_hh_data(employers_ids)
    create_database(database_name, params)
    save_data_to_database(data, database_name, params)
    data_manager = DBManager(database_name, params)

    print("Добрый день!")

    while True:
        operation_number = input("Выберите номер операции для просмотра информации:\n"
                                 "- Список всех компаний и количество вакансий у каждой компании: 1\n"
                                 "- Список всех вакансий: 2\n"
                                 "- Средняя зарплата по вакансиям: 3\n"
                                 "- Список всех вакансий, у которых зарплата выше средней по всем вакансиям: 4\n"
                                 "- Список всех вакансий, в названии которых содержится переданное слово: 5\n"
                                 "Для остановки просмотра информации введите слово - стоп\n"
                                 )
        if operation_number in ['1', '2', '3', '4', '5', 'стоп']:

            if operation_number == '1':
                companies = data_manager.get_companies_and_vacancies_count()
                for company in companies:
                    print(f"{company[0]} - {company[1]}")
            elif operation_number == '2':
                vacancies = data_manager.get_all_vacancies()
                for vacancy in vacancies:
                    if vacancy[2] is None and vacancy[3] is None:
                        print(f"{vacancy[0]}: {vacancy[1]}\n"
                              f"зарплата: не указана\n"
                              f"ссылка: {vacancy[4]}")
                    elif vacancy[2] is not None and vacancy[3] is None:
                        print(f"{vacancy[0]}: {vacancy[1]}\n"
                              f"зарплата: от {vacancy[2]}\n"
                              f"ссылка: {vacancy[4]}")
                    elif vacancy[2] is None and vacancy[3] is not None:
                        print(f"{vacancy[0]}: {vacancy[1]}\n"
                              f"зарплата: до {vacancy[3]}\n"
                              f"ссылка: {vacancy[4]}")
                    else:
                        print(f"{vacancy[0]}: {vacancy[1]}\n"
                              f"зарплата: от {vacancy[2]} до {vacancy[3]}\n"
                              f"ссылка: {vacancy[4]}")
            elif operation_number == '3':
                avg_salary = data_manager.get_avg_salary()
                print(round(avg_salary))
            elif operation_number == '4':
                big_salary_vacancies = data_manager.get_vacancies_with_higher_salary()
                for vacancy in big_salary_vacancies:
                    print(f"{vacancy[0]}: {vacancy[1]}\n"
                          f"зарплата: от {vacancy[2]}\n"
                          f"ссылка: {vacancy[3]}")
            elif operation_number == '5':
                word = input("Введите слово для поиска:\n")
                vacancies_with_keyword = data_manager.get_vacancies_with_keyword(word)
                for vacancy in vacancies_with_keyword:
                    if vacancy[2] is not None:
                        print(f"{vacancy[0]}: {vacancy[1]}\n"
                              f"зарплата: от {vacancy[2]}\n"
                              f"ссылка: {vacancy[3]}")
                    else:
                        print(f"{vacancy[0]}: {vacancy[1]}\n"
                              f"зарплата: не указана\n"
                              f"ссылка: {vacancy[3]}")

            elif operation_number.lower() == 'стоп':
                del data_manager
                print("Хорошего дня!")
                break

        else:
            print("Операции с указанным номером не существует.")


if __name__ == '__main__':
    main()
