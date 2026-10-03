from flask import Flask, render_template, request, redirect, session
import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:password@localhost/expense_tracker"
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ---------------- USER TABLE ----------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )

# ---------------- EXPENSE TABLE ----------------

class Expense(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    amount = db.Column(
        db.Float,
        nullable=False
    )

    category = db.Column(
        db.String(100),
        nullable=False
    )

    date = db.Column(
        db.String(50)
    )

    user_id = db.Column(
        db.Integer
    )

# ---------------- BUDGET TABLE ----------------

class Budget(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    amount = db.Column(
        db.Float,
        nullable=False
    )

    user_id = db.Column(
        db.Integer
    )

# ---------------- CREATE TABLES ----------------

with app.app_context():
    db.create_all()

# ---------------- HOME ----------------

@app.route('/')
def home():
    return redirect('/login')

# ---------------- REGISTER ----------------

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        user_exists = User.query.filter_by(
            email=email
        ).first()

        if user_exists:
            return "Email already registered"

        hashed_password = generate_password_hash(
            password
        )

        user = User(
            name=name,
            email=email,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        return redirect('/login')

    return render_template('register.html')

# ---------------- LOGIN ----------------

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(
            email=email
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):

            session['user_id'] = user.id

            return redirect('/dashboard')

        return "Invalid Email or Password"

    return render_template('login.html')

# ---------------- DASHBOARD ----------------

@app.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        return redirect('/login')

    user = User.query.get(
        session['user_id']
    )

    expenses = Expense.query.filter_by(
        user_id=session['user_id']
    ).all()

    budget = Budget.query.filter_by(
        user_id=session['user_id']
    ).first()

    total = sum(
        expense.amount
        for expense in expenses
    )

    budget_amount = 0

    if budget:
        budget_amount = budget.amount

    balance = budget_amount - total

    return render_template(
        'dashboard.html',
        user=user,
        expenses=expenses,
        total=total,
        budget=budget_amount,
        balance=balance,
        records=len(expenses)
    )

# ---------------- PROFILE ----------------

@app.route('/profile')
def profile():

    if 'user_id' not in session:
        return redirect('/login')

    user = User.query.get(
        session['user_id']
    )

    return render_template(
        'profile.html',
        user=user
    )

# ---------------- ADD EXPENSE ----------------

@app.route('/add', methods=['GET', 'POST'])
def add_expense():

    if 'user_id' not in session:
        return redirect('/login')

    if request.method == 'POST':

        amount = request.form['amount']
        category = request.form['category']
        date = request.form['date']

        expense = Expense(
            amount=float(amount),
            category=category,
            date=date,
            user_id=session['user_id']
        )

        db.session.add(expense)
        db.session.commit()

        return redirect('/dashboard')

    return render_template(
        'add_expense.html'
    )

# ---------------- DELETE EXPENSE ----------------

@app.route('/delete/<int:id>')
def delete_expense(id):

    if 'user_id' not in session:
        return redirect('/login')

    expense = Expense.query.get(id)

    if expense:
        db.session.delete(expense)
        db.session.commit()

    return redirect('/dashboard')

# ---------------- BUDGET ----------------

@app.route('/budget', methods=['GET', 'POST'])
def budget():

    if 'user_id' not in session:
        return redirect('/login')

    if request.method == 'POST':

        amount = float(
            request.form['budget']
        )

        existing_budget = Budget.query.filter_by(
            user_id=session['user_id']
        ).first()

        if existing_budget:

            existing_budget.amount = amount

        else:

            new_budget = Budget(
                amount=amount,
                user_id=session['user_id']
            )

            db.session.add(
                new_budget
            )

        db.session.commit()

        return redirect('/dashboard')

    return render_template(
        'budget.html'
    )

# ---------------- LOGOUT ----------------

@app.route('/logout')
def logout():

    session.clear()

    return redirect('/login')

# ---------------- RUN APP ----------------

if __name__ == "__main__":
    app.run(debug=True)
