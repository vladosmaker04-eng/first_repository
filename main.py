#Завдання 1 

from datetime import datetime, date

def get_days_from_today(date_str):
    try:
        given_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        today = date.today()
        return (today - given_date).days
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD")
    



#Завдання 2

import random

def get_numbers_ticket(min, max, quantity):
    if (
        not isinstance(min, int) or
        not isinstance(max, int) or
        not isinstance(quantity, int) or
        min < 1 or
        max > 1000 or
        min > max or
        quantity < 1 or
        quantity > (max - min + 1)
    ):
        return []

    return sorted(random.sample(range(min, max + 1), quantity))


lottery_numbers = get_numbers_ticket(1, 49, 6)
print(lottery_numbers)





#Задання 3 

import re

def normalize_phone(phone_number):
    phone = re.sub(r"[^\d+]", "", phone_number)

    if phone.startswith("+"):
        return phone
    if phone.startswith("380"):
        return "+" + phone
    return "+38" + phone


raw_numbers = [
    "067\t123 4567",
    "(095) 234-5678\n",
    "+380 44 123 4567",
    "380501234567",
    "    +38(050)123-32-34",
    "     0503451234",
    "(050)8889900",
    "38050-111-22-22",
    "38050 111 22 11   ",
]

sanitized_numbers = [normalize_phone(num) for num in raw_numbers]
print(sanitized_numbers)


#Завдання 4 

from datetime import datetime, timedelta

def get_upcoming_birthdays(users):
    today = datetime.strptime("2024.01.22", "%Y.%m.%d").date()
    end_date = today + timedelta(days=7)
    result = []

    for user in users:
        bday = datetime.strptime(user["birthday"], "%Y.%m.%d").date()
        bday_this_year = bday.replace(year=today.year)

        if bday_this_year < today:
            bday_this_year = bday_this_year.replace(year=today.year + 1)

        if today <= bday_this_year <= end_date:
            congratulation_date = bday_this_year
            if congratulation_date.weekday() == 5:
                congratulation_date += timedelta(days=2)
            elif congratulation_date.weekday() == 6:
                congratulation_date += timedelta(days=1)

            result.append({
                "name": user["name"],
                "congratulation_date": congratulation_date.strftime("%Y.%m.%d")
            })

    return result


users = [
    {"name": "John Doe", "birthday": "1985.01.23"},
    {"name": "Jane Smith", "birthday": "1990.01.27"}
]

print(get_upcoming_birthdays(users))