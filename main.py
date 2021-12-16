import os
from dotenv import load_dotenv
from terminaltables import AsciiTable
from hh_vacancies_statistic import get_languages_salary_statistic_hh
from sj_vacancies_statistic import get_languages_salary_statistic_sj


def get_vacancies_statistic_table(statistic, table_title):
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

    return table.table


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

    print(get_vacancies_statistic_table(hh_statistic, "HeadHunter Москва"))
    print()
    print(get_vacancies_statistic_table(sj_statistic, "SuperJob Москва"))


if __name__ == "__main__":
    main()
