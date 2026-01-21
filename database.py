import sqlite3
import os

class Database:
    def __init__(self, db_name="ims_records.db"):
        self.db_name = db_name
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def init_db(self):
        """Initialize the database and create the teachers table if it doesn't exist."""
        query = """
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT,
            department TEXT,
            phone TEXT,
            address TEXT
        )
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        conn.close()

    def add_record(self, first_name, last_name, email, department, phone, address):
        query = "INSERT INTO teachers (first_name, last_name, email, department, phone, address) VALUES (?, ?, ?, ?, ?, ?)"
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (first_name, last_name, email, department, phone, address))
        conn.commit()
        conn.close()

    def fetch_records(self):
        query = "SELECT * FROM teachers"
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        conn.close()
        return records

    def update_record(self, record_id, first_name, last_name, email, department, phone, address):
        query = """
        UPDATE teachers 
        SET first_name = ?, last_name = ?, email = ?, department = ?, phone = ?, address = ? 
        WHERE id = ?
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (first_name, last_name, email, department, phone, address, record_id))
        conn.commit()
        conn.close()

    def delete_record(self, record_id):
        query = "DELETE FROM teachers WHERE id = ?"
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (record_id,))
        conn.commit()
        conn.close()

    def search_records(self, search_term):
        query = """
        SELECT * FROM teachers 
        WHERE first_name LIKE ? OR last_name LIKE ? OR email LIKE ? OR department LIKE ?
        """
        term = f"%{search_term}%"
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (term, term, term, term))
        records = cursor.fetchall()
        conn.close()
        return records
