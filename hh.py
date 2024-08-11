import requests


class HeadHunterAPI:
    url: str
    vacancies: list
    headers: dict
    params: dict

    def __init__(self):
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': '', 'page': 0, 'per_page': 100}
        self.vacancies = []
        self.employers = []

    def get_vacancies(self, vac_url) -> list:
        '''Функция делает запрос к hh api и возвращеет список вакансий'''
        while self.params.get('page') != 20:
            response = requests.get(vac_url, headers=self.headers, params=self.params)
            vacancies = response.json()['items']
            self.vacancies.extend(vacancies)
            self.params['page'] += 1
        return self.vacancies

    def get_employers(self) -> list:
        '''Функция делает запрос к hh api и возвращеет список раблтодателей из топ списка'''
        top_id = ['39305', '3529', '10309', '3776', '4181',\
                  '4233', '665467', '865081', '32918', '3009249']
        for id_ in top_id:
            url = 'https://api.hh.ru/employers/' + id_
            response = requests.get(url, headers=self.headers, params=self.params)
            # print(response.json()['name'])
            # print(response.json()['vacancies_url'])
            # print(response.json()['site_url'])
            # print(response.json()['area']['name'])
            # print(response.json()['id'])
            self.employers.append(response.json())
        return self.employers