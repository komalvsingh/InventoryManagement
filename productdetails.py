import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import *
import sqlite3
import os
import openpyxl
import subprocess

def submit_form():
    product_name = entry_product_name.get()
    description = entry_description.get("1.0", tk.END)
    stock_value = entry_stock_value.get()
    sales_month = entry_sales_month.get()
    sales_year = entry_sales_year.get()
    selected_year = year_var.get()
    selected_supplier = supplier_var.get()
    
    # Process the form data as needed
    # print("Product Name:", product_name)
    # print("Description:", description)
    # print("Stock Value:", stock_value)
    # print("Sales per Month:", sales_month)
    # print("Sales per Year:", sales_year)
    # print("Selected Year:", selected_year)
    # print("Selected Supplier:", selected_supplier)

    conn = sqlite3.connect('data.db')
    table_create_query = '''CREATE TABLE IF NOT EXISTS Product_data(product_name TEXT, description TEXT, stock_value INT, sales_month INT, sales_year INT, selected_year INT, selected_supplier TEXT)'''
    conn.execute(table_create_query)
    data_insert = '''INSERT INTO Product_data(product_name,description,stock_value,sales_month,sales_year,selected_year,selected_supplier) VALUES(?,?,?,?,?,?,?)'''
    data_tuple = (product_name, description, stock_value, sales_month, sales_year, selected_year, selected_supplier)
    cursor = conn.cursor()
    cursor.execute(data_insert, data_tuple)
    conn.commit()
    conn.close()
    show()

    # Display a message box after successful insertion
    messagebox.showinfo("Success", "Product details have been inserted.")

    # Clear the form fields
    entry_product_name.delete(0, tk.END)
    entry_description.delete("1.0", tk.END)
    entry_stock_value.delete(0, tk.END)
    entry_sales_month.delete(0, tk.END)
    entry_sales_year.delete(0, tk.END)
    year_combobox.current(0)
    supplier_combobox.current(0)


    filepath = "C:\\Users\\ACER\\IdeaProjects\\exceldata.xlsx"

    if not os.path.exists(filepath):
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        heading = ["Product Name","Description","Stock Value","Sales per Month","Sales per Year","Year","Supplier"]
        sheet.append(heading)
        workbook.save(filepath)
    workbook = openpyxl.load_workbook(filepath)
    sheet = workbook.active
    sheet.append([product_name, description, stock_value, sales_month, sales_year, selected_year, selected_supplier])
    workbook.save(filepath)


def get_data(ev):
    selected_item = tree_table.selection()[0]  # Get the selected item
    values = tree_table.item(selected_item, 'values')
    
    entry_product_name.delete(0, END)
    entry_product_name.insert(0, values[0])
    
    entry_description.delete('1.0', END)
    entry_description.insert('1.0', values[1])
    
    entry_stock_value.delete(0, END)
    entry_stock_value.insert(0, values[2])
    
    entry_sales_month.delete(0, END)
    entry_sales_month.insert(0, values[3])
    
    entry_sales_year.delete(0, END)
    entry_sales_year.insert(0, values[4])
    
    year_var.set(values[5])  
    supplier_var.set(values[6])




def show():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    try:
        cursor.execute("Select * from Product_data")
        rows = cursor.fetchall()
        tree_table.delete(*tree_table.get_children())
        for row in rows:
            tree_table.insert('',END,values=row)
    except Exception as ex:
        messagebox.showerror("Error",f"Error due to: {str(ex)}")         




def dashboard():
    root.destroy()
    subprocess.run(["python","C:\\Users\\ACER\\IdeaProjects\\dashboard.py"])


def populate_suppliers():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM supplier")
    suppliers = [row[0] for row in cursor.fetchall()]
    conn.close()
    supplier_combobox['values'] = suppliers    


def select_record():
        #select the record and row
        selected = tree_table.focus()
        content = tree_table.item(selected)
        row = content['values']

        #clear the entry boxes
        clear()


        #insert in the entry boxes
        entry_product_name.insert(0, row[0])
        entry_description.insert(0, row[1])
        entry_stock_value.insert(0, row[2])
        entry_sales_month.insert(0,row[3])
        entry_sales_year.insert(0,row[4])
        year_var.insert(0,row[5])
        supplier_var.insert(END,row[6])

