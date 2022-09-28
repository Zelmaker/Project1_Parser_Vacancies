from bs4 import BeautifulSoup
import json
import requests


class Vacancy:
    def __init__(self, name, url, description, salary=None):
        self.name = name
        self.url = url
        self.description = description
        self.salary = salary


    def __repr__(self):
        return f"Название вакансии {self.name} \nСсылка на вакансию: {self.url} \nОписание вакансии: \n{self.description}\nЗарплата:{self.salary}\n\n"


# hh - 50 na page
# sj 40
def getting_vacancies_hh(vacancy_name, amount):
    counter = 0
    for p in range(int(amount) // 10):
        print(f"Страница: - {p}")
        par = {'per_page': '10', 'page': p, 'text': vacancy_name, 'User-Agent': 'User-Agent: MyApp/1.0',
               'From': 'proz2022@mail.ru'}
        page = requests.get("https://api.hh.ru/vacancies", params=par)
        data = json.loads(page.text)
        if len(data) == 0:
            print("break")
            break
        for i in data["items"]:
            counter += 1
            vacancy_name = i["name"]
            vacancy_url = i["alternate_url"]
            if i.get("salary") is not None:
                vacancy_salary = f'{i["salary"]["from"]} - {i["salary"]["to"]}'
            else:
                vacancy_salary = 0
            vacancy_description = f'{i["snippet"]["requirement"]} \n{i["snippet"]["responsibility"]}'.replace("<highlighttext>","").replace("</highlighttext>","")
            vacancy_one = str(Vacancy(vacancy_name, vacancy_url, vacancy_description, vacancy_salary))
            with open("vacancies.txt", 'a', encoding="utf-8") as f:
                f.write(vacancy_one)
            print(f"Спарсено вакансий: {counter}")

def getting_vacancies_sj(vacancy_name, amount):
    url = 'https://russia.superjob.ru/vacancy/search/'
    count = 0
    for i in range(amount//40):
        print(f"Собираем с {i} страницы:")
        params = {'page': i, 'keywords': vacancy_name}
        response = requests.get(url, params=params)
        soup = BeautifulSoup(response.text, 'lxml')
        vacancies = soup.find_all('div', class_='_2lp1U _2J-3z _3B5DQ')
        for vacancy in vacancies:
            count += 1
            print(f"Собрали {count} вакансию ")
            vacancy_name = vacancy.find('span', class_='_9fIP1 _249GZ _1jb_5 QLdOc').text
            vacancy_url = "https://russia.superjob.ru" + vacancy.find('a', href=True)['href']
            vacancy_salary = vacancy.find('span', class_='_2eYAG _1nqY_ _249GZ _1jb_5 _1dIgi').text
            vacancy_description = vacancy.find('span', class_='_1Nj4W _249GZ _1jb_5 _1dIgi _3qTky').text
            vacancy_sj = str(Vacancy(vacancy_name, vacancy_url, vacancy_description, vacancy_salary))
            with open("vacancies.txt", 'a', encoding="utf-8") as f:
                f.write(vacancy_sj)

#
# getting_vacancies_hh("python", 100)
getting_vacancies_sj("python", 40)
