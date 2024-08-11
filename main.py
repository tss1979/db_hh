from hh import HeadHunterAPI
from postgress_db import PostgresDB
from db_manager import DBManager


def main():
    hh = HeadHunterAPI()
    employers = hh.get_employers()
    postgres_db = PostgresDB()
    postgres_db.create_table('employers')
    postgres_db.create_table('vacancies')
    for employer in employers:
        id_ = postgres_db.insert_data_emp(employer)
        postgres_db.insert_data_vac(id_, hh.get_vacancies(employer.get('vacancies_url', '')))

    db_manager = DBManager('hh')

    print(db_manager.get_vacancies_with_keyword('Грузчик'))


if __name__ == '__main__':
    main()