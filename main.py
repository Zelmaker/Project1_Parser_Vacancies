from bs4 import BeautifulSoup
import json
import requests


def make_url(vacancy_name):
    hh_url = "https://hh.ru/search/vacancy?text=" + vacancy_name + "&from=suggest_post & area = 1&hhtmFrom = vacancy_search_list&page="
    superjob_url = "https://russia.superjob.ru/vacancy/search/?keywords=" + vacancy_name + "& page ="
    return hh_url, superjob_url


# print("Привет! Давай соберем вакансии по ключевому слову с HH.ru и c superjob.ru\nВведите ключ(например: python)")
# user_keyword_input = input()
# hh_url, superjob_url = make_url(user_keyword_input)
# print("Сколько вакансий собираем с hh? ")
# vacancies_from_hh = int(input())
# print("Сколько вакансий собираем с SJ? не меньше 40")
# vacancies_from_sj = int(input())
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

            # if len(vacancy_name) == 0:
            #     print("Больше вакансий на хх нет")
            #     break


getting_vacancies_hh("python", 100)
