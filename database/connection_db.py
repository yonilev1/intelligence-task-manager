import mysql.connector

class DbConnection:
    def get_connection(self):
        return mysql.connector.connect(
            user='root',
            password='1234',
            port=3306,
            host='127.0.0.1',
            database='Intelligence_db'
        )
    
conn = DbConnection()
get_conn = conn.get_connection()
cursor = get_conn.cursor()