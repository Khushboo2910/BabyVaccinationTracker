# # import tkinter as tk
# # from gui import login
# # from gui.login import login_screen
# # from gui.register import register_screen
# # from gui.baby_profiles import add_baby_profile, view_baby_profiles



# # def main_menu(user_id):
# #     root = tk.Tk()
# #     root.title("Baby Vaccination Tracker")

# #     tk.Button(root, text="Add Baby Profile", command=lambda: add_baby_profile(user_id)).pack()
# #     tk.Button(root, text="View Baby Profiles", command=lambda: view_baby_profiles(user_id)).pack()

# #     root.mainloop()

# # if __name__ == "__main__":
# #     # Assuming login_screen() returns the user_id if login is successful
# #     user_id = login
# # #



# CREATE TABLE users (
#     user_id INT AUTO_INCREMENT PRIMARY KEY,
#     username VARCHAR(255) NOT NULL UNIQUE,
#     password_hash VARCHAR(255) NOT NULL,
#     email VARCHAR(255) NOT NULL UNIQUE,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );



# CREATE TABLE baby_detail (
#     baby_id INT AUTO_INCREMENT PRIMARY KEY,
#     baby_name VARCHAR(255) NOT NULL,
#     date_of_birth DATE NOT NULL,
#     parent_name VARCHAR(255),
#     contact_info VARCHAR(255)
# );



# CREATE TABLE babies (
#     baby_id INT AUTO_INCREMENT PRIMARY KEY,
#     user_id INT,
#     baby_name VARCHAR(255) NOT NULL,
#     date_of_birth DATE NOT NULL,
#     gender VARCHAR(10) NOT NULL,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     FOREIGN KEY (user_id) REFERENCES users(user_id)
# );


# CREATE TABLE vaccine_detail (
#     vaccine_id INT AUTO_INCREMENT PRIMARY KEY,
#     vaccine_name VARCHAR(255) NOT NULL,
#     description TEXT,
#     age_group VARCHAR(50),
#     dosage VARCHAR(50),
#     side_effects TEXT
# );


# CREATE TABLE vaccinations (
#     vaccination_id INT AUTO_INCREMENT PRIMARY KEY,
#     baby_id INT,
#     vaccine_id INT,
#     scheduled_date DATE NOT NULL,
#     administered_date DATE,
#     notes TEXT,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     FOREIGN KEY (baby_id) REFERENCES babies(baby_id),
#     FOREIGN KEY (vaccine_id) REFERENCES vaccine_detail(vaccine_id)
# );





# database.py
#////////////////////////////////////////////
# # Function to retrieve all babies from the database
# def get_all_babies():
#     conn = create_connection()
#     if conn is None:
#         print("Failed to connect to the database")
#         return []
#     try:
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM baby_detail")
#         babies = cursor.fetchall()
#         return babies
#     except Error as e:
#         print("Error:", e)
#         return []
#     finally:
#         close_connection(conn)


# # Function to retrieve baby details by ID
# def get_baby_by_id(baby_id):
#     conn = create_connection()
#     if conn is None:
#         print("Failed to connect to the database")
#         return None
#     try:
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM baby_detail WHERE baby_id = %s", (baby_id,))
#         baby = cursor.fetchone()
#         return baby
#     except Error as e:
#         print("Error:", e)
#         return None
#     finally:
#         close_connection(conn)

# # Function to retrieve baby details by NAME
# def get_baby_by_name(baby_name):
#     conn = create_connection()
#     if conn:
#         try:
#             cursor = conn.cursor()
#             cursor.execute("SELECT * FROM baby_detail WHERE baby_name = %s", (baby_name,))
#             baby = cursor.fetchone()
#             return baby
#         except Error as e:
#             print(f"Error: {e}")
#             messagebox.showerror("Error", "Failed to fetch baby details")
#         finally:
#             close_connection(conn)
#     return None


