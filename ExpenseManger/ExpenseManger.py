# Import necessary libraries
import sqlite3
import pandas as pd
import hashlib
from datetime import date
import time

# Define the location of the SQLite database file
LOCATION = "/home/uqbah/Python/ExpenseManger/DataBase.db"

# Function to connect to the SQLite database
def connect_to_database(location):
    try:
        # Attempt to connect to the SQLite database
        conn = sqlite3.connect(location)
        return conn, conn.cursor()
    
    except sqlite3.Error as e:
        print(f"There is a SQLite Error: {e}")
        return None, None

# Function to initialize the master password table
def intialize_masterpass_table(cur):
    # Create the masterPassword table if it doesn't exist
    cur.execute('''
    CREATE TABLE IF NOT EXISTS masterPassword(
                ID INT PRIMARY KEY,
                NAME TEXT NOT NULL,
                MASTERPASSWORD TEXT NOT NULL 
    )
    ''')
    return cur

# Function to set a default user and password if no records exist
def first_time_password(cur):
    # Check if any records exist in the masterPassword table
    cur.execute("SELECT COUNT(*) FROM masterPassword")
    passResult = cur.fetchone()

    # If no records exist, insert a default user and password
    if passResult[0] == 0:
        name, password = "USER1", hashlib.sha256("password".encode()).hexdigest()
        
        cur.execute("INSERT INTO masterPassword(NAME, MASTERPASSWORD) VALUES(?, ?)", (name, password))
        return cur

# Function to check the entered password against the stored master password
def cheak_password(conn):
    # Retrieve masterPassword records from the database
    sql = pd.read_sql_query("SELECT * FROM masterPassword", conn)
    df = pd.DataFrame(sql, columns=["ID", "NAME", "MASTERPASSWORD"])
    Password = df["MASTERPASSWORD"].tolist()

    # Prompt the user to enter the master password
    masterPass = input("Enter password: ")
    masterPass = hashlib.sha256(masterPass.encode()).hexdigest()

    return Password, masterPass

# Function to initialize the expense table
def intialize_expense_table(cur):
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
    return cur

# Function to initialize the income table
def intialize_income_table(cur):
    # Create the income table if it doesn't exist
    cur.execute('''
    CREATE TABLE IF NOT EXISTS income(
                ID INT PRIMARY KEY,
                TAG TEXT,
                INCOME REAL NOT NULL,
                DATE TEXT NOT NULL,
                MONTH TEXT NOT NULL,
                YEAR TEXT NOT NULL
    ) 
    ''')
    return cur

# Function to enter expenses into the database
def enter_expenses(cur, conn):
    print("Enter exit if you don't want to write anything else:")
    
    while True:
        itemName = input("Enter item name:  ")
        if itemName.lower() == 'exit':
            break            
    
        while True:
            try:
                itemPrice = float(input("Enter item price:  "))
                break

            except ValueError:
                print("Only numbers can be entered: ")
        
        itemdate = date.today().strftime('%d-%B-%Y')
        
        # Insert expense record into the expenses table
        cur.execute("INSERT INTO expenses(ITEM, PRICE, DATE, MONTH, YEAR) VALUES(?, ?, ?, ?, ?)", (itemName, itemPrice, itemdate, 0, 0))
        conn.commit()
        
        print("Successfully added.") 

# Function to delete expenses from the database
def delete_expense(conn):
    delname = input("Enter name to delete  ")

    # Deleting the info.
    conn.execute("DELETE FROM expenses WHERE ITEM = ?", (delname,))
    conn.commit()
    print("Successfully deleted.")

