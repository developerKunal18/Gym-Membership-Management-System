from datetime import date, datetime
from config import CURRENCY


def read_text(prompt, required=True):
    while True:
        value = input(prompt).strip()

        if value or not required:
            return value

        print("This field is required.")


def read_int(prompt, minimum=0, maximum=None):
    while True:
        value = input(prompt).strip()

        try:
            number = int(value)

            if number < minimum:
                print(f"Enter a number greater than or equal to {minimum}.")
                continue

            if maximum is not None and number > maximum:
                print(f"Enter a number less than or equal to {maximum}.")
                continue

            return number

        except ValueError:
            print("Please enter a valid whole number.")


def read_float(prompt, minimum=0):
    while True:
        value = input(prompt).strip()

        try:
            number = float(value)

            if number < minimum:
                print(f"Enter a value greater than or equal to {minimum}.")
                continue

            return round(number, 2)

        except ValueError:
            print("Please enter a valid amount.")


def read_date(prompt, allow_blank=False):
    while True:
        value = input(prompt).strip()

        if allow_blank and not value:
            return None

        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            print("Use the date format YYYY-MM-DD, for example 2026-10-18.")


def money(amount):
    return f"{CURRENCY}{float(amount):,.2f}"


def membership_status(member):
    today = date.today()

    try:
        start = date.fromisoformat(member["start_date"])
        end = date.fromisoformat(member["end_date"])
    except (KeyError, ValueError):
        return "Invalid dates"

    if member.get("status") == "Inactive":
        return "Inactive"

    if today < start:
        return "Upcoming"

    if today > end:
        return "Expired"

    return "Active"


def pause():
    input("\nPress Enter to continue...")


def print_heading(title):
    print("\n" + "=" * 65)
    print(title.center(65))
    print("=" * 65)
