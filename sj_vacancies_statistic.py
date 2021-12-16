import requests
from statistics import mean
from utils import predict_salary


def fetch_sj_vacancies_by_lang(sj_key, language, town=4,
                               period=30, catalogue=48):
    fetched_vacancies = []

    page = 0
    more_pages = True

    while more_pages:
        headers = {
            "X-Api-App-Id": sj_key
        }

        params = {
            "page": page,
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

        page += 1
        more_pages = vacancies_page["more"]

    return fetched_vacancies


def predict_rub_salary_sj(vacancy):
    if not vacancy["currency"] == "rub":
        return None

    salary_from = vacancy["payment_from"]
    salary_to = vacancy["payment_to"]

    return predict_salary(salary_from, salary_to)


def get_languages_salary_statistic_sj(sj_key, languages):
    languages_salary_statistic = {}

    for lang in languages:
        vacancies = fetch_sj_vacancies_by_lang(sj_key, lang)
        predicted_salaries = [
            predict_rub_salary_sj(vacancy)
            for vacancy in vacancies
        ]
        cleaned_predicted_salaries = [
            int(salary)
            for salary in predicted_salaries
            if salary is not None
        ]

        vacancies_processed_count = len(cleaned_predicted_salaries)
        average_salary = (int(mean(cleaned_predicted_salaries))
                          if vacancies_processed_count
                          else None)

        languages_salary_statistic[lang] = {
            "vacancies_found": len(vacancies),
            "vacancies_processed": vacancies_processed_count,
            "average_salary": average_salary
        }

    return languages_salary_statistic
