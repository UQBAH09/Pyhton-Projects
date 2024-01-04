# Import necessary libraries
import sqlite3
import pandas as pd
import hashlib
from datetime import date
import time

# Specify the location of the SQLite database
location = "/home/uqbah/Python/ExpenseManger/DataBase.db"
conn = None
cur = None

try:
    # Attempt to connect to the SQLite database
    conn = sqlite3.connect(location)
    cur = conn.cursor()
except sqlite3.Error as e:
    print(f"There is a SQLite Error: {e}")

# Create the masterPassword table if it doesn't exist
cur.execute('''
CREATE TABLE IF NOT EXISTS masterPassword(
            ID INT PRIMARY KEY,
            NAME TEXT NOT NULL,
            MASTERPASSWORD TEXT NOT NULL 
)
''')
conn.commit()

# Check if there are any records in the masterPassword table
cur.execute("SELECT COUNT(*) FROM masterPassword")
passResult = cur.fetchone()

# If no records exist, insert a default user and password
if passResult[0] == 0:
    name, password = "USER1", hashlib.sha256("password".encode()).hexdigest()
    cur.execute("INSERT INTO masterPassword(NAME, MASTERPASSWORD) VALUES(?, ?)", (name, password))
    conn.commit()

# Retrieve the master password from the masterPassword table
sql = pd.read_sql_query("SELECT * FROM masterPassword", conn)
df = pd.DataFrame(sql, columns=["ID", "NAME", "MASTERPASSWORD"])
Password = df["MASTERPASSWORD"].tolist()

# Prompt the user to enter the master password
masterPass = input("Enter password: ")
masterPass = hashlib.sha256(masterPass.encode()).hexdigest()

# Check if the entered password matches the stored master password
if masterPass != Password[0]:
    print("Wrong password")
    exit()

# Create the expenses table if it doesn't exist
cur.execute('''
CREATE TABLE IF NOT EXISTS expenses(
            ID INT PRIMARY KEY,
            ITEM TEXT NOT NULL,
            PRICE REAL NOT NULL,
            DATE TEXT NOT NULL,
            MONTH TEXT NOT NULL,
            YEAR TEXT NOT NULL
) 
''')
conn.commit()

# Create the income table if it doesn't exist
cur.execute('''
CREATE TABLE IF NOT EXISTS income(
            ID INT PRIMARY KEY,
            TAG TEXT,
            INCOME REAL NOT NULL,
            DATE TEXT NOT NULL,
            MONTH INT NOT NULL,
            YEAR INT NOT NULL
) 
''')
conn.commit()

# Main loop for user interaction
option = None
while option != "exit":
    time.sleep(1)
    option = input("Enter 1 to write expenses, enter 2 to delete expenses, enter 3 to see all expenses, enter 4 to check current balance, enter 5 to write income, enter 6 to change password: \n")
    
    if option == '1':
        # Section for entering expenses
        time.sleep(1)
        print("Enter exit if you don't want to write anything else:")
        itemName = None
        itemPrice = None
        itemdate = None
        while itemName != 'exit':
            itemName = input("Enter item name:  ")
            if itemName != 'exit':
                itemPrice = float(input("Enter item price:  "))
                itemdate = date.today().strftime('%d-%B-%Y')
                cur.execute("INSERT INTO expenses(ITEM, PRICE, DATE, MONTH, YEAR) VALUES(?, ?, ?, ?, ?)", (itemName, itemPrice, itemdate, 0, 0))
                conn.commit()
                print("Successfully added.")
    
    elif option == '2':
        time.sleep(1)   # Waiting for a second
        delname = input("Enter name to delete  ")

        # Deleting the info.
        conn.execute("DELETE FROM expenses WHERE ITEM = ?", (delname,))
        conn.commit()
        print("Successfully deleted.")

    elif option == '3':
        time.sleep(1)   # Waiting for a second        
        # Section for viewing expenses based on month and year
        time.sleep(1)
        month = int(input("Enter month (01): "))
        year = int(input("Enter year (2024): "))
        sql = pd.read_sql_query("SELECT * FROM expenses", conn)
        db = pd.DataFrame(sql, columns=['ITEM', 'PRICE', 'DATE'])
        
        # Extract month and year from the 'DATE' column
        db['MONTH'] = pd.to_datetime(db['DATE']).dt.month
        db['YEAR'] = pd.to_datetime(db['DATE']).dt.year
        
        # Filter based on month and year
        filtered_expenses = db[(db['MONTH'] == month) & (db['YEAR'] == year)]
        print("Expenses:")
        print(filtered_expenses[['ITEM', 'PRICE', 'DATE']])

        sql = pd.read_sql_query("SELECT * FROM income", conn)
        db = pd.DataFrame(sql, columns=['TAG', 'INCOME', 'DATE'])
        
        # Extract month and year from the 'DATE' column
        db['MONTH'] = pd.to_datetime(db['DATE']).dt.month
        db['YEAR'] = pd.to_datetime(db['DATE']).dt.year

        # Filter based on month and year
        filtered_income = db[(db["MONTH"] == month) & db['YEAR'] == year]
        print("\nIncome:")
        print(filtered_income[['TAG', 'INCOME', 'DATE']])
    
    elif option == '4':
        time.sleep(1)   # Waiting for a second
        # Section for checking the current balance
        time.sleep(1)
        sql = pd.read_sql_query("SELECT * FROM expenses", conn)
        db = pd.DataFrame(sql, columns=['ITEM', 'PRICE', 'DATE'])
        totalExpense = db['PRICE'].tolist()
        total_expense = sum(float(i) for i in totalExpense)
        
        sql = pd.read_sql_query("SELECT * FROM income", conn)
        db = pd.DataFrame(sql, columns=['INCOME', 'DATE'])
        totalIncome = db['INCOME'].tolist()
        total_income = sum(float(i) for i in totalIncome)
        
        curentBalance = total_income - total_expense
        print(f"Your balance is {curentBalance}")

    elif option == '5':
        time.sleep(1)   # Waiting for a second
        # Section for entering income
        time.sleep(1)
        tag = input("Enter a tag ")
        income = float(input("Enter your income "))
        while type(income) != float:
            print("Only numbers can be entered")
            income = input("Enter your income again ")
        curentDate = date.today().strftime('%d-%m-%Y')
        cur.execute("INSERT INTO income(TAG, INCOME, DATE) VALUES(?, ?, ?)", (tag, income, curentDate))
        conn.commit()

        print("New income successfully added")

    elif option == '6':
        time.sleep(1)   # Waiting for a second
        # Section for changing the password
        cur.execute("DELETE FROM masterPassword")
        conn.commit()
        newPass = input("Enter new password:  ")
        confirmPass = input("Enter password again:  ")
        if newPass != confirmPass:
            print("Passwords don't match")
        else:
            name1, pass1 = "USER1", hashlib.sha256(newPass.encode()).hexdigest()
            cur.execute("INSERT INTO masterPassword(NAME, MASTERPASSWORD) VALUES(?, ?)", (name1, pass1))
            conn.commit()
            print("Password successfully changed.")
