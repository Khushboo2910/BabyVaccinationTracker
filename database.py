from tkinter import messagebox
import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234',
            database='vaccination_db'
        )
        if connection.is_connected():
            print("Connected to MySQL database")
        return connection
    except Error as e:
        messagebox.showerror("Error", "while connecting to MySQL")
    return None

def close_connection(connection):
    if connection.is_connected():
        connection.close()
        print("Connection closed")

#///////////////////////////////////////
def add_user(username, password):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            messagebox.showinfo("Success", "User registered successfully!")
        except Error as e:
            messagebox.showerror("Error", "Failed to register user")
        finally:
            close_connection(conn)

def get_user(username):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            return user
        except Error as e:
            messagebox.showerror("Error", "Failed to fetch user details")
        finally:
            close_connection(conn)
    return None

def get_users():
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM users")
            users = cursor.fetchall()
            user_ids = [user[0] for user in users]
            return user_ids
        except Error as e:
            messagebox.showerror("Error", "Failed to fetch users")
        finally:
            close_connection(conn)
    return []

#/////////////////////////////////////////////
# baby_detail
def get_babies_by_user(user_id):
    conn = create_connection()
    babies = []
    if conn:
        try:
            cursor = conn.cursor()
            query = """SELECT b.baby_id, b.user_id, b.baby_name, b.date_of_birth, b.gender, d.parent_name, d.contact_info 
                FROM babies b
                LEFT JOIN baby_detail d ON b.baby_id = d.baby_id
                WHERE b.user_id = %s
            """
            cursor.execute(query, (user_id,))
            results = cursor.fetchall()
            return results
        except mysql.connector.Error as err:
            messagebox.showerror("Error", "Failed to fetch babies record by id")
        finally:
            close_connection(conn)
        return babies

def add_baby(user_id, baby_name, date_of_birth, gender):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO babies (user_id, baby_name, date_of_birth,gender) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (user_id, baby_name, date_of_birth , gender))
            conn.commit()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", "Failed to add baby record")
        finally:
            close_connection(conn)

def update_baby(baby_id, baby_name, date_of_birth, gender):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "UPDATE babies SET baby_name = %s, date_of_birth = %s, gender = %s WHERE baby_id = %s"
            cursor.execute(query, (baby_name, date_of_birth, gender, baby_id))
            conn.commit()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", "Failed to update baby record")
        finally:
            close_connection(conn)

def delete_baby(baby_id):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "DELETE FROM babies WHERE baby_id = %s"
            cursor.execute(query, (baby_id,))
            conn.commit()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", "Failed to delete baby record")
        finally:
            close_connection(conn)

def get_babies():
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT baby_id FROM babies")
            result = cursor.fetchall()
            return result
        except Error as e:
            messagebox.showerror("Error", "Failed to fetch babies record")     
            return None
        finally:
            close_connection(conn)
    return None

def get_baby_details(baby_id):
    conn = create_connection()
    baby_details = None
    if conn:
        try:
            cursor = conn.cursor()
            query = "SELECT baby_name, date_of_birth, gender, parent_name, contact_info FROM baby_detail WHERE baby_id = %s"
            cursor.execute(query, (baby_id,))
            baby_details = cursor.fetchone()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", "Failed to fetch baby detail")
        finally:
            close_connection(conn)
    return baby_details

def add_baby_detail(baby_id, baby_name, date_of_birth, parent_name, contact_info):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO baby_detail (baby_id, baby_name, date_of_birth, parent_name, contact_info) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (baby_id, baby_name, date_of_birth, parent_name, contact_info))
            conn.commit()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", "Failed to add baby detail")
        finally:
            close_connection(conn)


def update_baby_detail(baby_id, baby_name, date_of_birth, parent_name, contact_info):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "UPDATE baby_detail SET baby_name = %s, date_of_birth = %s, parent_name = %s, contact_info = %s WHERE baby_id = %s"
            cursor.execute(query, (baby_name, date_of_birth, parent_name, contact_info, baby_id))
            conn.commit()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", "Failed to update baby detail")
        finally:
            close_connection(conn)


def delete_baby_detail(baby_id):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "DELETE FROM baby_detail WHERE baby_id = %s"
            cursor.execute(query, (baby_id,))
            conn.commit()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", "Failed to delete baby detail")
        finally:
            close_connection(conn)

