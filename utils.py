def get_vacancy(vacancy: dict) -> dict:
    '''Функция преобразует объект в объект для сохранения в базе данных'''
    name = vacancy.get('name', 'Нет названия вакансии')
    salary_info = vacancy.get('salary', {})
    requirements = vacancy.get('snippet', {}).get('requirement', '')
    url = vacancy.get('url', '')
    if salary_info is None or not salary_info:
        salary = 0
    else:
        salary = salary_info.get('from', 0)

    return {
        'name': name,
        'salary': salary,
        'url': url,
        'requirements': requirements
    }
