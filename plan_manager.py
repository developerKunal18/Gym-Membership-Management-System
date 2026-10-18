from config import PLANS_FILE, DEFAULT_PLANS
from storage import load_data, save_data, next_id
from utils import read_text, read_int, read_float, money


def get_plans():
    plans = load_data(PLANS_FILE, DEFAULT_PLANS)

    if not plans:
        plans = DEFAULT_PLANS.copy()
        save_data(PLANS_FILE, plans)

    return plans


def list_plans():
    plans = get_plans()

    print("\nAVAILABLE MEMBERSHIP PLANS")
    print("-" * 75)
    print(f"{'ID':<10}{'Plan':<20}{'Days':<10}{'Price':>15}")
    print("-" * 75)

    for plan in plans:
        print(
            f"{plan['id']:<10}"
            f"{plan['name']:<20}"
            f"{plan['duration_days']:<10}"
            f"{money(plan['price']):>15}"
        )

    if not plans:
        print("No plans available.")


def find_plan(plan_id):
    return next(
        (plan for plan in get_plans()
         if plan["id"].lower() == plan_id.strip().lower()),
        None
    )


def add_plan():
    plans = get_plans()
    name = read_text("Plan name: ")

    if any(plan["name"].lower() == name.lower() for plan in plans):
        print("A plan with this name already exists.")
        return

    duration = read_int("Membership duration in days: ", minimum=1)
    price = read_float("Plan price: ", minimum=0.01)

    plan = {
        "id": next_id(plans, "P"),
        "name": name,
        "duration_days": duration,
        "price": price,
    }

    plans.append(plan)
    save_data(PLANS_FILE, plans)
    print(f"Plan created successfully. Plan ID: {plan['id']}")


def update_plan():
    plans = get_plans()
    plan_id = read_text("Enter plan ID: ").upper()

    plan = next((p for p in plans if p["id"] == plan_id), None)

    if not plan:
        print("Plan not found.")
        return

    print("Leave a field blank to keep its current value.")
    name = input(f"Plan name [{plan['name']}]: ").strip()
    duration = input(
        f"Duration in days [{plan['duration_days']}]: "
    ).strip()
    price = input(f"Price [{plan['price']}]: ").strip()

    if name:
        if any(
            p["id"] != plan_id and p["name"].lower() == name.lower()
            for p in plans
        ):
            print("Another plan already uses this name.")
            return
        plan["name"] = name

    if duration:
        try:
            value = int(duration)
            if value <= 0:
                raise ValueError
            plan["duration_days"] = value
        except ValueError:
            print("Duration must be a positive whole number.")
            return

    if price:
        try:
            value = float(price)
            if value <= 0:
                raise ValueError
            plan["price"] = round(value, 2)
        except ValueError:
            print("Price must be greater than zero.")
            return

    save_data(PLANS_FILE, plans)
    print("Plan updated successfully.")


def plan_menu():
    while True:
        print("\n--- MEMBERSHIP PLAN MANAGEMENT ---")
        print("1. View plans")
        print("2. Add plan")
        print("3. Update plan")
        print("0. Back")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            list_plans()
        elif choice == "2":
            add_plan()
        elif choice == "3":
            update_plan()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")

        if choice != "0":
            input("\nPress Enter to continue...")
