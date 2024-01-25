import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Connect to MySQL database (replace 'your_host', 'your_user', 'your_password', and 'your_database' with your actual MySQL credentials)
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='student'
)
cursor = conn.cursor()

# Function to insert student data into the database
def insert_student_data(roll_number, name, ds, maths, python, cn):
    try:
        # Check if the roll number already exists
        query_check_roll = "SELECT * FROM student WHERE ROLL_NO = %s"
        cursor.execute(query_check_roll, (roll_number,))
        existing_student = cursor.fetchone()

        if existing_student:
            messagebox.showerror("Error", f"Roll Number {roll_number} already exists!")
        else:
            # Calculate total marks
            total = ds + maths + python + cn

            # Insert data into the 'student' table
            query = "INSERT INTO student (ROLL_NO, NAME, DS, MATHS, PYTHON, CN, TOTAL) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            data = (roll_number, name, ds, maths, python, cn, total)
            cursor.execute(query, data)
            conn.commit()

            # Show a messagebox confirming data entry
            messagebox.showinfo("Success", "Student data entered successfully!")

            # Clear the entry fields
            entry_roll.delete(0, tk.END)
            entry_name.delete(0, tk.END)
            entry_ds.delete(0, tk.END)
            entry_maths.delete(0, tk.END)
            entry_python.delete(0, tk.END)
            entry_cn.delete(0, tk.END)

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error inserting data into the database: {str(e)}")

# Function to handle button click event
def on_submit():
    try:
        # Get data from user input
        roll_number = int(entry_roll.get())
        name = entry_name.get()
        ds = int(entry_ds.get())
        maths = int(entry_maths.get())
        python = int(entry_python.get())
        cn = int(entry_cn.get())

        # Insert data into the database
        insert_student_data(roll_number, name, ds, maths, python, cn)

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numerical values for marks and roll number.")

# Tkinter GUI setup
root = tk.Tk()
root.title("Student Data Entry")
root.configure(bg="#F0F0F0")  # Set the background color of the window

# Set the size of the window
root.geometry("600x400")

# Labels and Entry widgets for student details
label_roll = tk.Label(root, text="Roll Number:", bg="#F0F0F0")  # Set label background color
label_roll.pack()

entry_roll = tk.Entry(root)
entry_roll.pack()

label_name = tk.Label(root, text="Name:", bg="#F0F0F0")
label_name.pack()

entry_name = tk.Entry(root)
entry_name.pack()

label_ds = tk.Label(root, text="DS Marks:", bg="#F0F0F0")
label_ds.pack()

entry_ds = tk.Entry(root)
entry_ds.pack()

label_maths = tk.Label(root, text="Maths Marks:", bg="#F0F0F0")
label_maths.pack()

entry_maths = tk.Entry(root)
entry_maths.pack()

label_python = tk.Label(root, text="Python Marks:", bg="#F0F0F0")
label_python.pack()

entry_python = tk.Entry(root)
entry_python.pack()

label_cn = tk.Label(root, text="CN Marks:", bg="#F0F0F0")
label_cn.pack()

entry_cn = tk.Entry(root)
entry_cn.pack()

# Button to submit
submit_button = tk.Button(root, text="Submit", command=on_submit, bg="#4CAF50", fg="white")  # Set button color
submit_button.pack()

# Run the Tkinter event loop
root.mainloop()

# Close the database connection when the Tkinter window is closed
conn.close()