from collections import UserDict
from datetime import datetime, timedelta


# ================= ДЕКОРАТОР =================
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me correct data please."
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Enter correct arguments."
    return inner


# ================= КЛАСИ =================
class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone must be 10 digits")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def edit_phone(self, old, new):
        for phone in self.phones:
            if phone.value == old:
                phone.value = Phone(new).value
                return "Phone updated."
        raise ValueError

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p

    def add_birthday(self, date):
        self.birthday = Birthday(date)

    def __str__(self):
        phones = ", ".join(p.value for p in self.phones)
        bday = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "None"
        return f"{self.name.value}: {phones}, Birthday: {bday}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        result = []

        for record in self.data.values():
            if record.birthday:
                bday = record.birthday.value.replace(year=today.year)

                if bday < today:
                    bday = bday.replace(year=today.year + 1)

                if 0 <= (bday - today).days <= 7:
                    congrat_date = bday

                    if congrat_date.weekday() >= 5:
                        congrat_date += timedelta(days=(7 - congrat_date.weekday()))

                    result.append({
                        "name": record.name.value,
                        "date": congrat_date.strftime("%d.%m.%Y")
                    })

        return result


# ================= ФУНКЦІЇ =================
def parse_input(user_input):
    cmd, *args = user_input.strip().split()
    return cmd.lower(), args


@input_error
def add_contact(args, book):
    name, phone, *_ = args
    record = book.find(name)

    if record is None:
        record = Record(name)
        book.add_record(record)
        record.add_phone(phone)
        return "Contact added."

    record.add_phone(phone)
    return "Contact updated."


@input_error
def change_contact(args, book):
    name, old, new = args
    record = book.find(name)
    if record is None:
        raise KeyError
    return record.edit_phone(old, new)


@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError
    return ", ".join(p.value for p in record.phones)


@input_error
def show_all(book):
    return "\n".join(str(record) for record in book.data.values())


@input_error
def add_birthday(args, book):
    name, date = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.add_birthday(date)
    return "Birthday added."


@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError
    if not record.birthday:
        return "No birthday set."
    return record.birthday.value.strftime("%d.%m.%Y")


@input_error
def birthdays(book):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No birthdays this week."
    return "\n".join(f"{item['name']} - {item['date']}" for item in upcoming)


# ================= MAIN =================
def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter command: ")
        command, args = parse_input(user_input)

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
