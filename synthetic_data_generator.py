import sqlite3
import random
from datetime import datetime, timedelta

def generate_unique_name(existing_names, length=6):
    """
    Generates a unique, pronounceable name not in the existing_names set.
    """
    vowels = "aeiou"
    consonants = "bcdfghjklmnpqrstvwxyz"
    while True:
        name = "".join(
            random.choice(consonants) if i % 2 == 0 else random.choice(vowels)
            for i in range(length)
        ).capitalize()
        if name not in existing_names:
            existing_names.add(name)
            return name

def generate_names(num_names):
    """
    Generates a set of unique first and last name pairs.
    """
    existing_names = set()
    first_last_names = []
    for _ in range(num_names):
        first_name = generate_unique_name(existing_names, length=random.randint(4, 8))
        last_name = generate_unique_name(existing_names, length=random.randint(4, 8))
        first_last_names.append((first_name, last_name))
    return first_last_names

def create_table(db_path, table_name):
    """
    Creates a table with the given name if it does not exist.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        salary TEXT,
        hire_date TEXT
    )
    """)
    conn.commit()
    conn.close()
    print(f"Table '{table_name}' is ready.")

def generate_random_hire_date(start_date="2000-01-01", end_date=None):
    """
    Generates a random hire date between start_date and end_date.
    """
    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    random_days = random.randint(0, (end - start).days)
    random_date = start + timedelta(days=random_days)
    return random_date.strftime("%m/%d/%Y")  # MM/DD/YYYY format

def generate_data(db_path, table_name, num_records=100, wipe_data=False):
    """
    Generates synthetic data for the given table and optionally wipes existing data.
    Default is to generate 100 records if num_records is not specified.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    if wipe_data:
        cursor.execute(f"DELETE FROM {table_name}")
        conn.commit()
        print(f"Existing data in table '{table_name}' has been wiped.")
        cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table_name}'")
        conn.commit()
        print(f"Identity column for table '{table_name}' has been reset.")

    names = generate_names(num_records)

    for first_name, last_name in names:
        name = f"{first_name} {last_name}"
        age = random.randint(18, 65)
        salary = f"${random.randint(30000, 150000):,}"  # Format salary
        hire_date = generate_random_hire_date()

        cursor.execute(
            f"""
            INSERT INTO {table_name} (name, age, salary, hire_date)
            VALUES (?, ?, ?, ?)
            """, (name, age, salary, hire_date)
        )

    conn.commit()
    print(f"{num_records} records inserted into table '{table_name}'.")

    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]

    print(f"\nData in table '{table_name}':")
    if rows:
        print(format_table(column_names, rows))
    else:
        print("No data found in the table.")

    conn.close()

def format_table(column_names, rows):
    """
    Formats the table output with aligned columns.
    """
    col_widths = [max(len(str(item)) for item in col) for col in zip(column_names, *rows)]
    row_format = " | ".join(f"{{:<{width}}}" for width in col_widths)
    separator = "-+-".join("-" * width for width in col_widths)

    formatted_output = []
    formatted_output.append(row_format.format(*column_names))
    formatted_output.append(separator)
    for row in rows:
        formatted_output.append(row_format.format(*row))
    return "\n".join(formatted_output)

# Usage Example
if __name__ == "__main__":
    db_path = "C:\GitHub\Virtusa-PoC\example.db"
    table_name = "employees"

    # Ask user for the number of records to generate
    try:
        user_input = input("Enter the number of records to generate (default 100): ")
        num_records = int(user_input) if user_input.strip() else 100
    except ValueError:
        print("Invalid input, defaulting to 100 records.")
        num_records = 100

    wipe_data = True

    create_table(db_path, table_name)
    generate_data(db_path, table_name, num_records, wipe_data)
