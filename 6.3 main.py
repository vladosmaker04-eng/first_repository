import sys
from pathlib import Path
from colorama import init, Fore, Style

init(autoreset=True)


def show_directory(path, level=0):
    try:
        items = sorted(path.iterdir(), key=lambda item: (item.is_file(), item.name.lower()))

        for item in items:
            indent = "    " * level

            if item.is_dir():
                print(f"{indent}{Fore.BLUE}{item.name}/{Style.RESET_ALL}")
                show_directory(item, level + 1)
            else:
                print(f"{indent}{Fore.YELLOW}{item.name}{Style.RESET_ALL}")

    except PermissionError:
        print(f"{'    ' * level}{Fore.RED}Немає доступу до: {path}{Style.RESET_ALL}")


def main():
    if len(sys.argv) < 2:
        print(Fore.RED + "Помилка: вкажіть шлях до директорії")
        return

    path = Path(sys.argv[1])

    if not path.exists():
        print(Fore.RED + "Помилка: шлях не існує")
        return

    if not path.is_dir():
        print(Fore.RED + "Помилка: це не директорія")
        return

    print(f"{Fore.BLUE}{path.name}/{Style.RESET_ALL}")
    show_directory(path, 1)


if __name__ == "__main__":
    main()
