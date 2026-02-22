import re
from typing import Callable, Generator


def generator_numbers(text: str) -> Generator[float, None, None]:
    """
    Yields all real numbers from text that are separated by spaces on both sides.
    Example match: " 1000.01 ", " 27.45 ", " 324.00 "
    """
    # Число: цілі + необов'язкова дробова частина.
    # Вимога: з обох боків мають бути пробіли.
    pattern = r" (?P<num>\d+(?:\.\d+)?) "

    for match in re.finditer(pattern, text):
        yield float(match.group("num"))


def sum_profit(text: str, func: Callable[[str], Generator[float, None, None]]) -> float:
    """
    Sums all numbers produced by generator function func(text).
    """
    return sum(func(text))


# Приклад використання
if __name__ == "__main__":
    text = (
        "Загальний дохід працівника складається з декількох частин: 1000.01 "
        "як основний дохід, доповнений додатковими надходженнями 27.45 і "
        "324.00 доларів."
    )
    total_income = sum_profit(text, generator_numbers)
    print(f"Загальний дохід: {total_income:.2f}")
