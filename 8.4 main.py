from typing import Dict, List, Tuple, Callable


def input_error(func: Callable) -> Callable:
    """
    Декоратор для обробки помилок введення користувача.
    Обробляє: ValueError, IndexError, KeyError
    та повертає зрозумілі повідомлення, не зупиняючи програму.
    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            # Зазвичай: не вистачає аргументів або їх неправильна кількість
            return "Give me name and phone please."
        except IndexError:
            # Зазвичай: команда потребує аргумент (наприклад: phone <name>)
            return "Enter user name."
        except KeyError:
            # Зазвичай: контакту з таким ім'ям нема
            return "Contact not found."
    return inner


def parse_input(user_input: str) -> Tuple[str, List[str]]:
    """
    Розбирає введення на команду та аргументи.
    """
    parts = user_input.strip().split()
    if not parts:
        return "", []
    command = parts[0].lower()
    args = parts[1:]
    return command, args


@input_error
def add_contact(args: List[str], contacts: Dict[str, str]) -> str:
    """
    add <name> <phone>
    """
    if len(args) != 2:
        raise ValueError
    name, phone = args
    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args: List[str], contacts: Dict[str, str]) -> str:
    """
    change <name> <phone>
    """
    if len(args) != 2:
        raise ValueError
    name, phone = args
    if name not in contacts:
        raise KeyError
    contacts[name] = phone
    return "Contact updated."


@input_error
def show_phone(args: List[str], contacts: Dict[str, str]) -> str:
    """
    phone <name>
    """
    if len(args) != 1:
        # якщо нічого не ввели або ввели зайве — вважаємо помилкою введення
        raise IndexError
    name = args[0]
    if name not in contacts:
        raise KeyError
    return f"{name}: {contacts[name]}"


@input_error
def show_all(args: List[str], contacts: Dict[str, str]) -> str:
    """
    all
    """
    if args:
        # all не потребує аргументів
        raise ValueError
    if not contacts:
        return "No contacts saved."
    lines = [f"{name}: {phone}" for name, phone in contacts.items()]
    return "\n".join(lines)


def main() -> None:
    contacts: Dict[str, str] = {}

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ("exit", "close", "goodbye"):
            print("Good bye!")
            break

        if command == "hello":
            print("How can I help you?")
            continue

        if command == "add":
            print(add_contact(args, contacts))
            continue

        if command == "change":
            print(change_contact(args, contacts))
            continue

        if command == "phone":
            print(show_phone(args, contacts))
            continue

        if command == "all":
            print(show_all(args, contacts))
            continue

        if command == "":
            # користувач просто натиснув Enter
            continue

        print("Invalid command.")


if __name__ == "__main__":
    main()
