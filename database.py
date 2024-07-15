import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                user="root",
                password="",
                host="localhost",
                database="Surf_club"
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
            else:
                raise Exception("Failed to connect to the database.")
        except Error as e:
            print(f"Error in MySQL: {e}")
            self.cursor = None  # Ensure cursor is None if connection fails

    def query(self, sql, params=None):
        if self.cursor is None:
            print("Cursor is not initialized. Database connection may have failed.")
            return []

        try:
            self.cursor.execute(sql, params)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error executing query: {e}")
            return []

    def execute(self, sql, params=None):
        if self.cursor is None:
            print("Cursor is not initialized. Database connection may have failed.")
            return 0

        try:
            self.cursor.execute(sql, params)
            self.connection.commit()
            return self.cursor.rowcount
        except Error as e:
            print(f"Error executing command: {e}")
            return 0

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
