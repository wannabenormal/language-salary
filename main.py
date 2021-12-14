import os
from statistics import mean
import requests
from dotenv import load_dotenv
from terminaltables import AsciiTable


def fetch_hh_vacancies_by_lang(language, search_area=1, period=30):
    page = 0
    pages_count = 1

    vacancies = []

    while page < pages_count:
        params = {
            "text": f"Программист {language}",
            "area": search_area,
            "period": period,
            "page": page,
        }

        response = requests.get("https://api.hh.ru/vacancies/", params=params)
        response.raise_for_status()

        page_data = response.json()

        pages_count = page_data["pages"]
        page += 1

        vacancies.extend(page_data["items"])

    return vacancies


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


def predict_salary(salary_from, salary_to):
    predicted_salary = None

    if salary_from and salary_to:
        predicted_salary = (salary_from + salary_to) / 2

    if salary_from:
        predicted_salary = salary_from * 1.2

    if salary_to:
        predicted_salary = salary_to * 0.8

    if predicted_salary:
        predicted_salary = int(predicted_salary)

    return predicted_salary


def predict_rub_salary_hh(vacancy):
    salary_info = vacancy["salary"]

    if not salary_info:
        return None

    if not salary_info["currency"] == "RUR":
        return None

    salary_from = salary_info["from"]
    salary_to = salary_info["to"]

    return predict_salary(salary_from, salary_to)


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


def get_languages_salary_statistic_hh(languages):
    languages_salary_statistic = {}

    for lang in languages:
        vacancies = fetch_hh_vacancies_by_lang(lang)
        predicted_salaries = [
            predict_rub_salary_hh(vacancy)
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


def render_vacancies_statistic_table(statistic, table_title):
    table_data = [
        [
            "Язык программирования",
            "Вакансий найдено",
            "Вакансий обработано",
            "Средняя зарплата"
        ]
    ]

    for lang_name, lang_stat in statistic.items():
        table_data.append(
            [
                lang_name,
                lang_stat["vacancies_found"],
                lang_stat["vacancies_processed"],
                lang_stat["average_salary"],
            ]
        )

    table = AsciiTable(table_data, title=table_title)
    print(table.table)


def main():
    load_dotenv()
    superjob_key = os.getenv("SUPERJOB_KEY")

    popular_languages = [
       "Swift",
       "Go",
       "C++",
       "PHP",
       "Python",
       "Java",
       "JavaScript",
    ]

    hh_statistic = get_languages_salary_statistic_hh(popular_languages)
    sj_statistic = get_languages_salary_statistic_sj(
        superjob_key,
        popular_languages
    )

    render_vacancies_statistic_table(hh_statistic, "HeadHunter Москва")
    print()
    render_vacancies_statistic_table(sj_statistic, "SuperJob Москва")


if __name__ == "__main__":
    main()
