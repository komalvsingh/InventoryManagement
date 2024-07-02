from tkinter import *
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3

import subprocess

class LoginClass:
    
    def __init__(self, root):
        
        self.root = root
        self.root.title('Login')
        self.root.geometry('1350x700')
        self.root.configure(bg='#fff')
        

        # Load background image
        self.bg_frame = Image.open("bg-image.png")
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = Label(self.root, image=photo)
        self.bg_panel.image = photo
        self.bg_panel.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Login frame
        self.lgn_frame = Frame(self.root, bg='#1F2544')
        self.lgn_frame.place(relx=0.3, rely=0.2, relwidth=0.4, relheight=0.6)

        self.heading = Label(self.lgn_frame, text='Login', bg='#1F2544', fg='white', font=('Microsoft YaHei UI Bold', 30, 'bold'))
        self.heading.place(relx=0.18, rely=0.07)

        # Username input
        self.user_lbl = Label(self.lgn_frame, text='Username', bg='#1F2544', fg='white', font=('Microsoft YaHei UI Light', 20))
        self.user_lbl.place(relx=0.05, rely=0.25)
        self.user_entry = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, fg='white', bg='#1F2544', font=('Microsoft YaHei UI Light', 15))
        self.user_entry.place(relx=0.05, rely=0.35, relwidth=0.9)
        Frame(self.lgn_frame, bg='white').place(relx=0.05, rely=0.42, relwidth=0.9, relheight=0.001)

        # Password input
        self.pass_lbl = Label(self.lgn_frame, text='Password', bg='#1F2544', fg='white', font=('Microsoft YaHei UI Light', 20))
        self.pass_lbl.place(relx=0.05, rely=0.5)
        self.pass_entry = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, fg='white', bg='#1F2544', font=('Microsoft YaHei UI Light', 15), show='*')
        self.pass_entry.place(relx=0.05, rely=0.6, relwidth=0.9)
        Frame(self.lgn_frame, bg='white').place(relx=0.05, rely=0.67, relwidth=0.9, relheight=0.001)

        # Login button
        self.login_btn = Button(self.lgn_frame, text='Login', cursor='hand2', bg='#6C22A6', fg='white', font=('Microsoft YaHei UI Bold', 13, 'bold'),command=self.login)
        self.login_btn.place(relx=0.3, rely=0.75, relwidth=0.4, relheight=0.1)
        
        # Sign up button
        self.dont_have_an_acc = Label(self.lgn_frame, text="Don't have an account?", fg='white', bg='#1F2544', font=('Microsoft YaHei UI Light', 12))
        self.dont_have_an_acc.place(relx=0.15, rely=0.9)
        self.sign_up_btn = Button(self.lgn_frame, text='Sign up', cursor='hand2', bg='#1F2544', fg='#9F70FD',border=0, font=('Microsoft YaHei UI Light', 12),command=self.signup)
        self.sign_up_btn.place(relx=0.6, rely=0.9)

        # Configure grid for responsiveness
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.lgn_frame.grid_rowconfigure(0, weight=1)
        self.lgn_frame.grid_columnconfigure(0, weight=1)

        # conn = sqlite3.connect('data.db')
        # cursor = conn.cursor()


    def login(self):
        username = self.user_entry.get()
        password = self.pass_entry.get()

    # Connect to the database
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

    # Query the database to check if the username and password combination exists
        cursor.execute("SELECT * FROM User_data WHERE username=? AND password=?", (username, password))
        user_data = cursor.fetchone()

        if user_data:
            messagebox.showinfo("Success", "Logged in Successfully")
        # Clear the login form fields
            self.user_entry.delete(0, tk.END)
            self.pass_entry.delete(0, tk.END)
            
            self.root.destroy() 
            subprocess.run(["python","C:\\Users\\ACER\\IdeaProjects\\dashboard.py"])
        else:
             messagebox.showerror("Error", "Invalid Username or Password")

    # Close the database connection
        conn.close()


    # def open_dashboard(self):
    #     subprocess.run(["python","dashboard.py"])    


    def signup(self):
        self.root.destroy()
        subprocess.run(["python","C:\\Users\\ACER\\IdeaProjects\\signuppage.py"])



        
             

if __name__ == "__main__":
    root = Tk()
    obj = LoginClass(root)
    root.mainloop()
