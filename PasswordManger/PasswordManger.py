# Import necessary libraries
import sqlite3
import pandas as pd
import hashlib
import time

# Starting connection to a database
db_conn = "/home/uqbah/Python/PasswordManger/PasswordOraganizer.db"
conn = None
cur = None

try:
    # Attempting to connect to the SQLite database
    conn = sqlite3.connect(db_conn)
    cur = conn.cursor()
except sqlite3.Error as e:
    # Handling SQLite connection errors
    print(f"SQLite error: \n {e}")
finally:
    # Closing the cursor if it exists
    if cur:
        cur.close()

# Creating a table to store the master password to access all usernames and passwords.
cur.execute('''
CREATE TABLE IF NOT EXISTS master_password (
            ID INT PRIMARY KEY,
            name STR NOT NULL,
            password STR NOT NULL
)
''')
conn.commit()

# Checking for any previous password.
cur.execute("SELECT COUNT(*) FROM master_password")
result = cur.fetchone()
if result[0] == 0:
    # Adding a default password for the first time.
    name1, pass1 = "UQBAH", hashlib.sha256("password".encode()).hexdigest()
    conn.execute("INSERT INTO master_password (name, password) VALUES (?, ?)", (name1, pass1))
    conn.commit()

# Storing all the data for representation through the pandas library.
sql = pd.read_sql_query("SELECT * FROM master_password", conn)
df = pd.DataFrame(sql, columns=['ID', 'name', 'password'])
master_password = df['password'].tolist()

# Asking the user for the password to continue.
password = input("Enter Master Password to continue:  ")
password = hashlib.sha256(password.encode()).hexdigest()

# Checking the password.
if master_password[0] != password:
    # Handling incorrect master password
    print("Wrong password, can't enter.")
    exit()

# Creating a table to store usernames and passwords of different sites.
cur.execute('''
CREATE TABLE IF NOT EXISTS passwords (
            NAME STR PRIMARY KEY,
            USERNAME STR,
            PASSWORD STR NOT NULL
)
''')

# Storing all the data for representation through the pandas library.
sql = pd.read_sql_query("SELECT * FROM passwords", conn)
df = pd.DataFrame(sql, columns=['NAME', 'USERNAME', 'PASSWORD'])

# Main loop for interacting with the password manager
option = 0
while option != "exit":
    # Asking the user to make a choice.
    option = input("Enter number '1' for searching, '2' for adding, 3 for deletion, 4 for inspection, 5 to change password. Enter 'exit' to exit the program.\n")

    if option == "1":   # Searching
        time.sleep(1)   # Waiting for a second
        # Saving all data via pandas for displaying.
        sql = pd.read_sql_query("SELECT * FROM passwords", conn)
        df = pd.DataFrame(sql, columns=['NAME', 'USERNAME', 'PASSWORD'])

        keyword = input("Enter keyword to search\n")    # Keyword for searching.
        # Searching for a keyword (variable) in the name column.
        result_df = df[df["NAME"].str.contains(keyword)]
        if not result_df.empty:
            print(result_df)
        else:
            print("No record found.")

    elif option == "2": # Adding
        time.sleep(1)   # Waiting for a second
        # Basic information for a new entry.
        name = input("Name:  ")
        username = input("Username:  ")
        password = input("Password:  ")

        # Inserting the info.
        cur.execute("INSERT INTO passwords (NAME, USERNAME, PASSWORD) VALUES (?, ?, ?)", (name, username, password))
        conn.commit()

        # Saving it via pandas.
        sql = pd.read_sql_query("SELECT * FROM passwords", conn)
        df = pd.DataFrame(sql, columns=['NAME', 'USERNAME', 'PASSWORD'])
        print("Successfully added.")

    elif option == "3": # Deletion
        time.sleep(1)   # Waiting for a second
        delname = input("Enter name to delete  ")

        # Deleting the info.
        conn.execute("DELETE FROM passwords WHERE NAME=?", (delname,))
        conn.commit()

        # Saving it via pandas.
        sql = pd.read_sql_query("SELECT * FROM passwords", conn)
        df = pd.DataFrame(sql, columns=['NAME', 'USERNAME', 'PASSWORD'])
        print("Successfully deleted.")

    elif option == "4": # Inspecting.
        time.sleep(1)   # Waiting for a second
        # Saving all data via pandas for displaying.
        sql = pd.read_sql_query("SELECT * FROM passwords", conn)
        df = pd.DataFrame(sql, columns=['NAME', 'USERNAME', 'PASSWORD'])
        if not df.empty():
            print(df)
        else:
            print("NO records found")

    elif option == '5': # Change password.
        time.sleep(1)   # Waiting for a second
        # Deleting the old password.
        conn.execute("DELETE FROM master_password WHERE NAME=?", ('UQBAH',))
        conn.commit()
        # Adding a new password.
        new_password = input("Enter a new password.\n")
        name1, pass1 = "UQBAH", hashlib.sha256(new_password.encode()).hexdigest()
        conn.execute("INSERT INTO master_password (name, password) VALUES (?, ?)", (name1, pass1))
        conn.commit()

        # Saving it via pandas.
        sql = pd.read_sql_query("SELECT * FROM master_password", conn)
        df = pd.DataFrame(sql, columns=['NAME', 'USERNAME', 'PASSWORD'])
        print("New password confirmed.")

    else:
        print("Command not found. Enter a number from 1 to 5 or write 'exit' to exit the program.")
