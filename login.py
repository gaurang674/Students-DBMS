import mysql.connector
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

db_config = {
    'user': 'root',
    'password': 'IluAbcde.1',
    'host': 'localhost',
    'database': 'Student'
}

try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
except mysql.connector.Error as err:
    messagebox.showerror("Error", f"Error connecting to database: {err}")


def login():
    username = "ABCDE"
    password = "12345"
    if user_entry.get() == username and password_entry.get() == password:
        switch_frame(login_frame, dashboard_frame)
    else:
        messagebox.showwarning("Error", "Invalid Username or Password!")


def switch_frame(from_frame, to_frame):
    from_frame.place_forget()  # Hide the current frame
    to_frame.place(relx=0.5, rely=0.5, anchor='center')  # Show the next frame


def insert_data():
    rollno = rollno_entry.get()
    name = name_entry.get()
    marks = marks_entry.get()

    if not rollno or not name or not marks:  # Check if any field is empty
        messagebox.showwarning("Warning", "Please fill in all fields!")
        return  # Exit the function if fields are empty

    try:
        rollno = int(rollno)  # Convert rollno to int
        marks = int(marks)  # Convert marks to int
    except ValueError:
        messagebox.showwarning("Warning", "Roll No and Marks must be integers!")
        return  # Exit the function if conversion fails

    cursor.execute("INSERT INTO students (rollno, name, marks) VALUES (%s, %s, %s)", (rollno, name, marks))
    conn.commit()
    messagebox.showinfo("Success", "Data inserted successfully!")

    # Clear the input fields
    rollno_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    marks_entry.delete(0, tk.END)


def view_data():
    for row in tree.get_children():
        tree.delete(row)

    cursor.execute("SELECT rollno, name, marks FROM students")
    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", "end", values=row)


def update_data():
    rollno = update_rollno_entry.get()
    name = update_name_entry.get()
    marks = update_marks_entry.get()

    if not rollno or not name or not marks:
        messagebox.showwarning("Warning", "Please fill in all fields!")
        return

    try:
        cursor.execute("UPDATE students SET name=%s, marks=%s WHERE rollno=%s", (name, marks, rollno))
        conn.commit()
        messagebox.showinfo("Success", "Data updated successfully!")
        view_data()  # Refresh data
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error updating data: {err}")


def delete_data():
    rollno = delete_rollno_entry.get()
    if not rollno:
        messagebox.showwarning("Warning", "Please enter a Roll No!")
        return

    try:
        cursor.execute("DELETE FROM students WHERE rollno=%s", (rollno,))
        conn.commit()
        messagebox.showinfo("Success", "Data deleted successfully!")
        view_data()  # Refresh data
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error deleting data: {err}")


window = tk.Tk()
window.title("Login Form")
window.geometry('1000x700')
window.config(bg='#1a5276')

# FRAMES
dashboard_frame = tk.Frame(window, bg='#1a5276')
login_frame = tk.Frame(window, bg='#1a5276')
insert_frame = tk.Frame(window, bg='#1a5276')
delete_frame = tk.Frame(window, bg='#1a5276')
update_frame = tk.Frame(window, bg='#1a5276')
view_frame = tk.Frame(window, bg='#1a5276')

# LOGIN FRAME
tk.Label(login_frame, text="Login", bg='#1a5276', fg='#FF7F50', font=('Arial', 30)).grid(row=0, column=0, columnspan=2, sticky='news', pady=40)

tk.Label(login_frame, text="Username", bg='#1a5276', fg='white', font=('Arial', 20)).grid(row=1, column=0)
user_entry = tk.Entry(login_frame, font=('Arial', 20))
user_entry.grid(row=1, column=1, pady=10)

tk.Label(login_frame, text="Password", bg='#1a5276', fg='white', font=('Arial', 20)).grid(row=2, column=0)
password_entry = tk.Entry(login_frame, show='*', font=('Arial', 20))
password_entry.grid(row=2, column=1, pady=10)

login_button = tk.Button(login_frame, text='Login', bg='#FF7F50', fg='white', font=('Arial', 20), command=login)
login_button.grid(row=3, column=0, columnspan=2, pady=20)

# DASHBOARD FRAME
insert_button = tk.Button(dashboard_frame, text="Insert Data", font=('Arial', 20), command=lambda: switch_frame(dashboard_frame, insert_frame))
insert_button.pack(pady=10)

delete_button = tk.Button(dashboard_frame, text="Delete Data", font=('Arial', 20), command=lambda: switch_frame(dashboard_frame, delete_frame))
delete_button.pack(pady=10)

