from cryptography.fernet import Fernet

def generate_key():
    # Generate a key and save it to a file for future use
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

generate_key()