# Function to view expenses and income for a specific month and year
def view_expenses_and_income(conn):
    while True:
        try:
            month = int(input("Enter month (01): "))
            year = int(input("Enter year (2024): "))
            break
        except ValueError:
            print("Only numbers can be entered.")    

    # Retrieve expense records from the expenses table
    sql = pd.read_sql_query("SELECT * FROM expenses", conn)
    db = pd.DataFrame(sql, columns=['ITEM', 'PRICE', 'DATE'])
        
    # Extract month and year from the 'DATE' column
    db['MONTH'] = pd.to_datetime(db['DATE']).dt.month
    db['YEAR'] = pd.to_datetime(db['DATE']).dt.year
        
    # Filter based on month and year
    filtered_expenses = db[(db['MONTH'] == month) & (db['YEAR'] == year)]
    if not filtered_expenses.empty:
        print("Expenses:")
        print(filtered_expenses[['ITEM', 'PRICE', 'DATE']])
    
    else: 
        print("No record found in expenses.")

    # Retrieve income records from the income table
    sql = pd.read_sql_query("SELECT * FROM income", conn)
    db = pd.DataFrame(sql, columns=['TAG', 'INCOME', 'DATE'])
        
    # Extract month and year from the 'DATE' column
    db['MONTH'] = pd.to_datetime(db['DATE']).dt.month
    db['YEAR'] = pd.to_datetime(db['DATE']).dt.year

    # Filter based on month and year
    filtered_income = db[(db["MONTH"] == month) & (db['YEAR'] == year)]
    if not filtered_income.empty:    
        print("\nIncome:")  
        print(filtered_income[['TAG', 'INCOME', 'DATE']])
    
    else: 
        print("\nNo record found in income.")

# Function to check the current balance
def cheak_current_ballance(conn):
    # Calculate total expenses
    expense_df = pd.read_sql_query("SELECT * FROM expenses", conn)
    totalExpense = sum(expense_df['PRICE'].tolist())

    # Calculate total income
    income_df = pd.read_sql_query("SELECT * FROM income", conn)
    totalIncome = sum(income_df['INCOME'].tolist())
    
    # Calculate current balance
    curentBalance = totalIncome - totalExpense
    print(f"Your balance is {curentBalance}")

# Function to enter income into the database
def enter_income(cur, conn):
    tag = input("Enter a tag ")
    while True:    
        try:
            income = float(input("Enter your income "))
            break
    
        except ValueError:
            print("Only numbers can be entered.")

    curentDate = date.today().strftime('%d-%B-%Y')
    # Insert income record into the income table
    cur.execute("INSERT INTO income(TAG, INCOME, DATE, MONTH, YEAR) VALUES(?, ?, ?, ?, ?)", (tag, income, curentDate, 0, 0))
    conn.commit()
    
    print("New income successfully added")

# Function to change the master password
def change_password(cur, conn):
    cur.execute("DELETE FROM masterPassword")
    conn.commit()

    newPass = input("Enter new password:  ")
    confirmPass = input("Enter password again:  ")
    
    if newPass != confirmPass:
        print("Passwords don't match")
    else:
        name1, pass1 = "USER1", hashlib.sha256(newPass.encode()).hexdigest()
        # Insert new master password record into the masterPassword table
        cur.execute("INSERT INTO masterPassword(NAME, MASTERPASSWORD) VALUES(?, ?)", (name1, pass1))
        conn.commit()
        print("Password successfully changed.")

# Function to handle user choices for different operations
def choice(cur, conn):
    option = None
    
    while option != "exit":
        time.sleep(1)
        option = input("Enter 1 to write expenses, enter 2 to delete expenses, enter 3 to see all expenses, enter 4 to check current balance, enter 5 to write income, enter 6 to change password: \n")
        
        if option == '1':
            enter_expenses(cur, conn)

        elif option == '2':
            delete_expense(conn)
            
        elif option == '3':
            view_expenses_and_income(conn)

        elif option == '4':
            cheak_current_ballance(conn)

        elif option == '5':
            enter_income(cur, conn)

        elif option == '6':
            change_password(cur, conn)
        
        elif option == 'exit':
            break

        else: 
            print("Wrong command, please enter the command again.")

# Connect to the database and perform necessary initializations
conn, cur = connect_to_database(LOCATION)
if conn and cur:
    intialize_masterpass_table(cur)
    first_time_password(cur)
    
    Password, masterPass = cheak_password(conn)
    
    if masterPass != Password[0]:
        print("Wrong password")
        exit()
    
    intialize_expense_table(cur)
    intialize_income_table(cur)
    
    # Handle user choices
    choice(cur, conn)
