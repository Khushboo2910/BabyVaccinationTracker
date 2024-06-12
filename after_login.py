import tkinter as tk
from tkinter import ttk
import subprocess
import os

def center_window(window, width=300, height=200):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 18
    y = (screen_height - height) // 13
    window.geometry(f'{width}x{height}+{x}+{y}')

class AfterLoginFrame:
    def __init__(self, root):
        self.root = root
        center_window(root)
        self.child_process = None
        self.root.title("After Login")
        self.root.geometry("400x300")

        self.canvas = tk.Canvas(self.root, bg="yellow", height=2, width=400)
        self.canvas.pack()

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=50)

        self.baby_info_button = ttk.Button(self.button_frame, text="Baby Information", command=self.open_baby_profile)
        self.baby_info_button.pack(pady=10)

        self.vaccination_info_button = ttk.Button(self.button_frame, text="Vaccination Information", command=self.open_vaccination)
        self.vaccination_info_button.pack(pady=10)

        self.vaccine_info_button = ttk.Button(self.button_frame, text="Vaccine Information", command=self.open_vaccine_detail)
        self.vaccine_info_button.pack(pady=10)

        self.exit_button = ttk.Button(self.button_frame, text="Exit", command=self.exit_application)
        self.exit_button.pack(pady=10)

    def close_child_process(self):
        if self.child_process and self.child_process.poll() is None:
            self.child_process.terminate()

    def open_baby_profile(self):
        self.close_child_process()
        self.child_process = subprocess.Popen(["python", "gui/baby_profiles.py"], cwd=os.path.dirname(os.path.abspath(__file__)))

    def open_vaccination(self):
        self.close_child_process()
        self.child_process = subprocess.Popen(["python", "gui/vaccination.py"], cwd=os.path.dirname(os.path.abspath(__file__)))

    def open_vaccine_detail(self):
        self.close_child_process()
        self.child_process = subprocess.Popen(["python", "gui/vaccine_detail.py"], cwd=os.path.dirname(os.path.abspath(__file__)))

    def exit_application(self):
        self.close_child_process()
        self.root.destroy()


def open_after_login():
    root = tk.Tk()
    after_login_frame = AfterLoginFrame(root)
    root.mainloop()

