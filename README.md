# Expense Tracker

A Flask-based expense tracking web application with user authentication, expense management, budgeting, profile pages, and a dashboard for tracking spending.

## Features

- User registration and login
- Password hashing with Werkzeug
- Add and delete expenses
- Budget management
- Expense dashboard with totals and balance
- User profile page
- Flask + SQLAlchemy backend
- MySQL support through PyMySQL

## Tech Stack

**Backend:** Python, Flask, Flask-SQLAlchemy

**Database:** MySQL

**Frontend:** HTML, CSS, Jinja2

## Project Structure

```text
expense-tracker/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── static/
│   └── style.css
└── templates/
    ├── add_expense.html
    ├── budget.html
    ├── dashboard.html
    ├── index.html
    ├── login.html
    ├── profile.html
    ├── register.html
    └── verify_otp.html
```

## Setup

1. Create a virtual environment:

```bash
python -m venv venv
```

2. Activate it on Windows:

```bash
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a MySQL database named `expense_tracker`.

5. Set environment variables:

```text
SECRET_KEY=your-secret-key
DATABASE_URL=mysql+pymysql://username:password@localhost/expense_tracker
```

6. Start the application:

```bash
python app.py
```

The application runs locally at `http://127.0.0.1:5000/`.

## Security

Sensitive credentials are intentionally excluded from the repository. Configure them with environment variables instead of committing passwords or secret keys.
