# FOR HACKED2021: PAYSTUB-COMPANION
# Import packages
import os
from cs50 import SQL
from flask import Flask, redirect, render_template, request, session, Markup
from flask_session import Session
# Import helper file
from helper import *

# Configure application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret, secret key'

# Load database
db = SQL("sqlite:///paystub-companion.db")

# Load main page and display all employees
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        dataCount = db.execute("SELECT ID FROM employees")
        iteration = 1
        while iteration <= len(dataCount):
            if str(iteration) in str(request.form):
                session['id'] = iteration
                # when print button pressed
                if f'print{iteration}' in str(request.form):
                    return redirect("/print")
                # when add button is pressed
                elif f'add{iteration}' in str(request.form):
                    return redirect("/add")
            iteration += 1
        if 'create' in str(request.form):
            return redirect('/create')
        elif 'settings' in str(request.form):
            return redirect('settings')
        print('error')
    else:
        tableInfo = loadTable()
        return render_template('main.html', tableInfo=tableInfo)

@app.route('/print', methods=["GET"])
def printStub():
    employee_ID = session['id']
    tableInfo = loadStub(employee_ID)

    return render_template('print.html', tableInfo=tableInfo)

@app.route('/add', methods=["GET", "POST"])
def addIncome():
    if request.method == "POST":
        employee_ID = session['id']
        ammount_added = request.form.get("income")
        db.execute("UPDATE employees SET 'Money-made' = ? WHERE ID = ?", float(ammount_added), employee_ID)
        return redirect('/')
    else:
        return render_template('add.html')

@app.route('/create', methods=["GET", "POST"])
def createEmployee():
    if request.method == "POST":
        # Get form data
        employee_name = request.form.get("name")
        employee_position = request.form.get("position")
        income_YTD = request.form.get('income-YTD')
        taxes_YTD = request.form.get('taxes-YTD')
        # Check how many employees (for ID assignment)
        employeeCounts = employeeCount()

        # update SQL
        db.execute("INSERT INTO employees (ID, Name, 'Money-made', 'Money-YTD', 'Taxes-YTD', position) VALUES (?, ?, ?, ?, ?, ?)", employeeCounts, employee_name, 0, income_YTD, taxes_YTD, employee_position)

        # Redirect
        return redirect('/')
    else:
        return render_template('create.html')

@app.route('/settings', methods=["GET", "POST"])
def settings():
    if request.method == "POST":
        # get form data
        new_ei = request.form.get("EI")
        new_ei = float(new_ei) / 100

        new_income_tax = request.form.get("income")
        new_income_tax = float(new_income_tax) / 100

        # Update SQL
        db.execute("UPDATE taxes SET EI = ?, INCOME = ?", new_ei, new_income_tax)

        # redirect
        return redirect('/')
    else:
        return render_template("settings.html")

