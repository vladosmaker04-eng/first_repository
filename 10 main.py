from __future__ import annotations

from collections import UserDict
from datetime import datetime, date, timedelta


# ---------- Helpers / Decorators ----------

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return "Not enough arguments. Check the command format."
        except ValueError as e:
            return str(e)
        except KeyError:
            return "Contact not found."
        except AttributeError:
            return "Contact not found."
    return wrapper


def parse_input(user_input: str):
    user_input = user_input.strip()
    if not user_input:
        return "", []
    parts = user_input.split()
    command = parts[0].lower()
    args = parts[1:]
    return command, args


# ---------- Core Classes ----------

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value: str):
        value = str(value)
        if not (value.isdigit() and len(value) == 10):
            raise ValueError("Invalid phone. Phone number must contain exactly 10 digits.")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value: str):
        try:
            dt = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(dt)

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday: Birthday | None = None

    def add_phone(self, phone: str) -> None:
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> bool:
        phone = str(phone)
        for i, p in enumerate(self.phones):
            if p.value == phone:
                self.phones.pop(i)
                return True
        return False

    def edit_phone(self, old_phone: str, new_phone: str) -> bool:
        old_phone = str(old_phone)
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)  # валідація нового
                return True
        return False

    def find_phone(self, phone: str) -> Phone | None:
        phone = str(phone)
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday_str: str) -> None:
        self.birthday = Birthday(birthday_str)

    def __str__(self):
        phones_str = "; ".join(p.value for p in self.phones) if self.phones else "-"
        bday_str = str(self.birthday) if self.birthday else "-"
        return f"Contact name: {self.name.value}, phones: {phones_str}, birthday: {bday_str}"


class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        return self.data.get(str(name))

    def delete(self, name: str) -> bool:
        name = str(name)
        if name in self.data:
            del self.data[name]
            return True
        return False

    def get_upcoming_birthdays(self) -> list[dict]:
        """
        Повертає список словників виду:
        [{"name": "John", "congratulation_date": "07.03.2026"}, ...]
        Логіка: беремо дні народження на наступні 7 днів включно.
        Якщо дата привітання припадає на Сб/Нд — переносимо на Пн.
        """
        today = date.today()
        end_day = today + timedelta(days=7)
        result = []

        for record in self.data.values():
            if not record.birthday:
                continue

            bday: date = record.birthday.value
            this_year_bday = bday.replace(year=today.year)

            # якщо ДН у цьому році вже був — беремо наступний рік
            if this_year_bday < today:
                this_year_bday = this_year_bday.replace(year=today.year + 1)

            if today <= this_year_bday <= end_day:
                congratulation_day = this_year_bday
                # перенос з вихідних на понеділок
                if congratulation_day.weekday() == 5:   # Saturday
                    congratulation_day += timedelta(days=2)
                elif congratulation_day.weekday() == 6: # Sunday
                    congratulation_day += timedelta(days=1)

                result.append({
                    "name": record.name.value,
                    "congratulation_date": congratulation_day.strftime("%d.%m.%Y")
                })

        # зручно відсортувати по даті привітання
        result.sort(key=lambda x: datetime.strptime(x["congratulation_date"], "%d.%m.%Y").date())
        return result


# ---------- Command Handlers ----------

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found."

    if not record.edit_phone(old_phone, new_phone):
        return "Old phone not found."
    return "Phone number updated."


@input_error
def show_phone(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    if not record.phones:
        return "No phones for this contact."
    return "; ".join(p.value for p in record.phones)


@input_error
def show_all(book: AddressBook):
    if not book.data:
        return "Address book is empty."
    return "\n".join(str(record) for record in book.data.values())


@input_error
def add_birthday(args, book: AddressBook):
    name, birthday_str, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    record.add_birthday(birthday_str)
    return "Birthday added."


@input_error
def show_birthday(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    if not record.birthday:
        return "Birthday not set."
    return str(record.birthday)


@input_error
def birthdays(book: AddressBook):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No birthdays in the next 7 days."
    lines = [f"{item['name']}: {item['congratulation_date']}" for item in upcoming]
    return "\n".join(lines)


# ---------- Main Loop ----------

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if not command:
            print("Please enter a command.")
            continue

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(book))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
