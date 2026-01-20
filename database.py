import sqlite3
import os

class Database:
    def __init__(self, db_name="ims_records.db"):
        self.db_name = db_name
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def init_db(self):
        """Initialize the database and create the records table if it doesn't exist."""
        query = """
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            address TEXT
        )
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        conn.close()

    def add_record(self, first_name, last_name, email, phone, address):
        query = "INSERT INTO records (first_name, last_name, email, phone, address) VALUES (?, ?, ?, ?, ?)"
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (first_name, last_name, email, phone, address))
        conn.commit()
        conn.close()

    def fetch_records(self):
        query = "SELECT * FROM records"
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        conn.close()
        return records

    def update_record(self, record_id, first_name, last_name, email, phone, address):
        query = """
        UPDATE records 
        SET first_name = ?, last_name = ?, email = ?, phone = ?, address = ? 
        WHERE id = ?
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (first_name, last_name, email, phone, address, record_id))
        conn.commit()
        conn.close()

    def delete_record(self, record_id):
        query = "DELETE FROM records WHERE id = ?"
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (record_id,))
        conn.commit()
        conn.close()

    def search_records(self, search_term):
        query = """
        SELECT * FROM records 
        WHERE first_name LIKE ? OR last_name LIKE ? OR email LIKE ?
        """
        term = f"%{search_term}%"
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (term, term, term))
        records = cursor.fetchall()
        conn.close()
        return records
