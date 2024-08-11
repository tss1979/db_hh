import psycopg2
from config import config
from utils import get_vacancy


class PostgresDB:
    def __init__(self):
        self.params = config()
        self.conn = psycopg2.connect(dbname='hh', **self.params)
        self.cur = self.conn.cursor()

    def create_table(self, table_name: str) -> None:
        '''Функция создает таблицы работодателей или вакансий'''
        with self.conn:
            if table_name == 'employers':
                self.cur.execute(f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                hh_id VARCHAR(255) NOT NULL,
                vac_url VARCHAR(255) NOT NULL,
                site_url VARCHAR(255),
                city VARCHAR(255));""")
            elif table_name == 'vacancies':
                self.cur.execute(f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                id SERIAL PRIMARY KEY,
                employer_id INT REFERENCES employers(id),
                name VARCHAR(255) NOT NULL,
                salary INT,
                url VARCHAR(255),
                requirements TEXT);""")
            else:
                raise ValueError('Wrong table name')

    def insert_data_emp(self, employer) -> int:
        '''Функция заполняет таблицe баpы данных employers полученными данными
        и возвращает id записи в базе'''
        with self.conn:
            self.cur.execute('''INSERT INTO public.employers (name, hh_id, vac_url, site_url, city) 
                                    VALUES (%s, %s, %s, %s, %s) RETURNING id''', \
                             (employer.get('name', ''), employer.get('id', ''), \
                              employer.get('vacancies_url', ''), employer.get('site_url', ''), \
                              employer.get('area', {}).get('name', '')))
            return self.cur.fetchone()[0]

    def insert_data_vac(self, id_,  vacancies: list) -> None:
        '''Функция заполняет таблицы баы данных полученными данными'''
        with self.conn:
            for vacancy in vacancies:
                try:
                    vac = get_vacancy(vacancy)
                    self.cur.execute("""INSERT INTO public.vacancies (employer_id, name, salary, url, requirements)
                    VALUES (%s, %s, %s, %s, %s)""", (id_, vac['name'], vac['salary'], vac['url'], vac['requirements']))
                except:
                    raise ValueError('Неверный формат')