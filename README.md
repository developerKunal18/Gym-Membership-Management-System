# Gym Membership Management System

A console-based Gym Membership Management System built using Python.
The application uses JSON files to store membership, payment, plan, and
attendance records locally.

## Features

- Register new gym members.
- View, search, and update member information.
- Activate or deactivate member accounts.
- Create and update membership plans.
- Record payments and view payment history.
- Mark member attendance.
- Prevent duplicate attendance check-ins on the same day.
- Allow attendance only when membership is active.
- Check active, expired, upcoming, and inactive memberships.
- Identify memberships expiring within seven days.
- Generate revenue and attendance reports.
- Automatically generate unique record IDs.
- Validate user input and handle common data errors.

## Technologies

- Python 3.10+
- JSON
- Python standard library

No third-party packages are required.

## Project Structure

    GymMembershipManagementSystem/
    ├── main.py
    ├── config.py
    ├── storage.py
    ├── utils.py
    ├── member_manager.py
    ├── plan_manager.py
    ├── payment_manager.py
    ├── attendance_manager.py
    ├── report_manager.py
    ├── requirements.txt
    ├── .gitignore
    ├── README.md
    └── data/
        ├── members.json
        ├── plans.json
        ├── payments.json
        └── attendance.json

## Installation

1. Install Python 3.10 or later.
2. Download or clone this project.
3. Open a terminal in the project folder.
4. Make sure the four JSON files exist inside the data folder.
5. Run the application.

## Run the Application

Windows:

    python main.py

If the command above does not work, try:

    py main.py

Linux or macOS:

    python3 main.py

## How to Use

### 1. Register a Member

Open Member Management and select Register Member.

Enter the member's name, phone number, email, membership plan, and
membership start date. Leave the start date blank to use today's date.

The application generates a member ID automatically.

### 2. Manage Membership Plans

Open Membership Plan Management to view, create, or update plans.

Default plans include Monthly, Quarterly, Half Yearly, and Yearly.

### 3. Record a Payment

Open Payment Management, select Record Payment, and enter the member ID.

Enter the amount received and choose Cash, UPI, Card, or Bank Transfer.

The application creates a receipt number and stores the transaction.

### 4. Mark Attendance

Open Attendance Management and select Mark Attendance.

Enter the member ID. The application checks membership validity and
prevents a second check-in for the same member on the same day.

### 5. Generate Reports

Open Reports to view membership statuses, expiring memberships,
recorded revenue, and attendance statistics.

## Membership Rules

- Monthly plans last 30 days.
- Quarterly plans last 90 days.
- Half Yearly plans last 180 days.
- Yearly plans last 365 days.
- The membership end date includes the final membership day.
- Membership status is calculated from the start date, end date,
  and account status.
- Attendance is allowed only when the membership status is Active.
- Expiry reports show active memberships ending within the next
  seven days, including today.

## Data Storage

The application stores information in local JSON files.

- members.json stores member profiles and membership dates.
- plans.json stores membership plans and prices.
- payments.json stores recorded payment transactions.
- attendance.json stores check-in history.

Back up the data folder regularly. Do not manually edit JSON records
unless you understand their structure.

## Important Limitations

- This is a learning project, not a production-ready gym management system.
- Payments are recorded locally; no real payment gateway is connected.
- There is no login system or role-based access control.
- JSON storage is suitable for small demonstrations, not concurrent
  multi-user production use.
- Membership registration and payment recording are separate operations.
- Editing a plan does not automatically change existing members'
  saved membership end dates.
- There is no automatic payment reminder service.

## Future Improvements

- Add administrator and staff login.
- Add a graphical user interface using Tkinter.
- Add member photo uploads.
- Add QR-code check-in.
- Add membership renewal functionality.
- Add PDF receipts and downloadable reports.
- Add email or SMS expiry reminders.
- Migrate JSON storage to MySQL or PostgreSQL.
- Add automated unit tests.
- Add a payment gateway for real transactions.

## Learning Outcomes

This project demonstrates Python functions, modules, loops, conditionals,
exception handling, date calculations, JSON file operations, input
validation, and basic application architecture.
