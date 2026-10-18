from datetime import date, timedelta

from config import (
    MEMBERS_FILE,
    PAYMENTS_FILE,
    ATTENDANCE_FILE,
    EXPIRY_WARNING_DAYS,
)
from storage import load_data
from utils import membership_status, money


def membership_report():
    members = load_data(MEMBERS_FILE, [])

    counts = {
        "Active": 0,
        "Expired": 0,
        "Upcoming": 0,
        "Inactive": 0,
        "Invalid dates": 0,
    }

    for member in members:
        status = membership_status(member)
        counts[status] = counts.get(status, 0) + 1

    print("\nMEMBERSHIP REPORT")
    print("-" * 40)
    print(f"Total registered members: {len(members)}")

    for status, count in counts.items():
        print(f"{status:<20}: {count}")


def expiry_report():
    members = load_data(MEMBERS_FILE, [])
    today = date.today()
    last_day = today + timedelta(days=EXPIRY_WARNING_DAYS)

    expiring = []

    for member in members:
        if membership_status(member) != "Active":
            continue

        try:
            end_date = date.fromisoformat(member["end_date"])
        except (KeyError, ValueError):
            continue

        if today <= end_date <= last_day:
            expiring.append((member, end_date))

    print(f"\nMEMBERSHIPS EXPIRING IN THE NEXT {EXPIRY_WARNING_DAYS} DAYS")
    print("-" * 70)

    if not expiring:
        print("No active memberships are expiring soon.")
        return

    for member, end_date in sorted(expiring, key=lambda item: item[1]):
        days_left = (end_date - today).days
        print(
            f"{member['id']} | {member['name']} | "
            f"{member['phone']} | Ends: {end_date} | "
            f"{days_left} day(s) left"
        )


def revenue_report():
    payments = load_data(PAYMENTS_FILE, [])
    today = date.today()
    month_prefix = today.strftime("%Y-%m")

    total_revenue = sum(
        float(p["amount"])
        for p in payments
        if p.get("status") == "Recorded"
    )

    monthly_revenue = sum(
        float(p["amount"])
        for p in payments
        if p.get("status") == "Recorded"
        and str(p.get("date", "")).startswith(month_prefix)
    )

    print("\nREVENUE REPORT")
    print("-" * 45)
    print(f"All-time recorded revenue: {money(total_revenue)}")
    print(f"Revenue this month:        {money(monthly_revenue)}")
    print(f"Recorded transactions:     {len(payments)}")


def attendance_report():
    records = load_data(ATTENDANCE_FILE, [])
    today = date.today().isoformat()
    month_prefix = date.today().strftime("%Y-%m")

    today_records = [r for r in records if r.get("date") == today]
    month_records = [
        r for r in records
        if str(r.get("date", "")).startswith(month_prefix)
    ]

    unique_month_members = {
        r["member_id"] for r in month_records
    }

    print("\nATTENDANCE REPORT")
    print("-" * 45)
    print(f"Today's check-ins: {len(today_records)}")
    print(f"This month's total visits: {len(month_records)}")
    print(f"Members who visited this month: {len(unique_month_members)}")


def report_menu():
    while True:
        print("\n--- REPORTS ---")
        print("1. Membership status report")
        print("2. Expiring membership report")
        print("3. Revenue report")
        print("4. Attendance report")
        print("0. Back")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            membership_report()
        elif choice == "2":
            expiry_report()
        elif choice == "3":
            revenue_report()
        elif choice == "4":
            attendance_report()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")

        if choice != "0":
            input("\nPress Enter to continue...")
