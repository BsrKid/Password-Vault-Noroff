# This module handles user authentication. Ensures ability to create, verify and manage master password given by users.
import hashlib
from getpass import getpass
from db import db_connection

def set_master_password():
    while True:
        # Function to ask user to create a new user and set master password, and then store it
        username = input("Enter a username (or type 'back' to return to the main menu): ").strip()
        
        if username.lower() == 'back':
            return None
        
        master_password = getpass("Set a master password (or type 'back' to return to the main menu): ").strip()

        if master_password.lower() == 'back':
            return None

        hashed_password = hashlib.sha256(master_password.encode()).hexdigest() # Hashes the password entered above

        try:
            connection = db_connection()
            with connection.cursor() as cursor:
                sql = "INSERT INTO master_password (username, password) VALUES (%s, %s)"
                cursor.execute(sql, (username, hashed_password,)) # Command to store the hashed password in the master_password table
                connection.commit()
            print("New user created!, Please log in with your newly created user.")
            return
        except Exception as e:
            print(f"Error creating new user: {e}")
            print("Please try again or choose a different username.")
        finally:
            connection.close()

def master_password_validation(username, master_password):
    # Validates the master password against stored hashed master_password in the database
    hashed_password = hashlib.sha256(master_password.encode()).hexdigest() #Hashes the input password using SHA-256 like above

    connection = db_connection()
    with connection.cursor() as cursor:
        sql = "SELECT id, password FROM master_password WHERE username=%s AND password = %s"
        cursor.execute(sql, (username, hashed_password,))
        result = cursor.fetchone() # Retreives the matching record if any.

    connection.close()

    # Checks if there inputted and hashed master_password matches any stored hash
    if result:
        return result[0] # Returns the user_id associated if validated
    else:
        return None