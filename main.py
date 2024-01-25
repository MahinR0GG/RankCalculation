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

# Grade thresholds
grade_thresholds = {'A+': 450, 'A': 400, 'B+': 350, 'B': 300, 'C+': 250, 'C': 200, 'D': 150, 'E': 100, 'F': 50}

# Function to fetch student data from the database
def fetch_student_data(roll_number):
    query = f"SELECT * FROM student WHERE ROLL_NO = {roll_number}"
    cursor.execute(query)
    result = cursor.fetchone()
    return result

# Function to calculate rank and grade based on total marks
def calculate_rank_and_grade_from_db(roll_number):
    try:
        # Fetch the student data from the database
        student = fetch_student_data(roll_number)

        if student:
            # Calculate total marks for the current student
            total_marks = sum(student[2:6])  # Assuming the columns DS, MATH, PYTHON, CN are 2nd to 5th columns

            # Count the number of students with higher total marks
            query_higher_ranks = f"SELECT COUNT(*) FROM student WHERE (DS + MATHS + PYTHON + CN) > {total_marks}"
            cursor.execute(query_higher_ranks)
            higher_ranks_count = cursor.fetchone()[0]

            # Calculate the rank by adding 1 to the count of higher ranks
            rank = higher_ranks_count + 1

            # Determine grade based on total marks
            for grade, threshold in grade_thresholds.items():
                if total_marks >= threshold:
                    student_grade = grade
                    break
            else:
                student_grade = 'F'

            # Display the result
            messagebox.showinfo("Result",
                                f"Roll Number: {roll_number}\nName: {student[1]}\nTotal Marks: {total_marks}\nRank: {rank}\nGrade: {student_grade}")

        else:
            messagebox.showerror("Error", "Roll number not found!")

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error accessing the database: {str(e)}")

    # Clear the entry after execution
    entry_roll.delete(0, tk.END)

# Function to handle button click event
def on_submit():
    roll_number = entry_roll.get()
    calculate_rank_and_grade_from_db(roll_number)

# Tkinter GUI setup
root = tk.Tk()
root.title("Ranking System")
root.configure(bg="#E6E6FA")  # Set the background color of the window

# Set the size of the window
root.geometry("400x200")

# Label and Entry for Roll Number
label_roll = tk.Label(root, text="Enter Roll Number (10X format):", bg="#E6E6FA")  # Set label background color
label_roll.pack()

entry_roll = tk.Entry(root)
entry_roll.pack()

# Button to submit
submit_button = tk.Button(root, text="Submit", command=on_submit, bg="#4CAF50", fg="white")  # Set button color
submit_button.pack()

# Run the Tkinter event loop
root.mainloop()

# Close the database connection when the Tkinter window is closed
conn.close()
