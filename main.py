from config import (
    DATA_DIR,
    MEMBERS_FILE,
    PLANS_FILE,
    PAYMENTS_FILE,
    ATTENDANCE_FILE,
    DEFAULT_PLANS,
)
from storage import ensure_file, load_data, save_data

from member_manager import member_menu
from plan_manager import plan_menu
from payment_manager import payment_menu
from attendance_manager import attendance_menu
from report_manager import report_menu


def initialize_application():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    ensure_file(MEMBERS_FILE, [])
    ensure_file(PLANS_FILE, DEFAULT_PLANS)
    ensure_file(PAYMENTS_FILE, [])
    ensure_file(ATTENDANCE_FILE, [])

    plans = load_data(PLANS_FILE, DEFAULT_PLANS)

    if not plans:
        save_data(PLANS_FILE, DEFAULT_PLANS)


def main():
    try:
        initialize_application()

        while True:
            print("\n" + "=" * 50)
            print("       GYM MEMBERSHIP MANAGEMENT SYSTEM")
            print("=" * 50)
            print("1. Member Management")
            print("2. Membership Plan Management")
            print("3. Payment Management")
            print("4. Attendance Management")
            print("5. Reports")
            print("0. Exit")
            print("-" * 50)

            choice = input("Enter your choice: ").strip()

            try:
                if choice == "1":
                    member_menu()
                elif choice == "2":
                    plan_menu()
                elif choice == "3":
                    payment_menu()
                elif choice == "4":
                    attendance_menu()
                elif choice == "5":
                    report_menu()
                elif choice == "0":
                    print("Thank you for using the Gym Management System.")
                    break
                else:
                    print("Invalid choice. Select an option from 0 to 5.")

            except (OSError, ValueError) as error:
                print(f"\nOperation could not be completed: {error}")
                print("Check the data files and try again.")

    except (OSError, ValueError) as error:
        print(f"Application could not start: {error}")
        print("Check your data folder and JSON files.")


if __name__ == "__main__":
    main()