#///////////////////////////////////////////////
# vaccine_detail
def add_vaccine(vaccine_name, description, age_group, dosage, side_effects):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO vaccine_detail (vaccine_name, description, age_group, dosage, side_effects) VALUES (%s, %s, %s, %s, %s)",
                           (vaccine_name, description, age_group, dosage, side_effects))
            conn.commit()
        except Error as e:
            messagebox.showerror("Error", "Failed to add vaccine detail")
        finally:
            close_connection(conn)

# Function to retrieve all vaccines from the database
def get_vaccines():
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM vaccine_detail")
            result = cursor.fetchall()
            return result
        except Error as e:
            messagebox.showerror("Error", "Failed to add vaccination record")
        finally:
            close_connection(conn)
    return []

# Function to update an existing vaccine in the database
def update_vaccine(vaccine_id, vaccine_name, description, age_group, dosage, side_effects):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE vaccine_detail SET vaccine_name = %s, description = %s, age_group = %s, dosage = %s, side_effects = %s WHERE vaccine_id = %s",
                           (vaccine_name, description, age_group, dosage, side_effects, vaccine_id))
            conn.commit()
        except Error as e:
            messagebox.showerror("Error", "Failed to update vaccination record")
        finally:
            close_connection(conn)

# Function to delete a vaccine from the database
def delete_vaccine(vaccine_id):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM vaccine_detail WHERE vaccine_id = %s", (vaccine_id,))
            conn.commit()
        except Error as e:
            print("Error:", str(e))
        finally:
            close_connection(conn)


# Vaccination
def get_vaccines():
    conn = create_connection()
    if conn is None:
        print("Failed to connect to the database")
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vaccine_detail")
        result = cursor.fetchall()
        return result
    except Error as e:
        messagebox.showerror("Error", "Failed to get vaccination record")
    finally:
        close_connection(conn)
    return []


def check_baby_exists(baby_id):
    conn = create_connection()
    cursor = conn.cursor()
    query = "SELECT COUNT(*) FROM babies WHERE baby_id = %s"
    cursor.execute(query, (baby_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] > 0


def add_vaccination_record(baby_id, vaccine_id, scheduled_date, administered_date, notes):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM babies WHERE baby_id = %s", (baby_id,))
            if cursor.fetchone()[0] == 0:
                raise ValueError(f"Baby ID {baby_id} does not exist.")
            
            cursor.execute("SELECT COUNT(*) FROM vaccine_detail WHERE vaccine_id = %s", (vaccine_id,))
            if cursor.fetchone()[0] == 0:
                raise ValueError(f"Vaccine ID {vaccine_id} does not exist.")
            
            cursor.execute(
                "INSERT INTO vaccinations (baby_id, vaccine_id, scheduled_date, administered_date, notes) VALUES (%s, %s, %s, %s, %s)",
                (baby_id, vaccine_id, scheduled_date, administered_date, notes)
            )
            conn.commit()
            messagebox.showinfo("Success", "Vaccination record added successfully!")
        except Error as e:
            messagebox.showerror("Error", "Failed to add vaccination record")
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
        finally:
            close_connection(conn)


def get_vaccination_records(baby_id):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM vaccinations WHERE baby_id = %s", (baby_id,))
            records = cursor.fetchall()
            return records
        except Error as e:
            messagebox.showerror("Error", "Failed to fetch vaccination records")
        finally:
            close_connection(conn)
    return []

def update_vaccination_record(vaccination_id, baby_id, vaccine_id, scheduled_date, administered_date, notes):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE vaccinations SET baby_id = %s, vaccine_id = %s, scheduled_date = %s, administered_date = %s, notes = %s WHERE vaccination_id = %s",
                           (baby_id, vaccine_id, scheduled_date, administered_date, notes, vaccination_id))
            conn.commit()
            messagebox.showinfo("Success", "Vaccination record updated successfully!")
        except Error as e:
            messagebox.showerror("Error", "Failed to update vaccination record")
        finally:
            close_connection(conn)

def delete_vaccination_record(vaccination_id):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM vaccinations WHERE vaccination_id = %s", (vaccination_id,))
            conn.commit()
            messagebox.showinfo("Success", "Vaccination record deleted successfully!")
        except Error as e:
            messagebox.showerror("Error", "Failed to delete vaccination record")
        finally:
            close_connection(conn)


