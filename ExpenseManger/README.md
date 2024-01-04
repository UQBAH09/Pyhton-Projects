# Expense Manager

This Python script serves as a basic Expense Manager using an SQLite database to store and manage expenses and income. It provides functionalities such as recording expenses, deleting expenses, viewing expenses and income, checking the current balance, adding income, and changing the master password.

## Setup

Before running the script, make sure to install the required libraries:

```bash
pip install pandas
```

## Usage

1. **Setting up the Database**
   - The SQLite database is located at `/home/uqbah/Python/ExpenseManger/DataBase.db`. Update the `location` variable if needed.

2. **Master Password**
   - A default user ("USER1") with the password "password" is created if no records exist in the `masterPassword` table. You can change the default password later.

3. **Expenses and Income**
   - The script allows you to record expenses and income, view them based on month and year, and check the current balance.

4. **Changing Master Password**
   - You can change the master password by selecting option 6 and following the prompts.

## Dependencies

- [sqlite3](https://docs.python.org/3/library/sqlite3.html)
- [pandas](https://pandas.pydata.org/)
- [hashlib](https://docs.python.org/3/library/hashlib.html)
- [datetime](https://docs.python.org/3/library/datetime.html)
- [time](https://docs.python.org/3/library/time.html)

## Running the Script

Run the script and follow the on-screen prompts to interact with the Expense Manager.

```bash
python expense_manager.py
```

**Note:** This script is a basic example and may require additional enhancements and error handling for production use.
