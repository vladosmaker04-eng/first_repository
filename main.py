#task1.py

from __future__ import annotations


def total_salary(path: str) -> tuple[int, float]:
    """
    Reads a salary file where each line is: "Name,Salary" (comma, no spaces).
    Returns (total_salary, average_salary).

    Handles:
    - FileNotFoundError
    - bad lines / bad salary values (skips invalid lines)
    """
    total = 0
    count = 0

    try:
        with open(path, "r", encoding="utf-8") as file:
            for line_no, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue

                parts = line.split(",")
                if len(parts) != 2:
                    # Bad format -> skip line
                    continue

                name, salary_str = parts[0].strip(), parts[1].strip()
                if not name:
                    continue

                try:
                    salary = int(salary_str)
                except ValueError:
                    # Salary is not an integer -> skip
                    continue

                total += salary
                count += 1

    except FileNotFoundError:
        return 0, 0.0
    except OSError:
        return 0, 0.0

    average = total / count if count else 0.0
    return total, average


if __name__ == "__main__":
    total, avg = total_salary("salary_file.txt")
    print(f"Загальна сума заробітної плати: {total}, Середня заробітна плата: {avg}")
