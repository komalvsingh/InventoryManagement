from tkinter import *
from PIL import Image, ImageTk
import requests
from io import BytesIO
from tkinter import ttk,messagebox
from datetime import datetime  # Added for fetching current date and time
import subprocess
import sqlite3

class IMS:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")

        # Fetch current date and time
        current_datetime = datetime.now().strftime("%d-%m-%Y    %H:%M:%S")

        # Fetch image from URL
        response = requests.get("https://cdn-icons-png.flaticon.com/512/7656/7656409.png")
        image_bytes = BytesIO(response.content)
        img = Image.open(image_bytes)
        img = img.resize((50, 50))  # Resize the image as needed

        # Convert image to PhotoImage and keep a reference
        self.bg_image = ImageTk.PhotoImage(img)

        # Create label with image
        title = Label(self.root, text="Inventify", image=self.bg_image, compound=LEFT,
                      font=("times new roman", 40, "bold"), bg="#0C1066", fg="white", anchor="w", padx=20)
        title.image = self.bg_image  # Keep a reference to the image
        title.place(x=0, y=0, relwidth=1, height=70)
        # clock statement

        # Update clock label text
        self.clock = Label(self.root, text=f"Welcome to Inventory Management System\t\t Date & Time: {current_datetime}",
                           font=("times new roman", 15), bg="#E6E6FA", fg="black")
        self.clock.place(x=0, y=70, relwidth=1, height=30)

        #left menu
        # Fetch image from URL
        response1 = requests.get("https://d38cf3wt06n6q6.cloudfront.net/tyasuitefront/webgpcs/images/warehouse-management-software.png")
        image_bytes1 = BytesIO(response1.content)
        img1 = Image.open(image_bytes1)
        img1 = img1.resize((200, 200))  # Resize the image as needed

        # Convert image to PhotoImage and keep a reference
        self.left_image = ImageTk.PhotoImage(img1)
        leftmenu = Frame(self.root,bd=2,relief=RIDGE ,bg="white")
        leftmenu.place(x=0,y=130,width=230,height=600)
        lbl_menu = Label(leftmenu,image=self.left_image)
        lbl_menu.pack(side=TOP,fill=X)

        label_menu = Label(leftmenu,text="Menu",font=("times new roman",20),bg="#FFD700").pack(side=TOP,fill=X)
        btn_supplier = Button(leftmenu,text="Supplier",font=("times new roman",15,"bold"),bg="white",bd=3,cursor="hand2",command=self.open_supplier).pack(side=TOP,fill=X)
        btn_suptrack = Button(leftmenu,text="Track Suppliers",font=("times new roman",15,"bold"),bg="white",bd=3,cursor="hand2",command=self.open_track_page).pack(side=TOP,fill=X)
        btn_product = Button(leftmenu,text="Products",font=("times new roman",15,"bold"),bg="white",bd=3,cursor="hand2",command=self.open_product_page).pack(side=TOP,fill=X)
        btn_report = Button(leftmenu,text="Report",font=("times new roman",15,"bold"),bg="white",bd=3,cursor="hand2",command=self.open_reports_page).pack(side=TOP,fill=X)
        btn_purchaseorder = Button(leftmenu,text="Purchase Order",font=("times new roman",15,"bold"),bg="white",bd=3,cursor="hand2",command=self.open_purchaseorder_page).pack(side=TOP,fill=X)
        btn_purinvoice = Button(leftmenu,text="Purchase Order Invoice",font=("times new roman",15,"bold"),bg="white",bd=3,cursor="hand2",command=self.open_purchaseinvoice_page).pack(side=TOP,fill=X)
        btn_demand = Button(leftmenu,text="Product Demand Predictor",font=("times new roman",15,"bold"),bg="white",bd=3,cursor="hand2",command=self.open_demand_page).pack(side=TOP,fill=X)
        
        self.lbl_supplier = Label(self.root,text="Total Suppliers\n[0]",bg="#F08080",font=("goudy old style",20,"bold"))
        self.lbl_supplier.place(x=330,y=120,height=150,width=200)

        self.lbl_product = Label(self.root,text="Total Products\n[0]",bg="#BDFCC9",font=("goudy old style",20,"bold"))
        self.lbl_product.place(x=600,y=120,height=150,width=200)

        self.lbl_purchase = Label(self.root,text="Total Purchase\n Invoice\n[0]",bg="#BBFFFF",font=("goudy old style",20,"bold"))
        self.lbl_purchase.place(x=900,y=120,height=150,width=200)

        purchase_frame  = Frame(self.root,bd=3,relief=RIDGE)
        purchase_frame.place(x=230,y=340,relwidth=0.8,height=150)
        scrolly = Scrollbar(purchase_frame,orient=VERTICAL)
        scrollx = Scrollbar(purchase_frame,orient=HORIZONTAL)


        purchaselabel = Label(self.root,text="Recent Purchase Invoice",font=("times new roman",20),bg="#EAEAEA",anchor="w")
        purchaselabel.place(x=230,y=300,height=23,width=1300)
        self.purchasetable = ttk.Treeview(purchase_frame,columns=("date","refno","vendorname","productname","quantity","price","totalamt"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.purchasetable.xview)
        scrolly.config(command=self.purchasetable.yview)

        self.purchasetable.heading("date",text="Date")
        self.purchasetable.heading("refno",text="Ref No.")
        self.purchasetable.heading("vendorname",text="Vendor Name")
        self.purchasetable.heading("productname",text="Product Name")
        self.purchasetable.heading("quantity",text="Quantity")
        self.purchasetable.heading("price",text="Price")
        self.purchasetable.heading("totalamt",text="Total Amount")
        self.purchasetable["show"]="headings"
        self.purchasetable.pack(fill=BOTH,expand=1)

        self.purchasetable.column("date",width=50)
        self.purchasetable.column("refno",width=50)
        self.purchasetable.column("vendorname",width=50)
        self.purchasetable.column("productname",width=50)
        self.purchasetable.column("quantity",width=50)
        self.purchasetable.column("price",width=50)
        self.purchasetable.column("totalamt",width=50)
        self.purchasetable.pack(fill=BOTH,expand=1)
        self.purchasetable.bind("<ButtonRelease-1>")

        prolabel = Label(self.root,text="Recent added Products",font=("times new roman",20),bg="#EAEAEA",anchor="w")
        prolabel.place(x=230,y=515,height=23,width=1300)
        product_frame  = Frame(self.root,bd=3,relief=RIDGE)
        product_frame.place(x=230,y=550,relwidth=0.8,height=150)
        scrolly = Scrollbar(product_frame,orient=VERTICAL)
        scrollx = Scrollbar(product_frame,orient=HORIZONTAL)


       
        self.producttable = ttk.Treeview(product_frame,columns=("productname","description","stockvalue","stockmonth","salesyear","year","supplier"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.purchasetable.xview)
        scrolly.config(command=self.purchasetable.yview)

        self.producttable.heading("productname",text="Product Name")
        self.producttable.heading("description",text="Description")
        self.producttable.heading("stockvalue",text="Stock Value")
        self.producttable.heading("stockmonth",text="Stock Month")
        self.producttable.heading("salesyear",text="Sales Year")
        self.producttable.heading("year",text="Year")
        self.producttable.heading("supplier",text="Suppliers")
        self.producttable["show"]="headings"
        self.producttable.pack(fill=BOTH,expand=1)

        self.producttable.column("productname",width=50)
        self.producttable.column("description",width=50)
        self.producttable.column("stockvalue",width=50)
        self.producttable.column("stockmonth",width=50)
        self.producttable.column("salesyear",width=50)
        self.producttable.column("year",width=50)
        self.producttable.column("supplier",width=50)
        self.producttable.pack(fill=BOTH,expand=1)
        self.producttable.bind("<ButtonRelease-1>")

        conn = sqlite3.connect('data.db')
        # table_create_query = '''CREATE TABLE IF NOT EXISTS PurchaseOrder_data(date_value TEXT, ref_no_value TEXT, vendor_name_value TEXT, category_value TEXT, quantity_value INT, price_value INT, total_value FLOAT)'''
        # conn.execute(table_create_query)
        conn.close()
        self.show()
        self.showproduct()
        self.update_content()
        
    
    def open_track_page(self):
        self.root.destroy()
        subprocess.run(["python", "C:\\Users\\ACER\\IdeaProjects\\track.py"])

    
    def show(self):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT date_value, ref_no_value, vendor_name_value, category_value, quantity_value, price_value, total_value FROM PurchaseOrder_data")
            rows = cursor.fetchall()
            self.purchasetable.delete(*self.purchasetable.get_children())
            
            for row in rows:
            # Insert each row of data into the Treeview widget
                self.purchasetable.insert('', END, values=row)
             
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}")
        finally:
            conn.close()


    def showproduct(self):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT product_name, description, stock_value, sales_month, sales_year, selected_year, selected_supplier from Product_data")
            rows = cursor.fetchall()
            self.producttable.delete(*self.producttable.get_children())
            
            for row in rows:
            # Insert each row of data into the Treeview widget
                self.producttable.insert('', END, values=row)
             
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}")
        finally:
            conn.close()





    def open_product_page(self):
        self.root.destroy()
        subprocess.run(["python", "C:\\Users\\ACER\\IdeaProjects\\productdetails.py"])


    def open_reports_page(self):
        self.root.destroy()
        subprocess.run(["python", "C:\\Users\\ACER\\IdeaProjects\\reports.py"]) 

    def open_purchaseorder_page(self):
        self.root.destroy()
        subprocess.run(["python", "purchaseOrder.py"])  


    def open_purchaseinvoice_page(self):
        self.root.destroy()
        subprocess.run(["python", "C:\\Users\\ACER\\IdeaProjects\\purchaseorderInvoice.py"]) 

    def open_supplier(self):
        self.root.destroy()
        subprocess.run(["python","C:\\Users\\ACER\\IdeaProjects\\supplier.py"])

    def open_demand_page(self):
        self.root.destroy()
        subprocess.run(["python","C:\\Users\\ACER\\IdeaProjects\\ProductDemand.py"])


    def update_content(self):
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        cur1 = conn.cursor()
        cur2 = conn.cursor()
        try:
            cur.execute("select * from Product_data")
            cur1.execute("select * from supplier")
            cur2.execute("select * from PurchaseOrder_data")
            supp = cur1.fetchall()
            pro = cur.fetchall()
            pur = cur2.fetchall()
            self.lbl_product.config(text=f'Total Products\n[{str(len(pro))}]')
            self.lbl_supplier.config(text=f'Total Suppliers\n[{str(len(supp))}]')
            self.lbl_purchase.config(text=f'Total Purchase\n[{str(len(pur))}]')

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}")    


    





             

root = Tk()
obj = IMS(root)
root.mainloop()
