import mysql.connector

class DbConnection:
    def get_connection(self):
        return mysql.connector.connect(
            user='root',
            password='1234',
            port=3306,
            host='127.0.0.1'
        )
    

    def create_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        CREATE DATABASE IF NOT EXISTS Intelligence_db;
        """)

    
conn = DbConnection()
cr = conn.create_database()
print(cr)