# This module takes care of every function related to password management for the password vault application
# Operations like adding, searching, updating, viewing and deleting password entries are found here
from db import db_connection
from encryption import generate_salt, encrypt_password, decrypt_password, derive_key
from getpass import getpass

def add_password(user_id):
    # Function for adding new password entry
    description = input("Enter description: ")
    username = input("Enter username: ")
    user_password = getpass("Enter password: ")

    # Generate a salt for the password encryption
    salt = generate_salt()

    # Derive the encryption key using the user's password and generated salt above
    encryption_key = derive_key(user_password, salt)

    # Encrypted password derived with the encryption key
    encrypted_password = encrypt_password(user_password, encryption_key)

    # Store the encrypted password, encryption key and salt in the database
    connection = db_connection()
    with connection.cursor() as cursor:
        sql = "INSERT INTO passwords (user_id, description, username, password, salt, encryption_key) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (user_id, description, username, encrypted_password, salt, encryption_key))
        connection.commit()
    connection.close()
    print("Password added!")

def search_password(user_id):
    # Function for searching for an entry in the vault
    search_term = input("Enter description or username to search: ")

    connection = db_connection()
    with connection.cursor() as cursor:
        sql = "SELECT description, username, password, salt, encryption_key FROM passwords WHERE (description=%s OR username=%s) AND user_id=%s"
        cursor.execute(sql, (search_term, search_term, user_id))
        result = cursor.fetchone()

    connection.close()

    if result:
        description, username, encrypted_password, salt, stored_encryption_key = result
        
        # This is where the password decryption is tried using the stored encryption key
        try:
            decrypted_password = decrypt_password(encrypted_password, stored_encryption_key)
            print(f"\nDescription: {description}\nUsername: {username}\nPassword: {decrypted_password}")
        except Exception as e:
            print("Password decryption failed!")
    else:
        print("No matching entry found.")

def update_password(user_id):
    # Function to update entries in the vault
    search_term = input("Enter description or username to update: ")

    connection = db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT id, salt FROM passwords WHERE (description=%s OR username=%s) AND user_id=%s"
            cursor.execute(sql, (search_term, search_term, user_id))
            result = cursor.fetchone()

        # Check if entry is in the vault
        if result:
            entry_id, existing_salt = result
        
            # Prompt user for new password
            new_password = getpass("Enter the new password: ")

            # Derive new encryption key with the new password and existing salt
            new_encryption_key = derive_key(new_password, existing_salt)

            # Encrypt the new password using the new derived encryption key
            encrypted_new_password = encrypt_password(new_password, new_encryption_key)

            with connection.cursor() as cursor:
                sql = "Update passwords SET password=%s, encryption_key=%s WHERE id=%s"
                cursor.execute(sql, (encrypted_new_password, new_encryption_key, entry_id))
                connection.commit()
        
            print("Password updated!")
        else:
            print("No matching entry found.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        connection.close()

def view_all_usernames(user_id):
    # Function to view all usernames with they descryptions while hiding passwords
    connection = db_connection()
    with connection.cursor() as cursor:
        sql = "SELECT description, username FROM passwords WHERE user_id=%s"
        cursor.execute(sql, (user_id,))
        results = cursor.fetchall()
    
    connection.close()

    if results:
        print("\nStored Passwords (Descriptions and Usernames only): ")
        for description, username in results:
            print(f"Description: {description}, Username: {username}")
    else:
        print("No stored credentials found.")

def delete_passwords(user_id):
    #Function to delete entries using the username from the vault
    search_term = input("Enter username of the entry you want to delete: ")

    connection = db_connection()
    with connection.cursor() as cursor:
        sql = "SELECT id, description, username FROM passwords WHERE (username=%s) AND user_id=%s"
        cursor.execute(sql, (search_term, user_id))
        result = cursor.fetchone()

    if result:
        entry_id, description, username = result

        # Confirm deletion
        confirm = input (f"Are you sure you want to delete the entry for'{description}' with username '{username}'? (y/n): ").strip().lower()
        if confirm == 'y':
            with connection.cursor() as cursor:
                sql = "DELETE FROM passwords WHERE id=%s"
                cursor.execute(sql, (entry_id,))
                connection.commit()
            print("Entry deleted!")
        else:
            print("Deletion cancelled")
    else:
        print("No matching record was found.")

        connection.close()