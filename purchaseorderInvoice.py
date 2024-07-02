import datetime
import tkinter as tk
from tkinter import *
from tkinter import ttk,messagebox
import sqlite3
import subprocess
from docxtpl import DocxTemplate

class saleorder:

    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700")
        self.root.title("Sale Order Details")
        self.root.config(bg="#4B0082")  # Lightest purple background color
        self.root.state('zoomed')

        self.date = StringVar()
        self.refno = StringVar()
        self.customername = StringVar()
        self.productname = StringVar()
        self.quantity = StringVar()
        self.price = StringVar()
        self.totalamt = StringVar()

        main_frame = ttk.Frame(root, padding=(20, 20, 20, 20), style="Main.TFrame", borderwidth=2, relief="solid")
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        label_detail = ttk.Label(main_frame,text="Purchase Order Details",font=('Microsoft YaHei UI Bold', 28, 'bold'),foreground="black",background="#E6E6FA")
        label_detail.pack(anchor="w", pady=5)

        # Sale Order Form
        date_label = Label(main_frame, text="Date:", font=('Arial', 14, 'bold'), bg="#E6E6FA")
        date_label.pack(anchor="w", pady=5)
        self.txt_date_label = Entry(main_frame, textvariable=self.date, font=('Arial', 14), bg="white")
        self.txt_date_label.pack(anchor="w", pady=5)

        ref_no_label = Label(main_frame, text="Reference No:", font=('Arial', 14, 'bold'), bg="#E6E6FA")
        ref_no_label.pack(anchor="w", pady=5)
        self.txt_ref_no_label = Entry(main_frame, textvariable=self.refno, font=('Arial', 14), bg="white")
        self.txt_ref_no_label.pack(anchor="w", pady=5)

        customer_name_label = Label(main_frame, text="Customer Name:", font=('Arial', 14, 'bold'), bg="#E6E6FA")
        customer_name_label.pack(anchor="w", pady=5)
        self.txt_customer_name_label = Entry(main_frame, textvariable=self.customername, font=('Arial', 14), bg="white")
        self.txt_customer_name_label.pack(anchor="w", pady=5)

        product_name_label = Label(main_frame, text="Product Name:", font=('Arial', 14, 'bold'), bg="#E6E6FA")
        product_name_label.pack(anchor="w", pady=5)
        self.category_txt = Entry(main_frame, textvariable=self.productname, font=('Arial', 14), bg="white")
        self.category_txt.pack(anchor="w", pady=5)

        quantity_label = Label(main_frame, text="Quantity:", font=('Arial', 14, 'bold'), bg="#E6E6FA")
        quantity_label.pack(anchor="w", pady=5)
        self.quantity_txt = Entry(main_frame, textvariable=self.quantity, font=('Arial', 14), bg="white")
        self.quantity_txt.pack(anchor="w", pady=5)

        price_label = Label(main_frame, text="Price:", font=('Arial', 14, 'bold'), bg="#E6E6FA")
        price_label.pack(anchor="w", pady=5)
        self.price_txt = Entry(main_frame, textvariable=self.price, font=('Arial', 14), bg="white")
        self.price_txt.pack(anchor="w", pady=5)

        amount_label = Label(main_frame, text="Total Amount:", font=('Arial', 14, 'bold'), bg="#E6E6FA")
        amount_label.pack(anchor="w", pady=5)
        self.amount_txt = Entry(main_frame, textvariable=self.totalamt, font=('Arial', 14), bg="white")
        self.amount_txt.pack(anchor="w", pady=5)

        btn_save = Button(main_frame, text="Save", command=self.save, width=10, bg="#6C22A6", fg="#fff", font=('Microsoft YaHei UI Light', 10, 'bold'))
        btn_save.place(x=500,y=530)
        
        btn_update = Button(main_frame, text="Update", command=self.update, width=10, bg="#6C22A6", fg="#fff", font=('Microsoft YaHei UI Light', 10, 'bold'))
        btn_update.place(x=650,y=530)
        
        btn_delete = Button(main_frame, text="Delete", command=self.delete, width=10, bg="#6C22A6", fg="#fff", font=('Microsoft YaHei UI Light', 10, 'bold'))
        btn_delete.place(x=800,y=530)
        
        btn_clear = Button(main_frame, text="Clear", command=self.clear, width=10, bg="#6C22A6", fg="#fff", font=('Microsoft YaHei UI Light', 10, 'bold'))
        btn_clear.place(x=950,y=530)

        btn_back = Button(main_frame, text="Back", command=self.dashboard, width=10, bg="#6C22A6", fg="#fff", font=('Microsoft YaHei UI Light', 10, 'bold'))
        btn_back.place(x=1100,y=530)

        btn_invoice = Button(main_frame, text="invoice", command=self.generate_invoice, width=10, bg="#6C22A6", fg="#fff", font=('Microsoft YaHei UI Light', 10, 'bold'))
        btn_invoice.place(x=1300,y=630)


        # sale_frame  = Frame(self.root,bd=3,relief=RIDGE,height=100,width=400)
        # sale_frame.place(x=500,y=350,relwidth=1,height=150)
        sale_frame = ttk.Frame(main_frame,width=500, height=400)
        sale_frame.place(x=680, y=210)
        scrolly = Scrollbar(sale_frame,orient=VERTICAL)
        scrollx = Scrollbar(sale_frame,orient=HORIZONTAL)

        self.saletable = ttk.Treeview(sale_frame,columns=("date","refno","customername","productname","quantity","price","totalamt"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.saletable.xview)
        scrolly.config(command=self.saletable.yview)

        self.saletable.heading("date",text="Date")
        self.saletable.heading("refno",text="Ref No.")
        self.saletable.heading("customername",text="Vendor Name")
        self.saletable.heading("productname",text="Product Name")
        self.saletable.heading("quantity",text="Quantity")
        self.saletable.heading("price",text="Price")
        self.saletable.heading("totalamt",text="Total Amount")
        self.saletable["show"]="headings"
        self.saletable.pack(fill=BOTH,expand=1)

        self.saletable.column("date",width=100)
        self.saletable.column("refno",width=100)
        self.saletable.column("customername",width=100)
        self.saletable.column("productname",width=100)
        self.saletable.column("quantity",width=100)
        self.saletable.column("price",width=100)
        self.saletable.column("totalamt",width=100)
        self.saletable.pack(fill=BOTH,expand=1)
        self.saletable.bind("<ButtonRelease-1>",self.get_data)

        conn = sqlite3.connect('data.db')
        table_create_query = '''CREATE TABLE IF NOT EXISTS PurchaseOrder_data(date_value TEXT, ref_no_value TEXT, vendor_name_value TEXT, category_value TEXT, quantity_value INT, price_value INT, total_value FLOAT)'''
        conn.execute(table_create_query)
        conn.close()
        self.show()

    def save(self):
        date_value = self.txt_date_label.get()
        ref_no_value = self.txt_ref_no_label.get()
        vendor_name_value = self.txt_customer_name_label.get()
        category_value = self.category_txt.get()
        quantity_value = self.quantity_txt.get()
        price_value = self.price_txt.get()
        total_value = self.amount_txt.get()

        messagebox.showinfo("Success", "Sale Order details have been inserted.")


        conn = sqlite3.connect('data.db')
        data_insert = '''INSERT INTO PurchaseOrder_data(date_value, ref_no_value, vendor_name_value, category_value, quantity_value, price_value, total_value) VALUES(?,?,?,?,?,?,?)'''
        data_tuple = (date_value, ref_no_value, vendor_name_value, category_value, quantity_value, price_value, total_value)
        cursor = conn.cursor()
        cursor.execute(data_insert, data_tuple)
        conn.commit()
        conn.close()
        self.show()


        self.txt_date_label.set_date(None)
        self.txt_ref_no_label.delete(0, tk.END)
        self.txt_customer_name_label.delete(0, tk.END)
        self.category_txt.delete(0, tk.END)
        self.quantity_txt.delete(0, tk.END)
        self.price_txt.delete(0, tk.END)
        self.amount_txt.delete(0, tk.END)

    def generate_invoice(self):
            doc = DocxTemplate("puchase_invoice.docx")
            name = self.txt_customer_name_label.get()
            refno = self.txt_ref_no_label.get()
            quantity =  self.quantity_txt.get()
            proname = self.category_txt.get()
            total = self.amount_txt.get()
            price = self.price_txt.get()
            date = self.txt_date_label.get()
            
            doc.render({"name":name, 
                    "refno":refno,
                    "qty": quantity,
                    "productName":proname,
                    "price":price,
                    "total":total,
                    "date": date})
            
            doc_name = "new_invoice" + name + datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S") + ".docx"
            doc.save(doc_name)
            
            messagebox.showinfo("Invoice Complete", "Invoice Complete")    


    def dashboard(self):
        self.root.destroy()
        subprocess.run(["python","dashboard.py"])    
    
    def show(self):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        try:
            cursor.execute("Select * from PurchaseOrder_data")
            rows = cursor.fetchall()
            self.saletable.delete(*self.saletable.get_children())
            for row in rows:
                self.saletable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}") 


    def dashboard(self):
        self.root.destroy()
        subprocess.run(["python","C:\\Users\\ACER\\IdeaProjects\\dashboard.py"])
        


    def get_data(self,ev):
        f=self.saletable.focus()
        content = (self.saletable.item(f))
        row = content['values']
        self.txt_date_label.delete(0, END)    
        self.txt_date_label.insert(0, row[0])
        self.txt_ref_no_label.delete(0, END)
        self.txt_ref_no_label.insert(0, row[1])
        self.txt_customer_name_label.delete(0, END)
        self.txt_customer_name_label.insert(0, row[2])
        self.category_txt.delete(0, END)
        self.category_txt.insert(0, row[3])
        self.quantity_txt.delete(0, END)
        self.quantity_txt.insert(0, row[4])
        self.price_txt.delete(0, END)
        self.price_txt.insert(0, row[5])
        self.amount_txt.delete(0, END)
        self.amount_txt.insert(0, row[6])


    def update(self):
        date_value = self.txt_date_label.get()
        ref_no_value = self.txt_ref_no_label.get()
        vendor_name_value = self.txt_customer_name_label.get()
        category_value = self.category_txt.get()
        quantity_value = self.quantity_txt.get()
        price_value = self.price_txt.get()
        total_value = self.amount_txt.get()

        messagebox.showinfo("Success", "Sale Order details have been updated.")

        conn = sqlite3.connect('data.db')
        data_insert = '''UPDATE PurchaseOrder_data SET date_value=?, vendor_name_value=?, category_value=?, quantity_value=?, price_value=?, total_value=? WHERE ref_no_value=?'''
        data_tuple = (date_value, vendor_name_value, category_value, quantity_value, price_value, total_value, ref_no_value)
        cursor = conn.cursor()
        cursor.execute(data_insert, data_tuple)
        conn.commit()
        conn.close()
        self.show()

        self.txt_date_label.delete(0, END)
        self.txt_ref_no_label.delete(0, END)
        self.txt_customer_name_label.delete(0, END)
        self.category_txt.delete(0, END)
        self.quantity_txt.delete(0, END)
        self.price_txt.delete(0, END)
        self.amount_txt.delete(0, END)


    def query_db(self):
        con = sqlite3.connect('data.db')
        c = con.cursor()

    # Clear existing data from the treeview
        self.saletable.delete(*self.saletable.get_children())

        c.execute("SELECT * FROM Product_data")
        records = c.fetchall()

        for idx, row in enumerate(records, start=1):
            tags = 'evenrow' if idx % 2 == 0 else 'oddrow'
            self.saletable.insert(parent='', index='end', iid=idx, text='', values=row, tags=(tags,))

        con.close()


    def delete(self):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        ref_no_value = self.txt_ref_no_label.get()
        op = messagebox.askyesno("Confirm Deletion", f"Do you really want to delete the record with reference number: {ref_no_value}?")
        if op:
            cursor.execute("DELETE FROM PurchaseOrder_data WHERE ref_no_value=?", (ref_no_value,))
            conn.commit()
            messagebox.showinfo("Delete", "Purchase Order Order Deleted Successfully")
            self.clear()  # Clear form fields
            self.query_db()   # Refresh displayed data
        else:
            messagebox.showinfo("Not Deleted", "Deletion canceled")


    def clear(self):
        self.txt_date_label.delete(0, END)    
       
        self.txt_ref_no_label.delete(0, END)
        
        self.txt_customer_name_label.delete(0, END)
        
        self.category_txt.delete(0, END)
        
        self.quantity_txt.delete(0, END)
        
        self.price_txt.delete(0, END)
        
        self.amount_txt.delete(0, END)
        self.txt_search.set("")
        self.cmb_search.set("Select")

        self.show()

    def search(self):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        try:
            if self.cmb_search.get() == "Select":
                messagebox.showerror("Error", "Select Search by option")
            elif self.txt_search.get() == "":
                messagebox.showerror("Error", "Search input is required")
            else:
                search_option = self.cmb_search.get()
                search_query = f"SELECT * FROM PurchaseOrder_data WHERE {search_option.replace(' ', '_')} LIKE ?"
                cursor.execute(search_query, ('%' + self.txt_search.get() + '%',))
                rows = cursor.fetchall()
                if len(rows) != 0:
                    self.saletable.delete(*self.saletable.get_children())
                    for row in rows:
                        self.saletable.insert('', END, values=row)
                else:
                    messagebox.showerror("No record found", "No record found matching the search criteria")
        except Exception as ex:
             messagebox.showerror("Error", f"Error due to: {str(ex)}")


if __name__ == "__main__":
    root = Tk()
    obj = saleorder(root)
    root.mainloop()
