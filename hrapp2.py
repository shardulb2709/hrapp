import psycopg2
import tkinter as tk
from tkinter import ttk, messagebox
# Database Connection Configuration (Replace with your Azure PostgreSQL details)
DB_CONFIG = {
   "dbname": "postgres",
   "user": "shardul",
   "password": "Admin@1234",
   "host": "pgfs3n.postgres.database.azure.com",
   "port": "5432",
      # Ensures secure connection
}
# Connect to PostgreSQL
def connect_db():
   try:
       return psycopg2.connect(**DB_CONFIG)
   except Exception as e:
       messagebox.showerror("Database Error", f"Error connecting to database: {e}")
       return None
# Insert Employee
def insert_employee():
   conn = connect_db()
   if conn:
       try:
           cursor = conn.cursor()
           emp_id = emp_id_var.get()
           emp_name = emp_name_var.get()
           salary = salary_var.get()
           department = dept_var.get()
           if emp_name and salary and department:
               cursor.execute("INSERT INTO employees (emp_name, salary, department) VALUES (%s, %s, %s) RETURNING emp_id",
                              (emp_name, salary, department))
               conn.commit()
               messagebox.showinfo("Success", "Employee inserted successfully!")
               clear_fields()
           else:
               messagebox.showwarning("Input Error", "All fields are required!")
       except Exception as e:
           messagebox.showerror("Error", f"Error inserting employee: {e}")
       finally:
           conn.close()
# Update Employee
def update_employee():
   conn = connect_db()
   if conn:
       try:
           cursor = conn.cursor()
           emp_id = emp_id_var.get()
           emp_name = emp_name_var.get()
           salary = salary_var.get()
           department = dept_var.get()
           if emp_id and emp_name and salary and department:
               cursor.execute("UPDATE employees SET emp_name=%s, salary=%s, department=%s WHERE emp_id=%s",
                              (emp_name, salary, department, emp_id))
               conn.commit()
               messagebox.showinfo("Success", "Employee updated successfully!")
               clear_fields()
           else:
               messagebox.showwarning("Input Error", "All fields are required!")
       except Exception as e:
           messagebox.showerror("Error", f"Error updating employee: {e}")
       finally:
           conn.close()
# Delete Employee
def delete_employee():
   conn = connect_db()
   if conn:
       try:
           cursor = conn.cursor()
           emp_id = emp_id_var.get()
           if emp_id:
               cursor.execute("DELETE FROM employees WHERE emp_id=%s", (emp_id,))
               conn.commit()
               messagebox.showinfo("Success", "Employee deleted successfully!")
               clear_fields()
           else:
               messagebox.showwarning("Input Error", "Employee ID is required!")
       except Exception as e:
           messagebox.showerror("Error", f"Error deleting employee: {e}")
       finally:
           conn.close()
# Find Employee by Name
def find_employee():
   conn = connect_db()
   if conn:
       try:
           cursor = conn.cursor()
           search_name = search_var.get()
           if search_name:
               cursor.execute("SELECT * FROM employees WHERE emp_name ILIKE %s", ('%' + search_name + '%',))
               results = cursor.fetchall()
               # Clear previous search results
               for row in search_tree.get_children():
                   search_tree.delete(row)
               for emp in results:
                   search_tree.insert("", "end", values=emp)
           else:
               messagebox.showwarning("Input Error", "Enter a name to search!")
       except Exception as e:
           messagebox.showerror("Error", f"Error finding employee: {e}")
       finally:
           conn.close()
# Clear Input Fields
def clear_fields():
   emp_id_var.set("")
   emp_name_var.set("")
   salary_var.set("")
   dept_var.set("")
   search_var.set("")
# Create Tkinter App
root = tk.Tk()
root.title("HR Management App (Azure PostgreSQL)")
root.geometry("600x400")
# Create Notebook (Tabs)
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")
# Tab 1 - Employee Management
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="Manage Employees")
emp_id_var = tk.StringVar()
emp_name_var = tk.StringVar()
salary_var = tk.StringVar()
dept_var = tk.StringVar()
# Labels and Entry Fields
ttk.Label(tab1, text="Emp ID:").grid(row=0, column=0, padx=5, pady=5)
ttk.Entry(tab1, textvariable=emp_id_var).grid(row=0, column=1, padx=5, pady=5)
ttk.Label(tab1, text="Emp Name:").grid(row=1, column=0, padx=5, pady=5)
ttk.Entry(tab1, textvariable=emp_name_var).grid(row=1, column=1, padx=5, pady=5)
ttk.Label(tab1, text="Salary:").grid(row=2, column=0, padx=5, pady=5)
ttk.Entry(tab1, textvariable=salary_var).grid(row=2, column=1, padx=5, pady=5)
ttk.Label(tab1, text="Department:").grid(row=3, column=0, padx=5, pady=5)
ttk.Entry(tab1, textvariable=dept_var).grid(row=3, column=1, padx=5, pady=5)
# Buttons
ttk.Button(tab1, text="Insert", command=insert_employee).grid(row=4, column=0, padx=5, pady=5)
ttk.Button(tab1, text="Update", command=update_employee).grid(row=4, column=1, padx=5, pady=5)
ttk.Button(tab1, text="Delete", command=delete_employee).grid(row=5, column=0, padx=5, pady=5)
ttk.Button(tab1, text="Clear", command=clear_fields).grid(row=5, column=1, padx=5, pady=5)
# Tab 2 - Search Employee   
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="Find Employee")
search_var = tk.StringVar()
ttk.Label(tab2, text="Search by Name:").grid(row=0, column=0, padx=5, pady=5)
ttk.Entry(tab2, textvariable=search_var).grid(row=0, column=1, padx=5, pady=5)
ttk.Button(tab2, text="Find", command=find_employee).grid(row=0, column=2, padx=5, pady=5,sticky="w")

tab2.grid_columnconfigure(0, weight=1)
tab2.grid_columnconfigure(1, weight=1)
tab2.grid_columnconfigure(2, weight=1)
# Search Results Treeview   
search_tree = ttk.Treeview(tab2, columns=("ID", "Name", "Salary", "Department"), show="headings")
search_tree.heading("ID", text="Emp ID")
search_tree.heading("Name", text="Emp Name")
search_tree.heading("Salary", text="Salary")
search_tree.heading("Department", text="Department")
search_tree.grid(row=1, column=0, columnspan=3, padx=5, pady=5,sticky="nsew")
# Run the Tkinter App
root.mainloop()