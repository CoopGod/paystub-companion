# Import packages
from cs50 import SQL
from flask import Markup

# Load database
db = SQL("sqlite:///paystub-companion.db")

# Returns all employees and their info as well as buttons for editing and printing
def loadTable():
    tableInfo = Markup("")
    data = db.execute("SELECT * FROM employees")
    iteration = 1
    while iteration <= len(data):
        employee_name = data[iteration - 1]['Name']
        employee_position = data[iteration - 1]['Position']
        money_YTD = data[iteration - 1]['Money-YTD']
        tableInfo += Markup(f'''
        <tr><td>{employee_name}</td>
        <td>{employee_position}</td>
        <td>{round(float(money_YTD),2)}</td>
        <td><button name=print{iteration}>PRINT</button></td>
        <td><button name=add{iteration}>ADD</button></td></tr>
        ''')

        iteration += 1

    return tableInfo

# Returns table for paystub creation
def loadStub(employee_ID):
    tableInfo = Markup("")
    data = db.execute("SELECT * FROM employees WHERE ID = ?", employee_ID)
    taxes = db.execute("SELECT * FROM taxes")
    employee_name = data[0]['Name']
    employee_position = data[0]['Position']
    money_made = data[0]['Money-made']
    ei_off = float(money_made) * taxes[0]['EI']
    income_tax_off = money_made * taxes[0]['INCOME']
    ammount_due = money_made - ei_off - income_tax_off

    taxes_YTD = data[0]['Taxes-YTD'] + ei_off + income_tax_off
    money_YTD = data[0]['Money-YTD'] + ammount_due

    tableInfo += Markup(
        f'''<tr><th>Name</th><th>Position</th></tr>
        <tr><td>{employee_name}</td><td>{employee_position}</td></tr>

        <tr><th>Money Made</th><th>EI Deducted</th><th>Income Tax Deducted</th><th>Net Pay</th></tr>
        <tr><td>{round(float(money_made),3)}</td><td>{round(float(ei_off),3)}</td><td>{round(float(income_tax_off),3)}</td><td>{round(float(ammount_due),3)}</td></tr>

        <tr><th>Net Pay YTD</th><th>Tax Deducts YTD</th></tr>
        <tr><td>{round(float(money_YTD),3)}</td><td>{round(float(taxes_YTD),3)}</td></tr>
        '''
        )

    db.execute("UPDATE employees SET 'Money-made' = 0, 'Taxes-YTD' = ?, 'Money-YTD' = ? WHERE ID = ?", taxes_YTD, money_YTD, employee_ID)

    return tableInfo


def employeeCount():
    data = db.execute('SELECT * FROM employees')
    iteration = 0
    while iteration < iteration + 1:
        try:
            testVar = data[iteration]['Name']
            iteration += 1
        except IndexError:
            return (iteration + 1)
