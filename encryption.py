# This is the encryption module that will handle the encryption and salting of the passwords using Fernet and PBKDF2
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64

def generate_salt():
    # Creates a random 16-byte salt for encryption
    return os.urandom(16)

def derive_key(password, salt):
    # Derive a key using PBKDF2 with the given password and salt
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt_password(password, encryption_key):
    # Encrypt the password using Fernet with the derived encryption key
    fernet = Fernet(encryption_key)
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password

def decrypt_password(encrypted_password, encryption_key):
    # Decrypt the password using Fernet with the derived encryption key
    fernet = Fernet(encryption_key)
    decrypted_password = fernet.decrypt(encrypted_password).decode()
    return decrypted_password