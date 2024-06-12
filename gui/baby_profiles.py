import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tkinter import *
from tkinter import ttk, messagebox
from database import *

def center_window(window, width=300, height=200):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 5
    y = (screen_height - height) // 4
    window.geometry(f'{width}x{height}+{x}+{y}')

class BabyProfiles:
    def __init__(self, master, user_id):
        self.master = master
        self.user_id = user_id
        self.master.title("Baby Profiles")
        self.master.geometry("1100x450")

        self.frame = Frame(self.master)
        self.frame.pack(fill=BOTH, expand=1)

        self.label = Label(self.frame, text="Baby Profiles", font=("Arial", 18))
        self.label.grid(row=0, column=0, columnspan=5, pady=10)

        self.tree = ttk.Treeview(self.frame, columns=("id", "user_id", "name", "date_of_birth", "gender", "parent_name", "contact_info"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("user_id", text="User ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("date_of_birth", text="Date of Birth")
        self.tree.heading("gender", text="Gender")
        self.tree.heading("parent_name", text="Parent Name")
        self.tree.heading("contact_info", text="Contact Info")

        self.tree.column("id", width=80)
        self.tree.column("user_id", width=150)
        self.tree.column("name", width=150)
        self.tree.column("date_of_birth", width=150)
        self.tree.column("gender", width=150)
        self.tree.column("parent_name", width=150)
        self.tree.column("contact_info", width=150)

        self.tree.grid(row=1, column=0, columnspan=5, padx=40, pady=10, sticky="nsew")

        self.scrollbar = Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.scrollbar.grid(row=1, column=5, sticky='ns')
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.tree.bind("<ButtonRelease-1>", self.get_baby_details)

        self.refresh_treeview()

        self.view_button = Button(self.frame, text="View Baby", command=self.view_baby)
        self.view_button.grid(row=2, column=0, pady=10)

        self.add_button = Button(self.frame, text="Add Baby", command=self.add_baby)
        self.add_button.grid(row=2, column=1, pady=10)

        self.update_button = Button(self.frame, text="Update Baby", command=self.update_baby)
        self.update_button.grid(row=2, column=2, pady=10)

        self.delete_button = Button(self.frame, text="Delete Baby", command=self.delete_baby)
        self.delete_button.grid(row=2, column=3, pady=10)

        self.exit_button = Button(self.frame, text="Exit", command=self.exit_application)
        self.exit_button.grid(row=2, column=4, pady=10)


    def exit_application(self):
        self.master.destroy()


    def refresh_treeview(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        babies = get_babies_by_user(self.user_id)
        for baby in babies:
            self.tree.insert("", END, values=baby)


    def add_baby(self):
        self.add_window = Toplevel(self.master)
        self.add_window.title("Add Baby")
        self.add_window.geometry("300x200")

        self.add_frame = Frame(self.add_window)
        self.add_frame.pack()

        self.name_label = Label(self.add_frame, text="Baby Name:")
        self.name_label.grid(row=0, column=0, pady=5)
        self.name_entry = Entry(self.add_frame)
        self.name_entry.grid(row=0, column=1, pady=5)

        self.dob_label = Label(self.add_frame, text="Date of Birth:")
        self.dob_label.grid(row=1, column=0, pady=5)
        self.dob_entry = Entry(self.add_frame)
        self.dob_entry.grid(row=1, column=1, pady=5)

        self.gender_label = Label(self.add_frame, text="Gender:")
        self.gender_label.grid(row=2, column=0, pady=5)
        self.gender_entry = Entry(self.add_frame)
        self.gender_entry.grid(row=2, column=1, pady=5)

        self.parent_name_label = Label(self.add_frame, text="Parent Name:")
        self.parent_name_label.grid(row=3, column=0, pady=5)
        self.parent_name_entry = Entry(self.add_frame)
        self.parent_name_entry.grid(row=3, column=1, pady=5)

        self.contact_info_label = Label(self.add_frame, text="Contact Info:")
        self.contact_info_label.grid(row=4, column=0, pady=5)
        self.contact_info_entry = Entry(self.add_frame)
        self.contact_info_entry.grid(row=4, column=1, pady=5)

        self.submit_button = Button(self.add_frame, text="Add", command=self.add_baby_to_db)
        self.submit_button.grid(row=5, columnspan=2, pady=10)

        self.add_window.update_idletasks()
        screen_width = self.add_window.winfo_screenwidth()
        screen_height = self.add_window.winfo_screenheight()
        window_width = 300
        window_height = 200
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.add_window.geometry(f'{window_width}x{window_height}+{x}+{y}')


    def add_baby_to_db(self):
        baby_name = self.name_entry.get()
        date_of_birth = self.dob_entry.get()
        gender = self.gender_entry.get()
        parent_name = self.parent_name_entry.get()
        contact_info = self.contact_info_entry.get()

        if baby_name and date_of_birth and gender and parent_name and contact_info:
            add_baby(self.user_id, baby_name, date_of_birth, gender)
            babies = get_babies_by_user(self.user_id)
            if not babies:
                messagebox.showerror("Error", "Could not retrieve the new baby ID.")
                return
            new_baby_id = max([baby[0] for baby in babies])
            add_baby_detail(new_baby_id, baby_name, date_of_birth, parent_name, contact_info)
            self.refresh_treeview()
            self.add_window.destroy()
        else:
            messagebox.showerror("Error", "Please fill in all fields.")


    def get_baby_details(self, baby_id): 
        conn = create_connection()
        baby_details = None
        if conn:
            try:
                cursor = conn.cursor()
                query = "SELECT b.baby_name, b.date_of_birth, b.gender, d.parent_name, d.contact_info FROM babies b LEFT JOIN baby_detail d ON b.baby_id = d.baby_id WHERE b.baby_id = %s"
                cursor.execute(query, (baby_id,))
                baby_details = cursor.fetchone()
            except mysql.connector.Error as err:
                print(f"Error: {err}")
            finally:
                close_connection(conn)
        return baby_details


    def view_baby(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "No baby selected")
            return
        
        baby_id = self.tree.item(selected_item)["values"][0]
        baby_details = self.get_baby_details(baby_id)
        if baby_details:
            detail_string = (f"Name: {baby_details[0]}\n"
                             f"Date of Birth: {baby_details[1]}\n"
                             f"Gender: {baby_details[2]}\n"
                             f"Parent Name: {baby_details[3]}\n"
                             f"Contact Info: {baby_details[4]}")
            messagebox.showinfo("Baby Details", detail_string)
        else:
            messagebox.showinfo("Error", "Failed to retrieve baby details")


    def update_baby(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "No baby selected")
            return

        baby_id = self.tree.item(selected_item)["values"][0]
        baby_details = self.get_baby_details(baby_id)
        if baby_details:
            self.update_window = Toplevel(self.master)
            self.update_window.title("Update Baby")
            # self.update_window.geometry("300x200")

            self.update_frame = Frame(self.update_window)
            self.update_frame.pack()

            self.name_label = Label(self.update_frame, text="Baby Name:")
            self.name_label.grid(row=0, column=0, pady=5)
            self.name_entry = Entry(self.update_frame)
            self.name_entry.insert(0, baby_details[0])
            self.name_entry.grid(row=0, column=1, pady=5)

            self.dob_label = Label(self.update_frame, text="Date of Birth:")
            self.dob_label.grid(row=1, column=0, pady=5)
            self.dob_entry = Entry(self.update_frame)
            self.dob_entry.insert(0, baby_details[1])
            self.dob_entry.grid(row=1, column=1, pady=5)

            self.gender_label = Label(self.update_frame, text="Gender:")
            self.gender_label.grid(row=2, column=0, pady=5)
            self.gender_entry = Entry(self.update_frame)
            self.gender_entry.insert(0, baby_details[2])
            self.gender_entry.grid(row=2, column=1, pady=5)

            self.parent_name_label = Label(self.update_frame, text="Parent Name:")
            self.parent_name_label.grid(row=3, column=0, pady=5) 
            self.parent_name_entry = Entry(self.update_frame)
            self.parent_name_entry.insert(0, baby_details[3])
            self.parent_name_entry.grid(row=3, column=1, pady=5)

            self.contact_info_label = Label(self.update_frame, text="Contact Info:")
            self.contact_info_label.grid(row=4, column=0, pady=5)
            self.contact_info_entry = Entry(self.update_frame)
            self.contact_info_entry.insert(0, baby_details[4])
            self.contact_info_entry.grid(row=4, column=1, pady=5)

            self.submit_button = Button(self.update_frame, text="Update", command=lambda: self.update_baby_in_db(baby_id))
            self.submit_button.grid(row=5, columnspan=2, pady=10)

            # center_window(self.update_window)
            self.update_window.update_idletasks()
            screen_width = self.update_window.winfo_screenwidth()
            screen_height = self.update_window.winfo_screenheight()
            window_width = 300
            window_height = 200
            x = (screen_width // 2) - (window_width // 2)
            y = (screen_height // 2) - (window_height // 2)
            self.update_window.geometry(f'{window_width}x{window_height}+{x}+{y}')
        else:
            messagebox.showerror("Error", "Failed to retrieve baby details")


    def update_baby_in_db(self, baby_id):
        baby_name = self.name_entry.get()
        date_of_birth = self.dob_entry.get()
        gender = self.gender_entry.get()
        parent_name = self.parent_name_entry.get()
        contact_info = self.contact_info_entry.get()
        if baby_name and date_of_birth and gender and parent_name and contact_info:
            update_baby(baby_id, baby_name, date_of_birth, gender)
            update_baby_detail(baby_id, baby_name, date_of_birth, parent_name, contact_info)
            self.refresh_treeview()
            self.update_window.destroy()
        else:
            messagebox.showerror("Error", "Please fill in all fields.")


    def delete_baby(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "No baby selected")
            return
        
        confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete this baby?")
        if confirmation:
            baby_id = self.tree.item(selected_item)["values"][0]
            delete_baby(baby_id)
            self.refresh_treeview()


if __name__ == "__main__":
    root = Tk()
    center_window(root)
    user_id = 1  
    app = BabyProfiles(root, user_id)
    root.mainloop()

