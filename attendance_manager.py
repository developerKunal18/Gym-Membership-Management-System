from datetime import date, datetime

from config import ATTENDANCE_FILE
from storage import load_data, save_data, next_id
from member_manager import find_member
from utils import membership_status, read_text


def get_attendance():
    return load_data(ATTENDANCE_FILE, [])


def mark_attendance():
    member_id = read_text("Enter member ID: ").upper()
    member = find_member(member_id)

    if not member:
        print("Member not found.")
        return

    if membership_status(member) != "Active":
        print("Attendance denied: membership is not currently active.")
        return

    records = get_attendance()
    today = date.today().isoformat()

    if any(
        record["member_id"] == member_id
        and record["date"] == today
        for record in records
    ):
        print("Attendance has already been marked for this member today.")
        return

    record = {
        "id": next_id(records, "A"),
        "member_id": member_id,
        "member_name": member["name"],
        "date": today,
        "time": datetime.now().strftime("%H:%M:%S"),
    }

    records.append(record)
    save_data(ATTENDANCE_FILE, records)

    print("Attendance marked successfully.")
    print(f"Member: {member['name']}")
    print(f"Date: {record['date']}")
    print(f"Time: {record['time']}")


def view_today_attendance():
    today = date.today().isoformat()
    records = [r for r in get_attendance() if r["date"] == today]

    print(f"\nATTENDANCE FOR {today}")
    print("-" * 65)

    if not records:
        print("No attendance records for today.")
        return

    for record in sorted(records, key=lambda r: r["time"]):
        print(
            f"{record['time']} | {record['member_id']} | "
            f"{record['member_name']}"
        )

    print(f"\nTotal check-ins: {len(records)}")


def member_attendance_history():
    member_id = read_text("Enter member ID: ").upper()

    if not find_member(member_id):
        print("Member not found.")
        return

    records = [
        r for r in get_attendance()
        if r["member_id"] == member_id
    ]

    records.sort(key=lambda r: (r["date"], r["time"]), reverse=True)

    print("\nMEMBER ATTENDANCE HISTORY")
    print("-" * 65)

    if not records:
        print("No attendance records found.")
        return

    for record in records:
        print(f"{record['date']} | {record['time']}")

    print(f"Total visits: {len(records)}")


def attendance_menu():
    while True:
        print("\n--- ATTENDANCE MANAGEMENT ---")
        print("1. Mark attendance")
        print("2. View today's attendance")
        print("3. View member attendance history")
        print("0. Back")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            mark_attendance()
        elif choice == "2":
            view_today_attendance()
        elif choice == "3":
            member_attendance_history()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")

        if choice != "0":
            input("\nPress Enter to continue...")
