import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import messagebox
import mysql.connector
import hashlib
from mysql.connector import Error
from utils.hashing import hash_password
from database import create_connection, close_connection


def center_window(window, width=300, height=250):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f'{width}x{height}+{x}+{y}')
    

def register_user(root):
    username = entry_username.get()
    password = entry_password.get()
    email = entry_email.get()
    if not username or not password or not email:
        messagebox.showwarning("Input Error", "All fields are required")
        return

    password_hash = hash_password(password)
    conn = create_connection()
    if conn is None:
        messagebox.showerror("Connection Error", "Failed to connect to database")
        return
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password_hash, email) VALUES (%s, %s, %s)",
                       (username, password_hash, email))  
        conn.commit()
        messagebox.showinfo("Success", "User registered successfully!")
        entry_username.delete(0, tk.END)
        entry_password.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        root.destroy()
    except Error as e:
        messagebox.showerror("Error", str(e))
    finally:
        close_connection(conn)


def register_screen():
    global entry_username, entry_password, entry_email
    root = tk.Tk()
    root.title("Register")
    center_window(root)

    heading = tk.Label(root, text="Register", font=("Arial", 20))
    heading.grid(row=0, columnspan=2, pady=20)

    tk.Label(root, text="Username").grid(row=1, column=0, padx=30, pady=5, sticky='e')
    entry_username = tk.Entry(root)
    entry_username.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(root, text="Password").grid(row=2, column=0, padx=30, pady=5, sticky='e')
    entry_password = tk.Entry(root, show="*")
    entry_password.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(root, text="Email").grid(row=3, column=0, padx=30, pady=5, sticky='e')
    entry_email = tk.Entry(root)
    entry_email.grid(row=3, column=1, padx=10, pady=5)

    tk.Button(root, text="Register", command=lambda: register_user(root)).grid(row=4, columnspan=2,pady=20)

    root.mainloop()

if __name__ == "__main__":
    register_screen()
