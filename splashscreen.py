import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk



import subprocess


def main_window():
    splash_root.destroy()
    subprocess.run(["python","sigin.py"])

# Create the splash screen
splash_root = tk.Tk()
splash_root.geometry("1000x600+300+100")
splash_root.overrideredirect(True)


bg_frame = Image.open("Inventify new.jpg")
photo = ImageTk.PhotoImage(bg_frame)
bg_panel = tk.Label(splash_root, image=photo)
bg_panel.image = photo
bg_panel.place(x=0, y=0, width=1000, height=600)


splash_root.after(5000, main_window)

# Start the main loop
splash_root.mainloop()