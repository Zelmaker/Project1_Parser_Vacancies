from abc import abstractmethod, ABC

from bs4 import BeautifulSoup
import json
import requests


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
            print(f"Страница: - {p}")
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
                vacancy_description = f'{i["snippet"]["requirement"]} \n{i["snippet"]["responsibility"]}'.replace(
                    "<highlighttext>", "").replace("</highlighttext>", "")
                vacancy_one = str(Vacancy(vacancy_name, vacancy_url, vacancy_description, vacancy_salary))
                with open("vacancies.txt", 'a', encoding="utf-8") as f:
                    f.write(vacancy_one)
                print(f"Спарсено вакансий: {counter}")


class Superjob(Engine):
    def __init__(self, vacancy_name, amount_sj):
        self.vacancy_name = vacancy_name
        self.amount_sj = amount_sj

    def get_request(self):
        url = 'https://russia.superjob.ru/vacancy/search/'
        count = 0
        print("СОБИРАЕМ c SuperJob")
        for i in range(self.amount_sj // 40):
            print(f"Собираем с {i} страницы:")
            params = {'page': i, 'keywords': self.vacancy_name}
            response = requests.get(url, params=params)
            soup = BeautifulSoup(response.text, 'lxml')
            vacancies = soup.find_all('div', class_='_2lp1U _2J-3z _3B5DQ')
            for vacancy in vacancies:
                count += 1
                print(f"Собрали {count} вакансию ")
                self.vacancy_name = vacancy.find('span', class_='_9fIP1 _249GZ _1jb_5 QLdOc').text
                vacancy_url = "https://russia.superjob.ru" + vacancy.find('a', href=True)['href']
                vacancy_salary = vacancy.find('span', class_='_2eYAG _1nqY_ _249GZ _1jb_5 _1dIgi').text
                vacancy_description = vacancy.find('span', class_='_1Nj4W _249GZ _1jb_5 _1dIgi _3qTky').text
                vacancy_sj = str(Vacancy(self.vacancy_name, vacancy_url, vacancy_description, vacancy_salary))
                with open("vacancies.txt", 'a', encoding="utf-8") as f:
                    f.write(vacancy_sj)


class Vacancy:
    def __init__(self, name, url, description, salary=None):
        self.name = name
        self.url = url
        self.description = description
        self.salary = salary

    def __repr__(self):
        return f"Название вакансии {self.name} \nСсылка на вакансию: {self.url} \nОписание вакансии: \n{self.description}\nЗарплата:{self.salary}\n\n"


def main():
    print("Привет! Давай соберем вакансии по ключевому слову с HH.ru и c superjob.ru\nВведите ключ(например: python)")
    user_keyword_input = input()
    print("Сколько вакансий собираем с hh? ")
    vacancies_from_hh = int(input())
    print("Сколько вакансий собираем с SJ?")
    vacancies_from_sj = int(input())
    print("Пошла жара")
    hh = HH(user_keyword_input, vacancies_from_hh)
    hh.get_request()
    sj = Superjob(user_keyword_input, vacancies_from_sj)
    sj.get_request()


if __name__ == '__main__':
    main()