def query_db():
    con = sqlite3.connect('data.db')
    c = con.cursor()

    # Clear existing data from the treeview
    tree_table.delete(*tree_table.get_children())

    c.execute("SELECT * FROM Product_data")
    records = c.fetchall()

    for idx, row in enumerate(records, start=1):
        tags = 'evenrow' if idx % 2 == 0 else 'oddrow'
        tree_table.insert(parent='', index='end', iid=idx, text='', values=row, tags=(tags,))

    con.close()


# GUI
root = tk.Tk()
root.title("Product Information Form")
root.geometry("1350x700")
root.state('zoomed')

# Styling
root.configure(bg="#4B0082")  # Lightest purple background color

main_frame = ttk.Frame(root, padding=(20, 20, 20, 20), style="Main.TFrame", borderwidth=2, relief="solid")
main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

label_detail = ttk.Label(main_frame,text="Product Details",font=('Microsoft YaHei UI Bold', 28, 'bold'),foreground="black",background="#E6E6FA")
label_detail.pack(anchor="w", pady=5)
# Product Name
label_product_name = ttk.Label(main_frame, text="Product Name:", font=('Microsoft YaHei UI Light', 15))
label_product_name.pack(anchor="w", pady=5)
entry_product_name = ttk.Entry(main_frame, width=60)
entry_product_name.pack(anchor="w", pady=5)

# Description
label_description = ttk.Label(main_frame, text="Description:", font=('Microsoft YaHei UI Light', 15))
label_description.pack(anchor="w", pady=5)
entry_description = tk.Text(main_frame, width=60, height=6)
entry_description.pack(anchor="w", pady=5)

# Stock Value
label_stock_value = ttk.Label(main_frame, text="Stock Value:", font=('Microsoft YaHei UI Light', 15))
label_stock_value.pack(anchor="w", pady=5)
entry_stock_value = ttk.Entry(main_frame, width=60)
entry_stock_value.pack(anchor="w", pady=5)

# Sales per Month
label_sales_month = ttk.Label(main_frame, text="Sales per Month:", font=('Microsoft YaHei UI Light', 15))
label_sales_month.pack(anchor="w", pady=5)
entry_sales_month = ttk.Entry(main_frame, width=60)
entry_sales_month.pack(anchor="w", pady=5)

# Sales per Year
label_sales_year = ttk.Label(main_frame, text="Sales per Year:", font=('Microsoft YaHei UI Light', 15))
label_sales_year.pack(anchor="w", pady=5)
entry_sales_year = ttk.Entry(main_frame, width=60)
entry_sales_year.pack(anchor="w", pady=5)

# Year (Dropdown)
label_year = ttk.Label(main_frame, text="Year:", font=('Microsoft YaHei UI Light', 15))
label_year.pack(anchor="w", pady=5)
year_var = tk.StringVar()
year_combobox = ttk.Combobox(main_frame, textvariable=year_var, values=[2021, 2022, 2023, 2024], state="readonly", width=57)
year_combobox.pack(anchor="w", pady=5)
year_combobox.current(0)

# Supplier (Dropdown)
label_supplier = ttk.Label(main_frame, text="Supplier:", font=('Microsoft YaHei UI Light', 15))
label_supplier.pack(anchor="w", pady=5)
supplier_var = tk.StringVar()
supplier_combobox = ttk.Combobox(main_frame, textvariable=supplier_var, state="readonly", width=57,values=["Select"])
supplier_combobox.pack(anchor="w", pady=5)
supplier_combobox.current(0)
populate_suppliers()

var_searchtxt = StringVar()
var_searchby = StringVar()
search_frame = Frame(root, width= 555, height=100, bg='#fff', border=1)
search_frame.place(x=680, y=120)
search_header = Label(search_frame, text="What are you looking for?", bg='#fff', fg='black', font=('Microsoft YaHei UI bold', 13))
txt_search = Entry(search_frame, textvariable=var_searchtxt, width= 25, font=('Microsoft YaHei UI Light', 13), bg='#F1EAFF')
txt_search.place(x=20, y= 40)

