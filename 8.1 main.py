def caching_fibonacci():
    cache = {}  # словник для збереження результатів

    def fibonacci(n):
        # базові випадки
        if n <= 0:
            return 0
        if n == 1:
            return 1

        # якщо вже є в кеші — повертаємо
        if n in cache:
            return cache[n]

        # обчислюємо і зберігаємо в кеш
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]

    return fibonacci
