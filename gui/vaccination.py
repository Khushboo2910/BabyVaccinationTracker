import sys
import os
from tkinter import *
from tkinter import ttk, messagebox
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database import add_vaccination_record, get_vaccination_records, update_vaccination_record, delete_vaccination_record, get_vaccines, check_baby_exists

def center_window(window, width=300, height=200):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 5
    y = (screen_height - height) // 4
    window.geometry(f'{width}x{height}+{x}+{y}')

class VaccinationWindow:
    def __init__(self, root, baby_id):
        self.root = root
        self.baby_id = baby_id

        self.root.title("Vaccination Records")
        self.root.geometry("1100x500")

        self.vaccine_id = StringVar()
        self.scheduled_date = StringVar()
        self.administered_date = StringVar()
        self.notes = StringVar()
        self.vaccine_dict = {}

        self.vaccination_frame = Frame(self.root, bd=2, relief=RIDGE)
        self.vaccination_frame.place(x=20, y=20, width=1050, height=460)

        self.vaccine_label = Label(self.vaccination_frame, text="Vaccine:")
        self.vaccine_label.grid(row=0, column=0, padx=20, pady=10)
        self.vaccine_entry = ttk.Combobox(self.vaccination_frame, textvariable=self.vaccine_id, state="readonly")
        self.vaccine_entry.grid(row=0, column=1, padx=20, pady=10)

        self.populate_vaccine_combobox()

        self.scheduled_label = Label(self.vaccination_frame, text="Scheduled Date:")
        self.scheduled_label.grid(row=1, column=0, padx=20, pady=10)
        self.scheduled_entry = Entry(self.vaccination_frame, textvariable=self.scheduled_date)
        self.scheduled_entry.grid(row=1, column=1, padx=20, pady=10)

        self.administered_label = Label(self.vaccination_frame, text="Administered Date:")
        self.administered_label.grid(row=2, column=0, padx=20, pady=10)
        self.administered_entry = Entry(self.vaccination_frame, textvariable=self.administered_date)
        self.administered_entry.grid(row=2, column=1, padx=20, pady=10)

        self.notes_label = Label(self.vaccination_frame, text="Notes:")
        self.notes_label.grid(row=3, column=0, padx=20, pady=10)
        self.notes_entry = Entry(self.vaccination_frame, textvariable=self.notes)
        self.notes_entry.grid(row=3, column=1, padx=20, pady=10)

        self.add_button = Button(self.vaccination_frame, text="Add", command=self.add_vaccination)
        self.add_button.grid(row=4, column=0, padx=20, pady=10)
        self.update_button = Button(self.vaccination_frame, text="Update", command=self.update_vaccination)
        self.update_button.grid(row=4, column=1, padx=20, pady=10)
        self.delete_button = Button(self.vaccination_frame, text="Delete", command=self.delete_vaccination)
        self.delete_button.grid(row=4, column=2, padx=20, pady=10)
        self.clear_button = Button(self.vaccination_frame, text="Clear", command=self.clear_fields)
        self.clear_button.grid(row=4, column=3, padx=20, pady=10)
        self.exit_button = Button(self.vaccination_frame, text="Exit", command=self.root.quit)
        self.exit_button.grid(row=4, column=4, padx=20, pady=10)

        self.vaccination_tree = ttk.Treeview(self.vaccination_frame, columns=("vaccination_id", "vaccine_id", "scheduled_date", "administered_date", "notes"))
        self.vaccination_tree.heading("vaccination_id", text="ID")
        self.vaccination_tree.heading("vaccine_id", text="Vaccine")
        self.vaccination_tree.heading("scheduled_date", text="Scheduled Date")
        self.vaccination_tree.heading("administered_date", text="Administered Date")
        self.vaccination_tree.heading("notes", text="Notes")
        self.vaccination_tree["show"] = "headings"
        self.vaccination_tree.grid(row=5, column=0, columnspan=5, padx=20, pady=10, sticky="nsew")

        self.vaccination_tree.bind("<ButtonRelease-1>", self.get_vaccination)
        self.populate_vaccinations()


    def populate_vaccine_combobox(self):
        vaccines = get_vaccines()
        self.vaccine_dict = {vaccine[1]: vaccine[0] for vaccine in vaccines} 
        vaccine_names = list(self.vaccine_dict.keys())
        self.vaccine_entry['values'] = vaccine_names


    def populate_vaccinations(self):
        self.vaccination_tree.delete(*self.vaccination_tree.get_children())
        vaccinations = get_vaccination_records(self.baby_id)
        for vaccination in vaccinations:
            vaccine_name = next((name for name, vid in self.vaccine_dict.items() if vid == vaccination[2]), vaccination[2])
            self.vaccination_tree.insert("", "end", values=(vaccination[0], vaccine_name, vaccination[3], vaccination[4], vaccination[5])) 


    def add_vaccination(self):
        vaccine_name = self.vaccine_id.get()
        scheduled_date = self.scheduled_date.get()
        administered_date = self.administered_date.get()
        notes = self.notes.get()
        if vaccine_name == "" or scheduled_date == "":
            messagebox.showerror("Error", "Please fill in all required fields")
            return
        vaccine_id = self.vaccine_dict.get(vaccine_name)
        add_vaccination_record(self.baby_id, vaccine_id, scheduled_date, administered_date, notes)
        self.clear_fields()
        self.populate_vaccinations()


    def update_vaccination(self):
        selected = self.vaccination_tree.focus()
        if selected:
            data = self.vaccination_tree.item(selected, "values")
            if data:
                vaccination_id = data[0]
                vaccine_name = self.vaccine_id.get()
                scheduled_date = self.scheduled_date.get()
                administered_date = self.administered_date.get()
                notes = self.notes.get()
                if vaccine_name == "" or scheduled_date == "":
                    messagebox.showerror("Error", "Please fill in all required fields")
                    return
                vaccine_id = self.vaccine_dict.get(vaccine_name)
                update_vaccination_record(vaccination_id, self.baby_id, vaccine_id, scheduled_date, administered_date, notes)
                self.clear_fields()
                self.populate_vaccinations()
        else:
            messagebox.showerror("Error", "Please select a vaccination record to update")


    def delete_vaccination(self):
        selected = self.vaccination_tree.focus()
        if selected:
            confirmation = messagebox.askyesno("Confirm", "Are you sure you want to delete this vaccination record?")
            if confirmation:
                data = self.vaccination_tree.item(selected, "values")
                if data:
                    vaccination_id = data[0]
                    delete_vaccination_record(vaccination_id)
                    self.clear_fields()
                    self.populate_vaccinations()
        else:
            messagebox.showerror("Error", "Please select a vaccination record to delete")


    def get_vaccination(self, event):
        selected = self.vaccination_tree.focus()
        if selected:
            data = self.vaccination_tree.item(selected, "values")
            if data:
                self.vaccine_id.set(data[1])
                self.scheduled_date.set(data[2])
                self.administered_date.set(data[3])
                self.notes.set(data[4])


    def clear_fields(self):
        self.vaccine_id.set("")
        self.scheduled_date.set("")
        self.administered_date.set("")
        self.notes.set("")


def main():
    baby_id = 1  
    if check_baby_exists(baby_id):
        root = Tk()
        app = VaccinationWindow(root, baby_id)
        root.mainloop()
    else:
        messagebox.showerror("Error", "Baby ID does not exist")

if __name__ == "__main__":
    root = Tk()
    center_window(root)
    baby_id = 1  
    app = VaccinationWindow(root, baby_id)
    root.mainloop()
