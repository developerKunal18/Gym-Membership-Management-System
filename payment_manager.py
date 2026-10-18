from datetime import date

from config import PAYMENTS_FILE, MEMBERS_FILE
from storage import load_data, save_data, next_id
from plan_manager import find_plan
from member_manager import find_member
from utils import read_text, read_float, money


def get_payments():
    return load_data(PAYMENTS_FILE, [])


def record_payment():
    members = load_data(MEMBERS_FILE, [])
    payments = get_payments()

    member_id = read_text("Enter member ID: ").upper()
    member = next((m for m in members if m["id"] == member_id), None)

    if not member:
        print("Member not found.")
        return

    plan = find_plan(member["plan_id"])

    if not plan:
        print("The member's plan no longer exists. Contact the administrator.")
        return

    print(f"Member: {member['name']}")
    print(f"Plan: {plan['name']}")
    print(f"Standard plan price: {money(plan['price'])}")

    amount = read_float("Amount received: ", minimum=0.01)

    if amount > 10000000:
        print("Amount exceeds the allowed limit.")
        return

    method = read_text(
        "Payment method (Cash/UPI/Card/Bank Transfer): "
    ).title()

    allowed_methods = {"Cash", "Upi", "Card", "Bank Transfer"}

    if method not in allowed_methods:
        print("Choose Cash, UPI, Card, or Bank Transfer.")
        return

    payment = {
        "id": next_id(payments, "PAY"),
        "member_id": member_id,
        "member_name": member["name"],
        "plan_id": plan["id"],
        "amount": round(amount, 2),
        "method": "UPI" if method == "Upi" else method,
        "date": date.today().isoformat(),
        "status": "Recorded",
    }

    payments.append(payment)
    save_data(PAYMENTS_FILE, payments)

    print("\nPayment recorded successfully.")
    print(f"Receipt number: {payment['id']}")
    print(f"Member: {payment['member_name']}")
    print(f"Amount: {money(payment['amount'])}")
    print(f"Method: {payment['method']}")
    print(f"Date: {payment['date']}")


def member_payment_history():
    member_id = read_text("Enter member ID: ").upper()

    if not find_member(member_id):
        print("Member not found.")
        return

    payments = [
        p for p in get_payments()
        if p["member_id"] == member_id
    ]

    if not payments:
        print("No payments found for this member.")
        return

    print("\nPAYMENT HISTORY")
    print("-" * 75)

    for payment in sorted(payments, key=lambda p: p["date"], reverse=True):
        print(
            f"{payment['id']} | {payment['date']} | "
            f"{money(payment['amount'])} | "
            f"{payment['method']} | {payment['status']}"
        )


def payment_menu():
    while True:
        print("\n--- PAYMENT MANAGEMENT ---")
        print("1. Record payment")
        print("2. View member payment history")
        print("0. Back")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            record_payment()
        elif choice == "2":
            member_payment_history()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")

        if choice != "0":
            input("\nPress Enter to continue...")
