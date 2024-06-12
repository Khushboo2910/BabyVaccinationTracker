import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tkinter import *
from tkinter import ttk, messagebox
from database import add_vaccine, get_vaccines, update_vaccine, delete_vaccine

def center_window(window, width=300, height=200):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 5
    y = (screen_height - height) // 3
    window.geometry(f'{width}x{height}+{x}+{y}')

class VaccineDetailsWindow:
    def __init__(self, root):
        self.root = root
        center_window(root)
        self.root.title("Vaccine Details")
        self.root.geometry("1200x500")

        self.vaccine_id = StringVar()
        self.vaccine_name = StringVar()
        self.description = StringVar()
        self.age_group = IntVar()
        self.dosage = IntVar()
        self.side_effects = StringVar()

        self.vaccine_frame = Frame(self.root, bd=2, relief=RIDGE)
        self.vaccine_frame.place(x=20, y=20, width=1500, height=460)

        self.vaccine_label = Label(self.vaccine_frame, text="Vaccine Name:")
        self.vaccine_label.grid(row=0, column=1, padx=20, pady=10)
        self.vaccine_entry = Entry(self.vaccine_frame, textvariable=self.vaccine_name)
        self.vaccine_entry.grid(row=0, column=2, padx=20, pady=10)

        self.description_label = Label(self.vaccine_frame, text="Description:")
        self.description_label.grid(row=1, column=1, padx=20, pady=10)
        self.description_entry = Entry(self.vaccine_frame, textvariable=self.description)
        self.description_entry.grid(row=1, column=2, padx=20, pady=10)

        self.age_group_label = Label(self.vaccine_frame, text="Age Group:")
        self.age_group_label.grid(row=2, column=1, padx=20, pady=10)
        self.age_group_entry = Entry(self.vaccine_frame, textvariable=self.age_group)
        self.age_group_entry.grid(row=2, column=2, padx=20, pady=10)

        self.dosage_label = Label(self.vaccine_frame, text="Dosage:")
        self.dosage_label.grid(row=3, column=1, padx=20, pady=10)
        self.dosage_entry = Entry(self.vaccine_frame, textvariable=self.dosage)
        self.dosage_entry.grid(row=3, column=2, padx=20, pady=10)

        self.side_effects_label = Label(self.vaccine_frame, text="Side Effects:")
        self.side_effects_label.grid(row=4, column=1, padx=20, pady=10)
        self.side_effects_entry = Entry(self.vaccine_frame, textvariable=self.side_effects)
        self.side_effects_entry.grid(row=4, column=2, padx=20, pady=10)

        self.add_button = Button(self.vaccine_frame, text="Add", command=self.add_vaccine)
        self.add_button.grid(row=5, column=0, padx=20, pady=10)
        self.update_button = Button(self.vaccine_frame, text="Update", command=self.update_vaccine)
        self.update_button.grid(row=5, column=1, padx=20, pady=10)
        self.delete_button = Button(self.vaccine_frame, text="Delete", command=self.delete_vaccine)
        self.delete_button.grid(row=5, column=2, padx=20, pady=10)
        self.clear_button = Button(self.vaccine_frame, text="Clear", command=self.clear_fields)
        self.clear_button.grid(row=5, column=3, padx=20, pady=10)
        self.exit_button = Button(self.vaccine_frame, text="Exit", command=root.quit)
        self.exit_button.grid(row=5, column=4, padx=20, pady=10)

        self.vaccine_tree = ttk.Treeview(self.vaccine_frame, columns=("vaccine_id", "vaccine_name", "description", "age_group", "dosage", "side_effects"))
        self.vaccine_tree.heading("vaccine_id", text="ID")
        self.vaccine_tree.heading("vaccine_name", text="Name")
        self.vaccine_tree.heading("description", text="Description")
        self.vaccine_tree.heading("age_group", text="Age Group")
        self.vaccine_tree.heading("dosage", text="Dosage")
        self.vaccine_tree.heading("side_effects", text="Side Effects")
        self.vaccine_tree["show"] = "headings"
        self.vaccine_tree.grid(row=6, column=0, columnspan=8, padx=30, pady=10)

        self.vaccine_tree.bind("<ButtonRelease-1>", self.get_vaccine)
        self.populate_vaccines()


    def populate_vaccines(self):
        self.vaccine_tree.delete(*self.vaccine_tree.get_children())
        vaccines = get_vaccines()
        for vaccine in vaccines:
            self.vaccine_tree.insert("", "end", values=vaccine)
        

    def add_vaccine(self):
        vaccine_name = self.vaccine_name.get()
        description = self.description.get()
        age_group = self.age_group.get()
        dosage = self.dosage.get()
        side_effects = self.side_effects.get()
        if vaccine_name == "":
            messagebox.showerror("Error", "Please fill in the vaccine name")
            return
        add_vaccine(vaccine_name, description, age_group, dosage, side_effects)
        self.clear_fields()
        self.populate_vaccines()


    def update_vaccine(self):
        selected = self.vaccine_tree.focus()
        if selected:
            data = self.vaccine_tree.item(selected, "values")
            if data:
                vaccine_id = data[0]
                vaccine_name = self.vaccine_name.get()
                description = self.description.get()
                age_group = self.age_group.get()
                dosage = self.dosage.get()
                side_effects = self.side_effects.get()
                if vaccine_name == "":
                    messagebox.showerror("Error", "Please fill in the vaccine name")
                    return
                update_vaccine(vaccine_id, vaccine_name, description, age_group, dosage, side_effects)
                self.clear_fields()
                self.populate_vaccines()
        else:
            messagebox.showerror("Error", "Please select a vaccine to update")


    def delete_vaccine(self):
        selected = self.vaccine_tree.focus()
        if selected:
            confirmation = messagebox.askyesno("Confirm", "Are you sure you want to delete this vaccine?")
            if confirmation:
                data = self.vaccine_tree.item(selected, "values")
                if data:
                    vaccine_id = data[0]
                    delete_vaccine(vaccine_id)
                    self.clear_fields()
                    self.populate_vaccines()
        else:
            messagebox.showerror("Error", "Please select a vaccine to delete")


    def get_vaccine(self, event):
        selected = self.vaccine_tree.focus()
        if selected:
            data = self.vaccine_tree.item(selected, "values")
            if data:
                self.vaccine_name.set(data[1])
                self.description.set(data[2])
                self.age_group.set(data[3])
                self.dosage.set(data[4])
                if len(data) > 5:
                    self.side_effects.set(data[5])
                else:
                    self.side_effects.set("")
            else:
                messagebox.showinfo("No Selection", "Please select a vaccine to view details.")


    def clear_fields(self):
        self.vaccine_name.set("")
        self.description.set("")
        self.age_group.set(0)
        self.dosage.set(0)
        self.side_effects.set("")

def main():
    root = Tk()
    app = VaccineDetailsWindow(root)  
    root.mainloop() 

if __name__ == "__main__":
    main()
