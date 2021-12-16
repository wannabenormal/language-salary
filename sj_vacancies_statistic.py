import itertools
from statistics import mean
import requests
from salary_calculations import predict_salary


def fetch_sj_vacancies_by_lang(
        sj_key, language, town=4,
        period=30, catalogue=48):

    fetched_vacancies = []
    vacancies_total = 0

    for page_num in itertools.count():
        headers = {
            "X-Api-App-Id": sj_key
        }

        params = {
            "page": page_num,
            "count": 100,
            "town": town,
            "period": period,
            "catalogues": catalogue,
            "keywords[0][srws]": 1,
            "keywords[0][keys]": language,
        }

        response = requests.get(
            "https://api.superjob.ru/2.0/vacancies/",
            headers=headers,
            params=params
        )
        response.raise_for_status()

        vacancies_page = response.json()
        fetched_vacancies.extend(vacancies_page["objects"])
        vacancies_total = vacancies_page["total"]

        if not vacancies_page["more"]:
            break

    return fetched_vacancies, vacancies_total


def predict_rub_salary_sj(vacancy):
    if vacancy["currency"] != "rub":
        return None

    salary_from = vacancy["payment_from"]
    salary_to = vacancy["payment_to"]

    return predict_salary(salary_from, salary_to)


def get_languages_salary_statistic_sj(sj_key, languages):
    languages_salary_statistic = {}

    for lang in languages:
        vacancies, vacancies_total = fetch_sj_vacancies_by_lang(sj_key, lang)

        predicted_salaries = [
            predict_rub_salary_sj(vacancy)
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
