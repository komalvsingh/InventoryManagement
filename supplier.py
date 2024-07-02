from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import subprocess


# data = [
#     [1, "Komal suppliers", "3434434", "acer laptop"],
#     [2, "jai mata di suppliers", "22334343", "hp laptop"],
#     [3, "lotus suppliers", "4534434", "dell laptop"],
#     [4, "newTech suppliers", "77834434", "apple laptop"], 
#     [5, "sanskruti suppliers", "37647863", "Apple Ipad, Apple Pen"]   
# ]


con = sqlite3.connect(database='data.db')
cur=con.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS supplier (invoice INTEGER PRIMARY KEY AUTOINCREMENT,
            name text,
            contact text,
            desc text)""")
# for record in data:
#     cur.execute(" INSERT INTO supplier VALUES (:invoice, :name, :contact, :desc)",
#             {
#             'invoice': record[0],
#             'name': record[1],
#             'contact': record[2],
#             'desc': record[3]
#             })
con.commit()
con.close()

class supplierClass:

    def __init__(self,root):
        self.root = root
        self.root.title("Suppliers")
        self.root.geometry("1350x700")
        self.root.configure(bg="#fff")
        self.root.state('zoomed')

        #Search
        self.var_searchtxt = StringVar()
        self.var_searchby = StringVar()
        search_frame = Frame(self.root, width= 555, height=100, bg='#fff', border=1)
        search_frame.place(x=680, y=120)
        search_header = Label(search_frame, text="What are you looking for?", bg='#fff', fg='black', font=('Microsoft YaHei UI bold', 13))
        search_header.place(x=14, y=0)
        txt_search = Entry(search_frame, textvariable=self.var_searchtxt, width= 25, font=('Microsoft YaHei UI Light', 13), bg='#F1EAFF')
        txt_search.place(x=20, y= 40)

        cmb_box = ttk.Combobox(search_frame, textvariable=self.var_searchby, width=13, values=("Select","Name", "Contact", "Desc"), state='readonly',font=('Microsoft YaHei UI light', 13))
        cmb_box.place(x=270, y=40)
        cmb_box.current(0)

        #Header label
        Manage_suppliers_tag = Label(self.root,text="Manage Suppliers data",bg="#fff", fg="black", font=('Microsoft YaHei UI Bold', 28, 'bold') )
        Manage_suppliers_tag.place(x=40, y=20)

        # Form entry feilds start from here==================
        lbl_invoice = Label(self.root,text="Invoice Number",bg="#fff", fg="#6C22A6", font=('Microsoft YaHei UI Light', 21) )
        lbl_invoice.place(x=120, y = 120)
        self.in_entry = Entry(self.root, width=25, fg='black', border=0,bg='#fff',font=('Microsoft YaHei UI semi bold', 14))
        self.in_entry.place(x=120, y = 170)
        Frame(self.root, width=280, height=2,bg='black').place(x=120, y = 200)

        lbl_name = Label(self.root,text="Supplier Name",bg="#fff", fg="#6C22A6", font=('Microsoft YaHei UI Light', 21) )
        lbl_name.place(x=120, y = 240)
        self.name_entry = Entry(self.root, width=25, fg='black', border=0,bg='#fff',font=('Microsoft YaHei UI semi bold', 14))
        self.name_entry.place(x=120, y = 290)
        Frame(self.root, width=400, height=2,bg='black').place(x=120, y = 320)


        lbl_contact = Label(self.root,text="Contact",bg="#fff", fg="#6C22A6", font=('Microsoft YaHei UI Light', 21) )
        lbl_contact.place(x=120, y = 360)
        self.contact_entry = Entry(self.root, width=25, fg='black', border=0,bg='#fff',font=('Microsoft YaHei UI semi bold', 14))
        self.contact_entry.place(x=120, y = 410)
        Frame(self.root, width=400, height=2,bg='black').place(x=120, y = 440)

        lbl_desc = Label(self.root, text="Description", bg='#fff', fg='#6C22A6',font=('Microsoft YaHei UI Light', 21))
        lbl_desc.place(x=120, y= 480)
        self.Desc_text = Text(self.root,border=2, width=40,height=5, bg='#F1EAFF',font=('Microsoft YaHei UI semi bold', 14) )
        self.Desc_text.place(x=120, y=530)

        # Supplier table=========================================


        sup_table_frame = Frame(self.root,width=500, height=400)
        sup_table_frame.place(x=680, y=290)

        tree_scroll_x = Scrollbar(sup_table_frame, orient=HORIZONTAL)
        tree_scroll_y = Scrollbar(sup_table_frame, orient=VERTICAL)

        self.tree_table = ttk.Treeview(sup_table_frame,yscrollcommand=tree_scroll_y.set,xscrollcommand=tree_scroll_x.set, selectmode="extended")
        tree_scroll_y.pack(side=RIGHT, fill=Y)
        tree_scroll_x.pack(side=BOTTOM, fill=X)
        tree_scroll_x.config(command=self.tree_table.xview)
        tree_scroll_y.config(command=self.tree_table.yview)
        self.tree_table.pack()


        self.tree_table["columns"] = ('invoice', 'name', 'contact', 'description')
        self.tree_table.column("#0", width=0,stretch=NO)
        self.tree_table.column("invoice", anchor=W, width=100)
        self.tree_table.column("name", anchor=W, width=140)
        self.tree_table.column("contact", anchor=W, width=140)
        self.tree_table.column("description", anchor=W,width=160)
        self.tree_table.bind("<ButtonRelease-1>", self.select_record)
        self.tree_table.tag_configure('oddrow', background='white')
        self.tree_table.tag_configure('evenrow', background='#F1EAFF')

        self.tree_table.heading("invoice", anchor=W, text="Invoice")
        self.tree_table.heading("name", anchor=W, text="Name")
        self.tree_table.heading("contact", anchor=W, text="Contact")
        self.tree_table.heading("description", anchor=W, text="Description")

        add_btn = Button(self.root, text="Save", command=self.add,width=10,bg='#6C22A6',fg='#fff',border=0, font=('Microsoft YaHei UI Light', 10, 'bold'))
        add_btn.place(x=700,y=600)
        update_btn = Button(self.root, text="Update", command=self.update_record,width=10,bg='#6C22A6',fg='#fff',border=0, font=('Microsoft YaHei UI Light', 10, 'bold'))
        update_btn.place(x=840,y=600)
        delete_btn = Button(self.root, text="Delete", command=self.delete_record, width=10,bg='#6C22A6',fg='#fff',border=0, font=('Microsoft YaHei UI Light', 10, 'bold'))
        delete_btn.place(x=980,y=600)
        clear_btn = Button(self.root,  text="Clear", command=self.clear_entry, width=10,bg='#6C22A6',fg='#fff',border=0, font=('Microsoft YaHei UI Light', 10, 'bold'))
        clear_btn.place(x=1120,y=600)
        search_btn =Button(search_frame,  text="Search", command=self.search, width=10,bg='#6C22A6',fg='#fff',border=0, font=('Microsoft YaHei UI Light', 10, 'bold'))
        search_btn.place(x= 430, y = 40)
        back_btn =Button(self.root,  text="Back", command=self.dashboard, width=10,bg='#6C22A6',fg='#fff',border=0, font=('Microsoft YaHei UI Light', 10, 'bold'))
        back_btn.place(x= 1240, y = 600)

    def query_db(self):
      con=sqlite3.connect('data.db')
      c = con.cursor()

      c.execute("Select * from supplier")
      records = c.fetchall()
      #print(records)

      global count
      count = 0

      for row in records:
          if count%2==0:
              self.tree_table.insert(parent='', index='end', iid=count, text='', values=(row[0], row[1], row[2], row[3]), tags=('evenrow',))
          else:
              self.tree_table.insert(parent='', index='end', iid=count, text='', values=(row[0], row[1], row[2], row[3]), tags=('oddrow',))

          count+=1

      con.commit()
      con.close()

    def clear_entry(self):
        self.in_entry.delete(0, END)
        self.name_entry.delete(0, END)
        self.contact_entry.delete(0, END)
        self.Desc_text.delete('1.0',END)

    def add(self):
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        try:
            if self.in_entry.get() == "":
                messagebox.showerror("Error", "Invoice number is required.", parent= self.root)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.in_entry.get(),))
                row = cur.fetchone()
                if row!= None:
                    messagebox.showerror("Error","This invoice number already exists, try different invoice number.", parent=self.root)
                else:
                     cur.execute("""INSERT INTO supplier VALUES (:invoice, :name,:contact,:desc)""",
                            {   
                                'invoice': self.in_entry.get(),
                                'name': self.name_entry.get(),
                                'contact': self.contact_entry.get(),
                                'desc': self.Desc_text.get('1.0', END)   
                            })
                     con.commit()
                     con.close()
                     messagebox.showinfo("Success", "Record Added Successfully", parent=self.root)
                     self.tree_table.delete(*self.tree_table.get_children())
                     self.query_db()
                     self.clear_entry()
        except Exception as e:
            messagebox.showerror("Error", f"Error due to : {str(e)}",parent=self.root)

    def select_record(self,ev):
        #select the record and row
        selected = self.tree_table.focus()
        content = self.tree_table.item(selected)
        row = content['values']

        #clear the entry boxes
        self.clear_entry()


        #insert in the entry boxes
        self.in_entry.insert(0, row[0])
        self.name_entry.insert(0, row[1])
        self.contact_entry.insert(0, row[2])
        self.Desc_text.insert(END,row[3])

    def update_record(self):
        selected = self.tree_table.focus()
        content = self.tree_table.item(selected)
        row = content['values']


        con = sqlite3.connect('data.db')
        cur = con.cursor()
        try:
            if self.in_entry.get() == "":
                messagebox.showerror("Error", "Invoice number is required.", parent= self.root)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.in_entry.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error","Invalid Invoice Number.", parent=self.root)
                else:
                      con.execute("""UPDATE supplier SET name= :name,
                                                         contact= :contact,
                                                         desc= :desc
                                                         WHERE oid= :oid""",
                                                         {
                                                           'name': self.name_entry.get(),
                                                           'contact': self.contact_entry.get(),
                                                           'desc': self.Desc_text.get('1.0', END),
                                                           'oid': self.in_entry.get()  
                                                         }
                            )
                      con.commit()
                      con.close()
                      messagebox.showinfo("Success", "Record Updated Successfully", parent=self.root)
                      self.tree_table.delete(*self.tree_table.get_children())
                      self.clear_entry()
                      self.query_db()
        except Exception as e:
            messagebox.showerror("Error", f"Error due to : {str(e)}",parent=self.root)

    def delete_record(self):
        con=sqlite3.connect('data.db')
        c= con.cursor()

        try:
                        if self.in_entry.get()=="":
                                messagebox.showerror("Error","Invoice number is required.",parent=self.root)
                        else:

                                c.execute("DELETE FROM supplier WHERE oid =" + self.in_entry.get())
                                con.commit()
                                messagebox.showinfo("Success","Data deleted successfully.",parent=self.root)

        except Exception as e:
                                messagebox.showerror("Error", f"Error due to : {str(e)}",parent=self.root)


        con.commit()
        con.close()
        self.tree_table.delete(*self.tree_table.get_children())
        self.clear_entry()
        self.query_db()  

    def search(self):

        try:
            if not self.var_searchtxt.get():
                messagebox.showerror("Error", "Search input is required.", parent=self.root)
                return

            con = sqlite3.connect(database='data.db')
            cur = con.cursor()
            search_query = "SELECT * FROM supplier WHERE {} LIKE ?".format(self.var_searchby.get())

            cur.execute(search_query, ('%' + self.var_searchtxt.get() + '%',))
            rows = cur.fetchall()

            if rows:
                self.tree_table.delete(*self.tree_table.get_children())
                for count, row in enumerate(rows, start=1):
                    tags = 'evenrow' if count % 2 == 0 else 'oddrow'
                    self.tree_table.insert(parent='', index='end', iid=count, text='', values=(row[0], row[1], row[2], row[3]), tags=(tags,))
            else:
                messagebox.showerror("Error", "No record found.", parent=self.root)

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error accessing database: {str(e)}", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}", parent=self.root)
        finally:
            if con:
                con.close()


    def dashboard(self):
         self.root.destroy()
         subprocess.run(["python","C:\\Users\\ACER\\IdeaProjects\\dashboard.py"])           



if __name__ == "__main__":
        root = Tk()
        obj = supplierClass(root)
        obj.query_db()
        root.mainloop()