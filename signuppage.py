from tkinter import *
from tkinter import messagebox
import ast
import sqlite3
import tkinter as tk
import subprocess


window=Tk()
window.title("SignUp")
window.geometry("925x500+200+200")
window.configure(bg='#fff')


def signup():
     username=user.get()
     password=code.get()
     confirm_password=confirm_code.get()

     if password==confirm_password:        
         
             conn = sqlite3.connect('data.db')
             table_create_query = '''CREATE TABLE IF NOT EXISTS User_data(username TEXT, password TEXT,confirm_password TEXT)'''
             conn.execute(table_create_query)
             data_insert = '''INSERT INTO User_data(username,password,confirm_password) VALUES(?,?,?)'''
             data_tuple = (username,password,confirm_password)
             cursor = conn.cursor()
             cursor.execute(data_insert, data_tuple)
             conn.commit()
             conn.close()

    
             messagebox.showinfo("Success", "User account has been created.")

    
             user.delete(0, tk.END)
             user.insert(0, 'Username')
             code.delete(0, tk.END)
             code.insert(0, 'Password')
             code.config(show='')
             confirm_code.delete(0, tk.END)
             confirm_code.insert(0, 'Confirm Password')
             confirm_code.config(show='')     
             

     else:
         messagebox.showerror('Invalid',"Both Password should match")

                 


img=PhotoImage(file='C:\\Users\\ACER\\IdeaProjects\\login.png')
Label(window,image=img,border=0,bg='white').place(x=50,y=90)

frame=Frame(window,width=350,height=390,bg='#fff')
frame.place(x=480,y=50)


heading=Label(frame,text='Sign up',fg="#57a1f8",bg='white',font=('Microsoft Yahei UI Light',23,'bold'))
heading.place(x=100,y=5)

#-------------------------------------------------------------------------
def on_enter(e):
    user.delete(0,'end')
def on_leave(e):
    if user.get()=='':
        user.insert(0,'Username')

user = Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light',11))
user.place(x=30,y=80)
user.insert(0, 'Username')
user.bind("<FocusIn>",on_enter)
user.bind("<FocusOut>",on_leave)

Frame(frame,width=295,height=2,bg='black').place(x=25,y=107)

#-------------------------------------------------------------------------------------
def on_enter(event, entry_widget):
    if entry_widget.get() == 'Password':
        entry_widget.delete(0, tk.END)
    entry_widget.config(show='*')  # Show asterisks for entered text

def on_leave(event, entry_widget):
    if not entry_widget.get():
        entry_widget.insert(0, 'Password')
        entry_widget.config(show='')  # Show the placeholder text


def signin():
    window.destroy()
    subprocess.run(["python","C:\\Users\\ACER\\IdeaProjects\\sigin.py"])



# Usage in the Entry widget
code = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft Yahei UI Light', 11), show='')
code.place(x=30, y=150)
code.insert(0, 'Password')
code.bind("<FocusIn>", lambda event: on_enter(event, code))
code.bind("<FocusOut>", lambda event: on_leave(event, code))


Frame(frame,width=295,height=2,bg='black').place(x=25,y=177)

#---------------------------------------------------------------------------------------------
def on_enter(event, entry_widget):
    if entry_widget.get() == 'Confirm Password':
        entry_widget.delete(0, tk.END)
    entry_widget.config(show='*')  # Show asterisks for entered text

def on_leave(event, entry_widget):
    if not entry_widget.get():
        entry_widget.insert(0, 'Confirm Password')
        entry_widget.config(show='')  # Show the placeholder text

# Usage in the Entry widget
confirm_code = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft Yahei UI Light', 11), show='')
confirm_code.place(x=30, y=220)
confirm_code.insert(0, 'Confirm Password')
confirm_code.bind("<FocusIn>", lambda event: on_enter(event, confirm_code))
confirm_code.bind("<FocusOut>", lambda event: on_leave(event, confirm_code))

Frame(frame,width=295,height=2,bg='black').place(x=25,y=247)

#--------------------------------------------------------------------------

Button(frame,width=39,pady=7,text='Sign up',bg='#57a1f8',fg='white',border=0,command=signup).place(x=35,y=280)
label=Label(frame,text='I have an account',fg='black',bg='white',font=('Microsoft Yahei UI Light',9))
label.place(x=90,y=340)

signin=Button(frame,width=6,text='Sign in',border=0,bg='white',cursor='hand2',fg='#57a1f8',command=signin)
signin.place(x=200,y=340)                                                                                  
window.mainloop()