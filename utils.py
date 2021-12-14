from terminaltables import AsciiTable


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

