import psycopg2
from config import config
from typing import Any, List


class DBManager:
    def __init__(self, database_name: str):
        self.params = config()
        self.conn = psycopg2.connect(dbname=database_name, **self.params)
        self.cur = self.conn.cursor()

    def close(self) -> None:
        '''Функция закрывает соединение с базой данных'''
        self.cur.close()
        self.conn.close()

    def get_data(self, sql: str) -> List[Any]:
        '''Функция производит запрос согласно переданного параметра и возвращает данные'''
        self.cur.execute(sql)
        data = self.cur.fetchall()
        return data

    def get_companies_and_vacancies_count(self) -> List[Any]:
        '''Функция возвращает список компаний и количество вакансий этих конпаний'''
        return self.get_data('''SELECT e.name as company, COUNT(*) FROM public.vacancies AS v JOIN public.employers as e
                                ON v.employer_id = e.id GROUP BY e.name;''')

    def get_all_vacancies(self) -> List[Any]:
        '''Функция возвращает список вакансий, компаний, зарплаты, и ссылку на вакансию'''
        return self.get_data('''SELECT v.name, e.name, v.salary, v.url FROM public.vacancies AS v 
                                JOIN public.employers as e ON v.employer_id = e.id;''')

    def get_avg_salary(self) -> List[Any]:
        '''Функция возвращает среднюю зарплату'''
        return self.get_data('''SELECT AVG(salary) FROM public.vacancies;''')[0][0]

    def get_vacancies_with_higher_salary(self) -> List[Any]:
        '''Функция возвращает список вакансий с зарплатой выше средней'''
        return self.get_data('''SELECT * FROM public.vacancies WHERE salary > 
        (SELECT AVG(salary) FROM public.vacancies)''')

    def get_vacancies_with_keyword(self, keyword) -> List[Any]:
        '''Функция возвращает список вакансий содержащих в названии ключевое слово'''
        self.cur.execute(f"SELECT * FROM public.vacancies WHERE name LIKE '%{keyword}%'")
        data = self.cur.fetchall()
        return data