update_button = tk.Button(dashboard_frame, text="Update Data", font=('Arial', 20), command=lambda: switch_frame(dashboard_frame, update_frame))
update_button.pack(pady=10)

view_button = tk.Button(dashboard_frame, text="View Data", font=('Arial', 20), command=lambda: switch_frame(dashboard_frame, view_frame))
view_button.pack(pady=10)

exit_button = tk.Button(dashboard_frame, text="Exit", font=('Arial', 20), command=window.quit)
exit_button.pack(pady=10)

# INSERT FRAME
tk.Label(insert_frame, text="Roll No. ", bg='#1a5276', fg='#FF7F50', font=('Arial', 30)).grid(row=0, column=0)
rollno_entry = tk.Entry(insert_frame, font=('Arial', 30))
rollno_entry.grid(row=0, column=1)

tk.Label(insert_frame, text="Name ", bg='#1a5276', fg='#FF7F50', font=('Arial', 30)).grid(row=1, column=0)
name_entry = tk.Entry(insert_frame, font=('Arial', 30))
name_entry.grid(row=1, column=1)

tk.Label(insert_frame, text="Marks ", bg='#1a5276', fg='#FF7F50', font=('Arial', 30)).grid(row=2, column=0)
marks_entry = tk.Entry(insert_frame, font=('Arial', 30))
marks_entry.grid(row=2, column=1)

submit_button = tk.Button(insert_frame, text='Submit', bg='#FF7F50', fg='white', font=('Arial', 20), command=insert_data)
submit_button.grid(row=3, column=0)

back_button = tk.Button(insert_frame, text='Back', bg='#FF7F50', fg='white', font=('Arial', 20), command=lambda: switch_frame(insert_frame, dashboard_frame))
back_button.grid(row=3, column=1)

# UPDATE FRAME
tk.Label(update_frame, text="Roll No. to update ", bg='#1a5276', fg='#FF7F50', font=('Arial', 30)).pack(pady=5)
update_rollno_entry = tk.Entry(update_frame, font=('Arial', 30))
update_rollno_entry.pack(pady=5)

tk.Label(update_frame, text="Updated Name ", bg='#1a5276', fg='#FF7F50', font=('Arial', 30)).pack(pady=5)
update_name_entry = tk.Entry(update_frame, font=('Arial', 30))
update_name_entry.pack(pady=5)

tk.Label(update_frame, text="Updated Marks ", bg='#1a5276', fg='#FF7F50', font=('Arial', 30)).pack(pady=5)
update_marks_entry = tk.Entry(update_frame, font=('Arial', 30))
update_marks_entry.pack(pady=5)

update_button = tk.Button(update_frame, text='Update', bg='#FF7F50', fg='white', font=('Arial', 20), command=update_data)
update_button.pack(pady=20)

back_button_update = tk.Button(update_frame, text='Back', bg='#FF7F50', fg='white', font=('Arial', 20), command=lambda: switch_frame(update_frame, dashboard_frame))
back_button_update.pack(pady=20)

# DELETE FRAME
tk.Label(delete_frame, text="Roll No.", bg='#1a5276', fg='#FF7F50', font=('Arial', 30)).pack(pady=5)
delete_rollno_entry = tk.Entry(delete_frame, font=('Arial', 30))
delete_rollno_entry.pack(pady=5)

delete_button = tk.Button(delete_frame, text='Delete', bg='#FF7F50', fg='white', font=('Arial', 20), command=delete_data)
delete_button.pack(pady=20)

back_button_delete = tk.Button(delete_frame, text='Back', bg='#FF7F50', fg='white', font=('Arial', 20), command=lambda: switch_frame(delete_frame, dashboard_frame))
back_button_delete.pack(pady=20)

# VIEW FRAME
columns = ("Roll No", "Name", "Marks")
tree = ttk.Treeview(view_frame, columns=columns, show='headings', height=10)
tree.heading("Roll No", text="Roll No")
tree.heading("Name", text="Name")
tree.heading("Marks", text="Marks")
tree.pack(pady=20)

view_button = tk.Button(view_frame, text="Refresh Data", font=('Arial', 20), command=view_data)
view_button.pack(pady=20)

back_button_view = tk.Button(view_frame, text="Back", font=('Arial', 20), command=lambda: switch_frame(view_frame, dashboard_frame))
back_button_view.pack(pady=20)

# Start with the login frame
login_frame.place(relx=0.5, rely=0.5, anchor='center')

window.mainloop()