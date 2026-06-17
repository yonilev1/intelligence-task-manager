import mysql.connector

class DbConnection:
    def __init__(self):
        self.user='root'
        self.password='1234'
        self.port=3306
        self.host='127.0.0.1'

    def get_connection(self):
        """
        return the connection
        """
        return mysql.connector.connect(
            user=self.user,
            password=self.password,
            port=self.port,
            host=self.host
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
        cursor.close()

        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS missions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(50) NOT NULL,
            description TEXT NOT NULL,
            location VARCHAR(50) NOT NULL,
            difficulty INT NOT NULL CHECK (difficulty >= 1 AND difficulty <= 10), 
            importance INT NOT NULL CHECK (importance >= 1 AND importance <= 10),
            status VARCHAR(11) NOT NULL,
            risk_level VARCHAR(8) NOT NULL,             
            assigned_agent_id INT DEFAULT NULL);
        """)


if __name__ == "__main__":
    conn = DbConnection()
    cr_db = conn.create_database()
    print(cr_db)
    cr_tbl = conn.create_tables()
    print(cr_tbl)