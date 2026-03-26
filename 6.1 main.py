def total_salary(path):
    total = 0
    count = 0

    try:
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()  # прибираємо \n
                if not line:
                    continue  # пропускаємо пусті рядки

                name, salary = line.split(",")  # розділяємо
                total += int(salary)  # додаємо зарплату
                count += 1

        if count == 0:
            return (0, 0)

        average = total / count
        return (total, average)

    except FileNotFoundError:
        print("Файл не знайдено!")
        return (0, 0)
    except Exception as e:
        print(f"Помилка: {e}")
        return (0, 0)
