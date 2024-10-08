# This is the main script with user interface to allow users to interact with the password vault application
from auth import set_master_password, master_password_validation # Importing authentication functions
from db import create_tables
from getpass import getpass
from password_manager import add_password, search_password, update_password, view_all_usernames, delete_passwords # Importing the password management functions

def main():
    # This makes sure that the tables are created before any thing else.
    create_tables()

    print("Welcome to the KidSecure Password Vault")

    # Options for present users and new
    while True:
        print("\nSelect an option:")
        print("1. Login")
        print("2. Create A New User")
        print("3. Exit Application")
        choice = input("Enter your choice (1, 2 or 3): ").strip()

        if choice == '1':
            # Login with master password
            user_id = login_user()
            if user_id:
                print("Access granted! Welcome to the password vault. Proceeding to the password vault menu...")
                show_menu(user_id)
        
        elif choice == '2':
            # New user option
                set_master_password()
        
        elif choice == '3':
            # User exits the application
            print("Exiting the Password Vault. Goodbye!")
            break
        else:
            print("Invalid choice. Please choose 1, 2 or 3.")

def login_user():
    # Function to handle login
    user_id = None
    attempt_count = 0 # Counter to track number of failed attempts

    while user_id is None:
        username = input("Enter your username (or type 'back' to return to main menu): ").strip()
        
        if username.lower() == 'back':
            return None # Gets the user back to main menu
        
        master_password = getpass("Enter the master password (or type 'back' to return to the main menu): ").strip()
        
        if master_password.lower() == 'back':
            return None
        
        user_id = master_password_validation(username, master_password)
        
        if user_id:
            return user_id
        else:
            attempt_count += 1
            print("Wrong username or master password. Please try again.")
            if attempt_count >=3:
                back_choice = input("Would you like to return to the main menu? (y/n): ").strip().lower()
                if back_choice == 'y':
                    return None # Goes back to the main menu
    return None

def show_menu(user_id):
    # Shows the password vault menu
    while True:
        print("\nPassword Vault Menu:")
        print("1. Add Password")
        print("2. Search Password")
        print("3. Update Password")
        print("4. View All Entries")
        print("5. Delete Entry")
        print("6. Log out")
        choice = input("Enter your choice: ")

        # Function associated with choice above
        if choice == '1':
            add_password(user_id)
        elif choice == '2':
            search_password(user_id)
        elif choice == '3':
            update_password(user_id)
        elif choice == '4':
            view_all_usernames(user_id)
        elif choice == '5':
            delete_passwords(user_id)
        elif choice == '6':
            print("Logging you out. Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()