def caching_fibonacci():
    # Кеш для збереження вже обчислених значень
    cache = {}

    def fibonacci(n):
        # Базові випадки
        if n <= 0:
            return 0
        if n == 1:
            return 1

        # Якщо вже є в кеші — повертаємо
        if n in cache:
            return cache[n]

        # Обчислюємо рекурсивно і зберігаємо в кеш
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]

    # Повертаємо внутрішню функцію (замикання)
    return fibonacci


# Приклад використання
fib = caching_fibonacci()

print(fib(10))  # 55
print(fib(15))  # 610
