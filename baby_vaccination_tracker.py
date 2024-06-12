import os
import subprocess
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class BabyVaccinationTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Baby Vaccination Tracker")
        self.root.state('zoomed')  

        self.main_frame = ttk.Frame(root, padding=(20, 10))
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.heading_label = ttk.Label(self.main_frame, text="Baby Vaccination Tracker", font=("Arial", 24, "bold"))
        self.heading_label.pack(pady=10)

        self.canvas = tk.Canvas(self.main_frame, bg="yellow", height=2, width=400)
        self.canvas.pack()

        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        self.add_content()

        self.nav_bar = ttk.Frame(self.main_frame)
        self.nav_bar.pack(fill=tk.X, pady=100)

        self.login_button = ttk.Button(self.nav_bar, text="Login", command=self.open_login)
        self.login_button.pack(side=tk.LEFT, padx=(100, 500))

        self.exit_button = ttk.Button(self.nav_bar, text="Exit", command=self.root.destroy)
        self.exit_button.pack(side=tk.LEFT)

        self.register_button = ttk.Button(self.nav_bar, text="Register", command=self.open_register)
        self.register_button.pack(side=tk.LEFT, padx=(500, 100))

        self.login_frame = None
        self.register_frame = None


    def add_content(self):
        content_label = ttk.Label(self.content_frame, text="Welcome to the Baby Vaccination Tracker!", font=("Arial", 18))
        content_label.pack(pady=20)
        try:
            image = Image.open("image1.jpeg")  
            image = image.resize((300, 300), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            image_label = tk.Label(self.content_frame, image=photo)
            image_label.image = photo
            image_label.pack(pady=10)
        except Exception as e:
            print(f"Error loading image: {e}")

        description = ("This application helps you keep track of your baby's vaccinations.\n"
                       "You can login or register to manage your baby's vaccination records.")
        description_label = ttk.Label(self.content_frame, text=description, font=("Arial", 14), justify=tk.CENTER)
        description_label.pack(pady=20)


    def open_login(self):
        subprocess.Popen(["python", "gui/login.py"], cwd=os.path.dirname(os.path.abspath(__file__)))

    def open_register(self):
        subprocess.Popen(["python", "gui/register.py"], cwd=os.path.dirname(os.path.abspath(__file__)))


def main():
    root = tk.Tk()
    app = BabyVaccinationTrackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
