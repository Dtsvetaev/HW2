import csv
import re


def split_name_patronymic(name):
    # Ищем паттерн, где строчная буква сменяется заглавной
    name_parts = re.findall(r'[А-ЯЁ][^А-ЯЁ]*', name)
    if len(name_parts) == 2:
        return name_parts
    return [name, '']


def correct_name(full_name):
    parts = re.split(r'\s+', full_name.strip())

    if len(parts) > 2:
        lastname, firstname, surname = parts[0], parts[1], ' '.join(parts[2:])
    elif len(parts) == 2:
        lastname, firstname = parts[0], parts[1]
        firstname, surname = split_name_patronymic(firstname)
    else:
        lastname, firstname, surname = parts[0], '', ''
    return [lastname, firstname, surname]


def format_phone(phone):
    pattern = r"(\+7|8)?\s*\(?(\d{3})\)?\s*(\d{3})[-\s]?(\d{2})[-\s]?(\d{2})(\s*\(?(доб.)\s*(\d+)\)?)?"
    subst = r"+7(\2)\3-\4-\5 \7\8"
    return re.sub(pattern, subst, phone).strip()


def is_contact_match(contact1, contact2):

    if contact1[0] != contact2[0]:
        return False

    if contact1[1] != contact2[1]:
        return False

    if contact1[2] and contact2[2] and contact1[2] != contact2[2]:
        return False
    return True


with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


new_contacts = []
for row in contacts_list[1:]:  # Пропускаем заголовок
    row[:3] = correct_name(' '.join(row[:3]))
    row[5] = format_phone(row[5])


    matched = False
    for existing_contact in new_contacts:
        if is_contact_match(existing_contact, row):
            matched = True

            for i in range(3, 7):
                existing_contact[i] = existing_contact[i] or row[i]
            break

    if not matched:
        new_contacts.append(row)


final_contacts = [contacts_list[0]] + new_contacts


with open("phonebook.csv", "w", newline="", encoding='utf-8') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(final_contacts)
