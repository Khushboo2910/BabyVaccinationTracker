import subprocess
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from after_login import AfterLoginFrame
from baby_vaccination_tracker import BabyVaccinationTrackerApp
from utils.hashing import hash_password
import tkinter as tk
from tkinter import  messagebox
from database import create_connection, close_connection

def center_window(window, width=300, height=200):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f'{width}x{height}+{x}+{y}')
        

def login_user(login_window, app):
    username = entry_username.get()
    password = entry_password.get()
    if not username or not password:
        messagebox.showwarning("Input Error", "All fields are required")
        return

    password_hash = hash_password(password)
    conn = create_connection()
    if conn is None:
        messagebox.showerror("Connection Error", "Failed to connect to database")
        return
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password_hash = %s",
                       (username, password_hash))
        user = cursor.fetchone()
        if user:
            # messagebox.showinfo("Login", "Login Successful")
            login_window.destroy()  
            root.deiconify()
            app = AfterLoginFrame(root)
        else:
            messagebox.showerror("Login", "Invalid Username or Password")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        close_connection(conn)


def login_screen(app):
    global entry_username, entry_password
    root = tk.Tk()
    root.title("Login")
    center_window(root)

    heading = tk.Label(root, text="Login", font=("Arial", 18))
    heading.grid(row=0, columnspan=2, pady=10)

    tk.Label(root, text="Username").grid(row=1, column=0, padx=30, pady=5, sticky='e')
    entry_username = tk.Entry(root)
    entry_username.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(root, text="Password").grid(row=2, column=0, padx=30, pady=5, sticky='e')
    entry_password = tk.Entry(root, show="*")
    entry_password.grid(row=2, column=1, padx=10, pady=5)

    tk.Button(root, text="Login", command=lambda: login_user(root, app)).grid(row=3, columnspan=2, pady=20)


if __name__ == "__main__":
    root = tk.Tk()
    app = AfterLoginFrame(root)
    root.withdraw()
    login_screen(root)
    root.mainloop()

