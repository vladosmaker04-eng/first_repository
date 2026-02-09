#Завдання 1 

from datetime import datetime, date


def get_days_from_today(date_str: str) -> int:
    """
    Calculate the number of days between a given date and today.

    Args:
        date_str: Date string in format 'YYYY-MM-DD'.

    Returns:
        Integer number of days from the given date to today.
        If the given date is in the future, result will be negative.

    Raises:
        ValueError: If date_str has invalid format or impossible date.
    """
    try:
        given_date: date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValueError("Неправильний формат дати. Використовуйте 'YYYY-MM-DD'.") from exc

    today: date = datetime.today().date()
    return (today - given_date).days

if __name__ == "__main__":
    print(get_days_from_today("2020-10-09"))
    



#Завдання 2

import random


def get_numbers_ticket(min_num: int, max_num: int, quantity: int) -> list[int]:
    """
    Generate a sorted list of unique random lottery numbers.

    Args:
        min_num: Minimum possible number (>= 1).
        max_num: Maximum possible number (<= 1000).
        quantity: Amount of numbers to generate.

    Returns:
        Sorted list of unique random numbers.
        Returns empty list if input parameters are invalid.
    """
    if min_num < 1 or max_num > 1000:
        return []

    if min_num > max_num:
        return []

    if quantity < 1 or quantity > (max_num - min_num + 1):
        return []

    numbers: list[int] = random.sample(range(min_num, max_num + 1), quantity)
    return sorted(numbers)


if __name__ == "__main__":
    lottery_numbers = get_numbers_ticket(1, 49, 6)
    print("Ваші лотерейні числа:", lottery_numbers)





#Задання 3 

import re


def normalize_phone(phone_number: str) -> str:
    """
    Normalize Ukrainian phone number to standard format with country code.

    Rules:
    - Remove all characters except digits and '+'.
    - If starts with '+': return as is (after cleaning).
    - If starts with '380': add '+' at the beginning.
    - Otherwise add '+38'.

    Args:
        phone_number: Raw phone number string in any format.

    Returns:
        Normalized phone number string.
    """
    cleaned: str = re.sub(r"[^\d+]", "", phone_number.strip())

    if cleaned.startswith("+"):
        return cleaned

    if cleaned.startswith("380"):
        return f"+{cleaned}"

    return f"+38{cleaned}"


if __name__ == "__main__":
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
    print("Нормалізовані номери телефонів для SMS-розсилки:", sanitized_numbers)



#Завдання 4 

from datetime import datetime, date, timedelta
from typing import Any


def _move_to_monday(d: date) -> date:
    """
    Move date to next Monday if it falls on weekend.

    Saturday -> +2 days
    Sunday   -> +1 day
    """
    if d.weekday() == 5:      # Saturday
        return d + timedelta(days=2)

    if d.weekday() == 6:      # Sunday
        return d + timedelta(days=1)

    return d


def get_upcoming_birthdays(users: list[dict[str, Any]]) -> list[dict[str, str]]:
    """
    Get list of users who have birthdays within the next 7 days (including today).

    If birthday falls on weekend, congratulation date is moved to next Monday.

    Args:
        users: List of dictionaries with keys:
            - name: user's name
            - birthday: date string in format 'YYYY.MM.DD'

    Returns:
        List of dictionaries with keys:
            - name
            - congratulation_date (YYYY.MM.DD)
    """
    today: date = datetime.today().date()
    end_date: date = today + timedelta(days=7)

    upcoming_birthdays: list[dict[str, str]] = []

    for user in users:
        name = user.get("name")
        birthday_str = user.get("birthday")

        if not isinstance(name, str) or not isinstance(birthday_str, str):
            continue

        try:
            birthday: date = datetime.strptime(
                birthday_str, "%Y.%m.%d"
            ).date()
        except ValueError:
            continue

        birthday_this_year: date = date(
            today.year, birthday.month, birthday.day
        )

        if birthday_this_year < today:
            birthday_this_year = date(
                today.year + 1, birthday.month, birthday.day
            )

        if today <= birthday_this_year <= end_date:
            congratulation_date: date = _move_to_monday(birthday_this_year)

            upcoming_birthdays.append(
                {
                    "name": name,
                    "congratulation_date": congratulation_date.strftime("%Y.%m.%d"),
                }
            )

    return upcoming_birthdays


if __name__ == "__main__":
    users = [
        {"name": "Іван Петренко", "birthday": "1990.02.10"},
        {"name": "Марія Іванова", "birthday": "1988.02.11"},
        {"name": "Олег Коваль", "birthday": "1995.02.15"},
        {"name": "Анна Шевченко", "birthday": "1992.02.16"},
        {"name": "Петро Сидоренко", "birthday": "1980.03.01"},
    ]

    birthdays_this_week = get_upcoming_birthdays(users)

    print("Привітання на цьому тижні:")
    for item in birthdays_this_week:
        print(f"- {item['name']} → {item['congratulation_date']}")
