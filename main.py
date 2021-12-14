import os
from dotenv import load_dotenv
from hh_vacancies_statistic import get_languages_salary_statistic_hh
from sj_vacancies_statistic import get_languages_salary_statistic_sj
from utils import render_vacancies_statistic_table


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
