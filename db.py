# This module controls how the application communicates with the database
import pymysql

# Credentials for connecting to the database
def db_connection():
    connection = pymysql.connect(
        host='localhost',
        user='database_manager',
        password='kidane',
        database='password_vault'
    )
    return connection

def create_tables():
    connection = db_connection()
    with connection.cursor() as cursor:
        # Creates tables if they dont exist
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS master_password (
                       id INT AUTO_INCREMENT PRIMARY KEY,
                       username VARCHAR(255) UNIQUE NOT NULL,
                       password VARCHAR(255) NOT NULL
                       );
                       """)
        # This creates the passwords table while assosciating with a user_id column
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS passwords (
                       id INT AUTO_INCREMENT PRIMARY KEY,
                       user_id INT NOT NULL,
                       description VARCHAR(255) NOT NULL,
                       username VARCHAR(255) NOT NULL,
                       password BLOB NOT NULL,
                       salt BLOB NOT NULL,
                       encryption_key BLOB NOT NULL,
                       FOREIGN KEY (user_id) REFERENCES master_password(id) ON DELETE CASCADE
                       );
                       """)
        
        connection.commit
    connection.close