from datetime import date, timedelta

from config import MEMBERS_FILE, PLANS_FILE
from storage import load_data, save_data, next_id
from plan_manager import get_plans
from utils import (
    read_text,
    read_date,
    membership_status,
    money,
)


def get_members():
    return load_data(MEMBERS_FILE, [])


def find_member(member_id):
    return next(
        (member for member in get_members()
         if member["id"].lower() == member_id.strip().lower()),
        None
    )


def display_member(member):
    print("-" * 65)
    print(f"Member ID   : {member['id']}")
    print(f"Name        : {member['name']}")
    print(f"Phone       : {member['phone']}")
    print(f"Email       : {member['email'] or 'Not provided'}")
    print(f"Plan ID     : {member['plan_id']}")
    print(f"Start date  : {member['start_date']}")
    print(f"End date    : {member['end_date']}")
    print(f"Status      : {membership_status(member)}")
    print(f"Account     : {member.get('status', 'Active')}")
    print("-" * 65)


def list_members():
    members = get_members()

    if not members:
        print("No members registered.")
        return

    for member in members:
        display_member(member)


def add_member():
    members = get_members()
    plans = get_plans()

    if not plans:
        print("Create a membership plan first.")
        return

    name = read_text("Full name: ")
    phone = read_text("Phone number: ")

    if not phone.replace("+", "").replace("-", "").replace(" ", "").isdigit():
        print("Enter a valid phone number using digits, spaces, +, or -.")
        return

    if any(member["phone"] == phone for member in members):
        print("This phone number is already registered.")
        return

    email = read_text("Email (optional): ", required=False)

    if email and ("@" not in email or "." not in email.split("@")[-1]):
        print("Please enter a valid email address.")
        return

    print("\nMembership plans:")
    for plan in plans:
        print(
            f"{plan['id']} - {plan['name']} "
            f"({plan['duration_days']} days) - {money(plan['price'])}"
        )

    plan_id = read_text("Choose plan ID: ").upper()
    plan = next((p for p in plans if p["id"] == plan_id), None)

    if not plan:
        print("Invalid plan ID.")
        return

    start_date = read_date(
        f"Membership start date (YYYY-MM-DD, blank for today): ",
        allow_blank=True
    )

    if start_date is None:
        start_date = date.today()

    end_date = start_date + timedelta(days=plan["duration_days"] - 1)

    member = {
        "id": next_id(members, "M"),
        "name": name,
        "phone": phone,
        "email": email,
        "plan_id": plan["id"],
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "status": "Active",
        "created_at": date.today().isoformat(),
    }

    members.append(member)
    save_data(MEMBERS_FILE, members)

    print(f"Member registered successfully. Member ID: {member['id']}")
    print(f"Membership ends on: {member['end_date']}")
    print(f"Plan price: {money(plan['price'])}")
    print("Record the payment separately using Payment Management.")


def search_member():
    term = read_text("Enter member ID, name, or phone: ").lower()

    matches = [
        member for member in get_members()
        if term in member["id"].lower()
        or term in member["name"].lower()
        or term in member["phone"].lower()
    ]

    if not matches:
        print("No matching members found.")
        return

    for member in matches:
        display_member(member)


def update_member():
    members = get_members()
    member_id = read_text("Enter member ID: ").upper()

    member = next((m for m in members if m["id"] == member_id), None)

    if not member:
        print("Member not found.")
        return

    print("Leave a field blank to keep its current value.")
    name = input(f"Name [{member['name']}]: ").strip()
    phone = input(f"Phone [{member['phone']}]: ").strip()
    email = input(f"Email [{member['email']}]: ").strip()

    if name:
        member["name"] = name

    if phone:
        normalized = phone.replace("+", "").replace("-", "").replace(" ", "")
        if not normalized.isdigit():
            print("Invalid phone number.")
            return

        if any(
            m["id"] != member_id and m["phone"] == phone
            for m in members
        ):
            print("Another member already uses this phone number.")
            return

        member["phone"] = phone

    if email:
        if "@" not in email or "." not in email.split("@")[-1]:
            print("Invalid email address.")
            return
        member["email"] = email

    save_data(MEMBERS_FILE, members)
    print("Member details updated.")


def change_member_status():
    members = get_members()
    member_id = read_text("Enter member ID: ").upper()
    member = next((m for m in members if m["id"] == member_id), None)

    if not member:
        print("Member not found.")
        return

    current = member.get("status", "Active")
    new_status = "Inactive" if current == "Active" else "Active"

    print(f"Current account status: {current}")
    confirmation = input(
        f"Change account status to {new_status}? (y/n): "
    ).strip().lower()

    if confirmation == "y":
        member["status"] = new_status
        save_data(MEMBERS_FILE, members)
        print("Account status updated.")


def member_menu():
    while True:
        print("\n--- MEMBER MANAGEMENT ---")
        print("1. Register member")
        print("2. View all members")
        print("3. Search member")
        print("4. Update member")
        print("5. Activate/deactivate member")
        print("0. Back")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_member()
        elif choice == "2":
            list_members()
        elif choice == "3":
            search_member()
        elif choice == "4":
            update_member()
        elif choice == "5":
            change_member_status()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")

        if choice != "0":
            input("\nPress Enter to continue...")
