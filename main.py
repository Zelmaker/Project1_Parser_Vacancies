from abc import abstractmethod, ABC

from bs4 import BeautifulSoup
import json
import requests
from random import shuffle


class Engine(ABC):
    @abstractmethod
    def get_request(self):
        pass


class HH(Engine):
    def __init__(self, vacancy_name, amount_hh):
        self.vacancy_name = vacancy_name
        self.amount_hh = amount_hh

    def get_request(self):
        counter = 0
        print("СОБИРАЕМ c HH")
        for p in range(int(self.amount_hh) // 10):
            print(f"Страница HH: - {p}")
            par = {'per_page': '10', 'page': p, 'text': self.vacancy_name, 'User-Agent': 'User-Agent: MyApp/1.0',
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
                    vacancy_salary = i["salary"]["from"]
                else:
                    vacancy_salary = 0
                vacancy_description = f'{i["snippet"]["requirement"]}{i["snippet"]["responsibility"]}'.replace(
                    "<highlighttext>", "").replace("</highlighttext>", "")
                vacancy_one = str(Vacancy(vacancy_name, vacancy_url, vacancy_description, vacancy_salary))
                with open("vacancies.txt", 'a', encoding="utf-8") as f:
                    f.write(vacancy_one)
                print(f"Спарсено вакансий HH: {counter}")
        return counter


class Superjob(Engine):
    def __init__(self, vacancy_name, amount_sj):
        self.vacancy_name = vacancy_name
        self.amount_sj = amount_sj

    def get_request(self):
        url = 'https://russia.superjob.ru/vacancy/search/'
        count = 0
        print("СОБИРАЕМ c SuperJob")
        for i in range(self.amount_sj // 40):
            print(f"Собираем с {i} страницы SJ:")
            params = {'page': i, 'keywords': self.vacancy_name}
            response = requests.get(url, params=params)
            soup = BeautifulSoup(response.text, 'lxml')
            vacancies = soup.find_all('div', class_='_2lp1U _2J-3z _3B5DQ')
            for vacancy in vacancies:
                count += 1
                print(f"Собрали c SJ {count} вакансию ")
                self.vacancy_name = vacancy.find('span', class_='_9fIP1 _249GZ _1jb_5 QLdOc').text
                vacancy_url = "https://russia.superjob.ru" + vacancy.find('a', href=True)['href']
                vacancy_salary = vacancy.find('span', class_='_2eYAG _1nqY_ _249GZ _1jb_5 _1dIgi').text

                vacancy_description = vacancy.find('span', class_='_1Nj4W _249GZ _1jb_5 _1dIgi _3qTky').text
                vacancy_sj = str(Vacancy(self.vacancy_name, vacancy_url, vacancy_description, vacancy_salary))
                with open("vacancies.txt", 'a', encoding="utf-8") as f:
                    f.write(vacancy_sj)
        return count


class Vacancy:
    def __init__(self, name, url, description, salary=None):
        self.name = name
        self.url = url
        self.description = description
        self.salary = salary

    def __repr__(self):
        return f"Название вакансии {self.name}|Ссылка на вакансию: {self.url}|Описание вакансии:{self.description}|Зарплата:{self.salary}\n"


def vacancies_file_output():
    with open("vacancies.txt", 'r', encoding="utf-8") as f:
        file = f.readline()
    return file


def main():
    print("Привет!\nЭто парсер вакансий с сайтов HH и SJ!\nВыбери, что будем делать?\n1.Собираем с HH\n2.Собираем с SJ")
    user_input = input()
    if user_input == "1":
        print("Собираем HH")
        print("Введи ключ(например: python)")
        user_keyword_input = input()
        print("Сколько вакансий собираем с hh? ")
        vacancies_from_hh = int(input())
        hh = HH(user_keyword_input, vacancies_from_hh)
        number_of_hh_vacs = hh.get_request()
        print(f"Собрано {number_of_hh_vacs} вакансий")
    elif user_input == "2":
        print("Собираем SJ введите ключ(например: python)")
        user_keyword_input = input()
        print("Сколько вакансий собираем с SJ?")
        vacancies_from_sj = int(input())
        sj = Superjob(user_keyword_input, vacancies_from_sj)
        number_of_sj_vacs = sj.get_request()
        print(f"Собрано {number_of_sj_vacs} вакансий")
    else:
        print("Ошибочка попробуй ещё")
    # Доп. блок, что делаем с собранными данными
    while True:
        print(
            "Выбери, что будем делать?\n1. Вывести все вакансии\n2. Вывести рандом 10 по зп\n3. Собираем с HH\n4.Собираем с SJ\n5.Очистить файл")
        user_input = input()
        if user_input == "1":
            all_vacancies = vacancies_file_output()
            for vacancy in all_vacancies:
                print(vacancy)
        elif user_input == "2":
            all_vacancies = vacancies_file_output()
            shuffle(all_vacancies)
            for i in range(10):
                for vacancy in all_vacancies:
                    print(vacancy)
        elif user_input == "3":
            print("Собираем HH")
            print("Введи ключ(например: python)")
            user_keyword_input = input()
            print("Сколько вакансий собираем с hh? ")
            vacancies_from_hh = int(input())
            hh = HH(user_keyword_input, vacancies_from_hh)
            number_of_hh_vacs = hh.get_request()
            print(f"Собрано {number_of_hh_vacs} вакансий")

        elif user_input == "4":
            print("Собираем SJ введите ключ(например: python)")
            user_keyword_input = input()
            print("Сколько вакансий собираем с SJ?")
            vacancies_from_sj = int(input())
            sj = Superjob(user_keyword_input, vacancies_from_sj)
            number_of_sj_vacs = sj.get_request()
            print(f"Собрано {number_of_sj_vacs} вакансий")
        elif user_input == "5":
            open('vacancies.txt', 'w').close()
        else:
            print("Ошибочка попробуй ещё")


if __name__ == '__main__':
    main()