cmb_box = ttk.Combobox(search_frame, textvariable=var_searchby, width=13, values=("Select","product_name", "selected_year"), state='readonly',font=('Microsoft YaHei UI light', 13))
cmb_box.place(x=270, y=40)
cmb_box.current(0)


sup_table_frame = ttk.Frame(root,width=500, height=400)
sup_table_frame.place(x=680, y=290)

tree_scroll_x = ttk.Scrollbar(sup_table_frame, orient=HORIZONTAL)
tree_scroll_y = ttk.Scrollbar(sup_table_frame, orient=VERTICAL)

tree_table = ttk.Treeview(sup_table_frame,yscrollcommand=tree_scroll_y.set,xscrollcommand=tree_scroll_x.set, selectmode="extended")
tree_scroll_y.pack(side=RIGHT, fill=Y)
tree_scroll_x.pack(side=BOTTOM, fill=X)
tree_scroll_x.config(command=tree_table.xview)
tree_scroll_y.config(command=tree_table.yview)
tree_table.pack()


tree_table["columns"] = ('productname', 'description', 'stockvalue', 'salespermonth','salesperyear','year','supplier')
tree_table.column("#0", width=0,stretch=NO)
tree_table.column("productname", anchor=W, width=100)
tree_table.column("description", anchor=W, width=100)
tree_table.column("stockvalue", anchor=W, width=100)
tree_table.column("salespermonth", anchor=W,width=100)
tree_table.column("salesperyear", anchor=W,width=100)
tree_table.column("year", anchor=W,width=100)
tree_table.column("supplier", anchor=W,width=100)
tree_table.bind("<ButtonRelease-1>", get_data)
tree_table.tag_configure('oddrow', background='white')
tree_table.tag_configure('evenrow', background='#F1EAFF')

tree_table.heading("productname", anchor=W, text="Product Name")
tree_table.heading("description", anchor=W, text="Description")
tree_table.heading("stockvalue", anchor=W, text="Stock Value")
tree_table.heading("salespermonth", anchor=W, text="Sales per Month")
tree_table.heading("salesperyear", anchor=W, text="Sales per Year")
tree_table.heading("year", anchor=W, text="Year")
tree_table.heading("supplier", anchor=W, text="Suppliers")

conn = sqlite3.connect('data.db')
table_create_query = '''CREATE TABLE IF NOT EXISTS Product_data(product_name TEXT, description TEXT, stock_value INT, sales_month INT, sales_year INT, selected_year INT, selected_supplier TEXT)'''
conn.execute(table_create_query)
conn.close()
query_db()  # Call query_db() to populate the treeview widget

# Define the query_db() function to populate the treeview widget

    

def clear_entry():
    entry_product_name.delete(0, END)
    entry_description.delete('1.0', END)  # Use '1.0' as the start index
    entry_stock_value.delete(0, END)
    entry_sales_month.delete(0, END)
    entry_sales_year.delete(0, END)
    year_combobox.current(0)
    supplier_combobox.current(0)
    show()  # Update the treeview after clearing the entry fields




def update():
    product_name = entry_product_name.get()
    description = entry_description.get("1.0", tk.END)
    stock_value = entry_stock_value.get()
    sales_month = entry_sales_month.get()
    sales_year = entry_sales_year.get()
    selected_year = year_var.get()  # No need to use get() with IntVar
    selected_supplier = supplier_var.get()  # No need to use get() with StringVar

    messagebox.showinfo("Success", "Purchase Order details have been updated.")

    conn = sqlite3.connect('data.db')
    data_update = '''UPDATE Product_data SET description=?,stock_value=?,sales_month=?,sales_year=?,selected_year=?,selected_supplier=? WHERE product_name=?'''
    data_tuple = (description, stock_value, sales_month, sales_year, selected_year, selected_supplier, product_name)
    cursor = conn.cursor()
    cursor.execute(data_update, data_tuple)
    conn.commit()
    conn.close()
    show()

    entry_product_name.delete(0, END)
    entry_description.delete(1.0, END)
    entry_stock_value.delete(0, END)
    entry_sales_month.delete(0, END)
    entry_sales_year.delete(0, END)
    year_var.set(2021)  # Set default value for year_var
    supplier_var.set("Select")  # Set default value for supplier_var

