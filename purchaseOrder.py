import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3
import subprocess

def validate_string(input_text):
    return input_text.isalpha()

def validate_quantity(input_text):
    return input_text.isdigit()

def calculate_total(event=None):  # Event parameter added to handle binding
    try:
        quantity = float(quantity_entry.get())
        price = float(price_entry.get())
        total = quantity * price
        total_entry.delete(0, tk.END)
        total_entry.insert(0, f'{total:.2f}')
    except ValueError:
        total_entry.delete(0, tk.END)
        total_entry.insert(0, 'Invalid Input')


def dashboard():
    root.destroy()
    subprocess.run(["python","C:\\Users\\ACER\\IdeaProjects\\dashboard.py"])


def submit_data():
    date_value = date_entry.get()
    ref_no_value = ref_no_entry.get()
    vendor_name_value = vendor_name_entry.get()
    category_value = category_entry.get()
    quantity_value = quantity_entry.get()
    price_value = price_entry.get()
    total_value = total_entry.get()

    # Check if any input is missing
    if not all([date_value, ref_no_value, vendor_name_value, category_value, quantity_value, price_value, total_value]):
        messagebox.showerror("Error", "Fill all details")
        return

    # Validation
    if not validate_string(vendor_name_value):
        messagebox.showerror("Error", "Vendor Name should contain only letters.")
        return
    if not validate_string(category_value):
        messagebox.showerror("Error", "Category should contain only letters.")
        return
    if not validate_quantity(quantity_value):
        messagebox.showerror("Error", "Quantity should contain only numbers.")
        return
    
    conn = sqlite3.connect('data.db')
    table_create_query = '''CREATE TABLE IF NOT EXISTS PurchaseOrder_data(date_value TEXT, ref_no_value TEXT, vendor_name_value TEXT, category_value TEXT, quantity_value INT, price_value INT, total_value FLOAT)'''
    conn.execute(table_create_query)
    data_insert = '''INSERT INTO PurchaseOrder_data(date_value, ref_no_value, vendor_name_value, category_value, quantity_value, price_value, total_value) VALUES(?,?,?,?,?,?,?)'''
    data_tuple = (date_value, ref_no_value, vendor_name_value, category_value, quantity_value, price_value, total_value)
    cursor = conn.cursor()
    cursor.execute(data_insert, data_tuple)
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Purchase Order details have been inserted.")

    # Here, you can process the data as needed (e.g., store in a database).

    # For demonstration purposes, let's print the data to the console.
    # print(f"Date: {date_value}, Reference No: {ref_no_value}, Vendor Name: {vendor_name_value}, "
    #       f"Category: {category_value}, Quantity: {quantity_value}, Price: {price_value}, Total: {total_value}")

    # You can add further actions, such as saving the data to a file or database.

    # Clear the entry fields after submission
    date_entry.set_date(None)
    ref_no_entry.delete(0, tk.END)
    vendor_name_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    total_entry.delete(0, tk.END)

# Create the main window
root = tk.Tk()
root.title("Inventory Management System")
root.geometry("800x700")  # Increased height and width
 # Maximize the window

# Create a frame for the form
form_frame = ttk.Frame(root, padding=(20, 20), style="Form.TFrame")
form_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
form_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

#canvas for form frame
# border_canvas = tk.Canvas(form_frame, bg="#a58fff", width=1100, height=1200, highlightthickness=0)
# border_canvas.grid(row=0, column=0)


# Style for the form frame
style = ttk.Style(root)
style.configure("Form.TFrame", background="#E6E6FA", borderwidth=5, relief="solid", width=1500, height=1600)


# Heading label
heading_label = ttk.Label(form_frame, text="PURCHASE ORDER DETAILS", font=('Arial', 24, 'bold'), background="#4B0082",foreground="white")
heading_label.grid(row=0, column=0, columnspan=2, pady=20)

# Date Entry
date_label = ttk.Label(form_frame, text="Date:", font=('Arial', 14, 'bold'))
date_label.grid(row=1, column=0, pady=10, padx=10, sticky=tk.W)
date_entry = DateEntry(form_frame, background="white", foreground="black", borderwidth=2, date_pattern="yyyy-MM-dd")
date_entry.grid(row=1, column=1, pady=10, padx=10, sticky=tk.W)

# Reference Number Entry
ref_no_label = ttk.Label(form_frame, text="Reference No:", font=('Arial', 14, 'bold'))
ref_no_label.grid(row=2, column=0, pady=10, padx=10, sticky=tk.W)
ref_no_entry = ttk.Entry(form_frame, font=('Arial', 14))
ref_no_entry.grid(row=2, column=1, pady=10, padx=10, sticky=tk.W)

# Vendor Name Entry
vendor_name_label = ttk.Label(form_frame, text="Vendor Name:", font=('Arial', 14, 'bold'))
vendor_name_label.grid(row=3, column=0, pady=10, padx=10, sticky=tk.W)
vendor_name_entry = ttk.Entry(form_frame, font=('Arial', 14))
vendor_name_entry.grid(row=3, column=1, pady=10, padx=10, sticky=tk.W)

# Category Entry
category_label = ttk.Label(form_frame, text="Product Name:", font=('Arial', 14, 'bold'))
category_label.grid(row=4, column=0, pady=10, padx=10, sticky=tk.W)
category_entry = ttk.Entry(form_frame, font=('Arial', 14))
category_entry.grid(row=4, column=1, pady=10, padx=10, sticky=tk.W)

# Quantity Entry
quantity_label = ttk.Label(form_frame, text="Quantity:", font=('Arial', 14, 'bold'))
quantity_label.grid(row=5, column=0, pady=10, padx=10, sticky=tk.W)
quantity_entry = ttk.Entry(form_frame, font=('Arial', 14))
quantity_entry.grid(row=5, column=1, pady=10, padx=10, sticky=tk.W)

# Price Entry
price_label = ttk.Label(form_frame, text="Price:", font=('Arial', 14, 'bold'))
price_label.grid(row=6, column=0, pady=10, padx=10, sticky=tk.W)
price_entry = ttk.Entry(form_frame, font=('Arial', 14))
price_entry.grid(row=6, column=1, pady=10, padx=10, sticky=tk.W)

amount_label = ttk.Label(form_frame, text="Total Amount:", font=('Arial', 14, 'bold'))
amount_label.grid(row=7, column=0, pady=10, padx=10, sticky=tk.W)
total_entry = ttk.Entry(form_frame, font=('Arial', 14))
total_entry.grid(row=7, column=1, pady=10, padx=10, sticky=tk.W)
total_entry.bind("<FocusOut>", calculate_total)




# Submit Button
style.configure("Submit.TButton", background="#4B0082", foreground="black", font=('Arial', 20, 'bold'))
submit_button = ttk.Button(form_frame, text="Submit", command=submit_data, style="Submit.TButton")
submit_button.grid(row=8, column=0, columnspan=2, pady=15, padx=10)
back_button = ttk.Button(form_frame, text="Back", command=dashboard, style="Submit.TButton")
back_button.grid(row=8, column=2, columnspan=2, pady=15, padx=10)







# Style for the Calculate and Submit buttons
style.configure("Calculate.TButton", background="blue", foreground="black", font=('Arial', 14, 'bold'))

# Run the Tkinter

root.mainloop()