import sqlite3

def create_table():
    connection = sqlite3.connect("school.db")
    cursor = connection.cursor()

    # Create the Students table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Students (
            RollNo INTEGER PRIMARY KEY,
            Name TEXT,
            Subject TEXT,
            Marks INTEGER
        )
    ''')

    connection.commit()
    connection.close()

def insert_data(roll_no, name, subject, marks):
    connection = sqlite3.connect("school.db")
    cursor = connection.cursor()

    cursor.execute('''
        INSERT INTO Students (RollNo, Name, Subject, Marks)
        VALUES (?, ?, ?, ?)
    ''', (roll_no, name, subject, marks))

    connection.commit()
    connection.close()

def main():
    create_table()

    # Example data
    data = [
        (101, "John Doe", "Math", 90),
        (102, "Jane Smith", "Science", 85),
        # Add more data as needed
    ]

    for entry in data:
        insert_data(*entry)

    print("Data inserted successfully.")

if _name_ == "_main_":
    main()