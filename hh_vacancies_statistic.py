import itertools
from statistics import mean
import requests
from salary_calculations import predict_salary


def fetch_hh_vacancies_by_lang(language, search_area=1, period=30):
    fetched_vacancies = []
    vacancies_total = 0

    for page_num in itertools.count():
        params = {
            "text": f"Программист {language}",
            "area": search_area,
            "period": period,
            "page": page_num,
        }

        response = requests.get("https://api.hh.ru/vacancies/", params=params)
        response.raise_for_status()

        vacancies_page = response.json()
        fetched_vacancies.extend(vacancies_page["items"])
        vacancies_total = vacancies_page["found"]

        if page_num == vacancies_page["pages"] - 1:
            break

    return fetched_vacancies, vacancies_total


def predict_rub_salary_hh(vacancy):
    salary = vacancy["salary"]

    if not salary or salary["currency"] != "RUR":
        return None

    salary_from = salary["from"]
    salary_to = salary["to"]

    return predict_salary(salary_from, salary_to)


def get_languages_salary_statistic_hh(languages):
    languages_salary_statistic = {}

    for lang in languages:
        vacancies, vacancies_total = fetch_hh_vacancies_by_lang(lang)
        predicted_salaries = [
            predict_rub_salary_hh(vacancy)
            for vacancy in vacancies
        ]
        cleaned_predicted_salaries = [
            salary
            for salary in predicted_salaries
            if salary
        ]

        vacancies_processed_count = len(cleaned_predicted_salaries)
        average_salary = (
            int(mean(cleaned_predicted_salaries))
            if vacancies_processed_count else None
        )

        languages_salary_statistic[lang] = {
            "vacancies_found": vacancies_total,
            "vacancies_processed": vacancies_processed_count,
            "average_salary": average_salary
        }

    return languages_salary_statistic