def delete():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    ref_no_value = entry_stock_value.get()
    op = messagebox.askyesno("Confirm Deletion", f"Do you really want to delete the record with Product Name: {ref_no_value}?")
    if op:
        cursor.execute("DELETE FROM Product_data WHERE stock_value=?", (ref_no_value,))
        conn.commit()
        messagebox.showinfo("Delete", "Product Details Deleted Successfully")
        clear_entry()
        query_db()  
  # Update the treeview after deleting the record
    else:
        messagebox.showinfo("Not Deleted", "Deletion canceled")


def search():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    try:
        if cmb_box.get() == "Select":
            messagebox.showerror("Error", "Select Search by option")
        elif txt_search.get() == "":
            messagebox.showerror("Error", "Search input is required")
        else:
            search_option = cmb_box.get()
            search_query = f"SELECT * FROM Product_data WHERE {search_option.replace(' ', '_')} LIKE ?"
            cursor.execute(search_query, ('%' + txt_search.get() + '%',))
            rows = cursor.fetchall()
            if len(rows) != 0:
                tree_table.delete(*tree_table.get_children())
                for row in rows:
                    tree_table.insert('', END, values=row)
            else:
                messagebox.showerror("No record found", "No record found matching the search criteria")
    except Exception as ex:
        messagebox.showerror("Error", f"Error due to: {str(ex)}")

def clear():
    entry_product_name.delete(0, END)
    entry_description.delete(0, END)
    entry_stock_value.delete(0, END)
    entry_sales_month.delete(0,END)
    entry_sales_year.delete(0,END)
    year_var.set("2021")
    supplier_var.set("Select")
    show()
       





def dashboard():
         root.destroy()
         subprocess.run(["python","C:\\Users\\ACER\\IdeaProjects\\dashboard.py"])           



add_btn = Button(root, text="Save", command=submit_form,width=10,bg='#6C22A6',fg='#fff',border=0, font=('Microsoft YaHei UI Light', 10, 'bold'))
add_btn.place(x=700,y=600)
update_btn = Button(root, text="Update", command=update,width=10,bg='#6C22A6',fg='#fff',border=0, font=('Microsoft YaHei UI Light', 10, 'bold'))
update_btn.place(x=840,y=600)
delete_btn = Button(root, text="Delete", command=delete, width=10,bg='#6C22A6',fg='#fff',border=0, font=('Microsoft YaHei UI Light', 10, 'bold'))
delete_btn.place(x=980,y=600)
clear_btn = Button(root,  text="Clear", command=clear_entry, width=10,bg='#6C22A6',fg='#fff',border=0, font=('Microsoft YaHei UI Light', 10, 'bold'))
clear_btn.place(x=1120,y=600)
search_btn =Button(search_frame,  text="Search", command=search, width=10,bg='#6C22A6',fg='#fff',border=0, font=('Microsoft YaHei UI Light', 10, 'bold'))
search_btn.place(x= 430, y = 40)
back_btn =Button(root,  text="Back", command=dashboard, width=10,bg='#6C22A6',fg='#fff',border=0, font=('Microsoft YaHei UI Light', 10, 'bold'))
back_btn.place(x= 1230, y = 600)




# Apply Styling
style = ttk.Style(root)
style.configure("Main.TFrame", background="#E6E6FA")  # Lightest purple background color
style.configure("TLabel", foreground="#311b92")  # Dark purple text color for labels and borders
style.configure("TButton", foreground="#000000")  # Black text color for buttons

# Create a new style for the Submit button with a black background
style.configure("Submit.TButton", bg="#4B0082", fg="white")


root.mainloop()