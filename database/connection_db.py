import mysql.connector

class DbConnection:
    def get_connection(self):
        """
        return the connection
        """
        return mysql.connector.connect(
            user='root',
            password='1234',
            port=3306,
            host='127.0.0.1'
        )
    

    def create_database(self):
        """
        connect and create db if does not exist already
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        CREATE DATABASE IF NOT EXISTS Intelligence_db;
        """)


    def create_tables(self):
        """
        connect and create db if does not exist already,
        then use db and create table if does not exist already
        """
        self.create_database()
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("USE Intelligence_db")
        cursor.close()

        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS agents (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            specialty VARCHAR(50) NOT NULL,
            is_active BOOLEAN NOT NULL DEFAULT TRUE,
            completed_missions INT NOT NULL DEFAULT 0, 
            failed_missions INT NOT NULL DEFAULT 0,             
            agent_rank ENUM('Junior', 'Senior', 'Commander') NOT NULL);
        """)

    
conn = DbConnection()
cr = conn.create_tables()
print(cr)