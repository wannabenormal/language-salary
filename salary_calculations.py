def predict_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return int((salary_from + salary_to) / 2)

    if salary_from:
        return int(salary_from * 1.2)

    if salary_to:
        return int(salary_to * 0.8)
