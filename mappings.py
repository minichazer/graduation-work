mappings = {
    'Полное имя': ['full_name', 'name', 'FIO'],
    'Пол': ['gender', 'sex', 'm_or_f'],
    'Дата рождения': ['birth_date', 'date_of_birth', 'dob', 'birthdate', 'bdate'],
    'Паспорт': ['passport_number', 'passport_id', 'passport_series_and_number', 'passport', 'pass', 'pass_id', 'pass_num', 'pass_number'],
    'Место и адрес жительства': ['address', 'residence_address', 'living_address', 'living_place'],
    'Номер телефона': ['phone_number', 'phone', 'mobile_phone', 'pnumber', 'p_number', 'phone_n', 'number'],
    'Сведения о доходах': ['income_info', 'salary_info', 'earnings_info', 'income', 'salary', 'earnings'],
    'ИНН': ['inn', 'EIN', 'ein', 'INN', 'tin', 'TIN'],
    'СНИЛС': ['snils', 'SNILS', 'inila', 'INILA', 'IIAN', 'iian'],
    'Отношение к воинской обязанности': ['military_service_info', 'military_status', 'mil_status', 'military_s', 'military_service_status'],
    'Сведения о трудовом стаже, предыдущих местах работы': ['work_experience', 'previous_jobs', 'employment_history', 'job_experience', 'work_years', 'job_years', 'employment_years'],
    'Семейное положение': ['marital_status', 'family_status', 'marital', 'marriage', 'fam_status'],
    'Данные об образовании, квалификации': ['education_info', 'qualification_info', 'degree_info', 'education', 'qualification', 'degree']
}
mappings_label = {
    'Полное имя': 1,
    'Пол': 2,
    'Дата рождения': 3,
    'Паспорт': 4,
    'Место и адрес жительства': 5,
    'Номер телефона': 6,
    'Сведения о доходах': 7,
    'ИНН': 8,
    'СНИЛС': 9,
    'Отношение к воинской обязанности': 10,
    'Сведения о трудовом стаже, предыдущих местах работы': 11,
    'Семейное положение': 12,
    'Данные об образовании, квалификации': 13,
    'Не является ПДн': 14
}
mappings_types = {
    'Полное имя': ['char', 'varchar', 'text'],
    'Пол': ['char', 'varchar', 'text'],
    'Дата рождения': ['char', 'varchar', 'text', 'date', 'time', 'datetime', 'timestamp'],
    'Паспорт': ['char', 'varchar', 'text'],
    'Место и адрес жительства': ['char', 'varchar', 'text'],
    'Номер телефона': ['char', 'varchar', 'text'],
    'Сведения о доходах': ['char', 'varchar', 'text', 'integer', 'numeric', 'decimal'],
    'ИНН': ['char', 'varchar', 'text', 'integer', 'numeric', 'decimal'],
    'СНИЛС': ['char', 'varchar', 'text'],
    'Отношение к воинской обязанности': ['char', 'varchar', 'text'],
    'Сведения о трудовом стаже, предыдущих местах работы': ['char', 'varchar', 'text'],
    'Семейное положение': ['char', 'varchar', 'text'],
    'Данные об образовании, квалификации': ['char', 'varchar', 'text'],
    'Не является ПДн': ['char', 'varchar', 'text']
}