import os  # lets you read environment variables
from cryptography.fernet import Fernet  # the tool for encrypting/decrypting

_fernet = None  # global variable to hold the Fernet object (starts off empty)

def get_fernet():
    global _fernet  # tells Python we want to use the global `_fernet` variable

    if _fernet is None:
        # If _fernet hasn’t been created yet, create it now
        key = os.getenv("FERNET_SECRET_KEY")

        if not key:
            raise ValueError("FERNET_SECRET_KEY is not set in environment")

        _fernet = Fernet(key)  # build it once

    return _fernet  # reuse the existing one next time

def encrypt_token(raw: str) -> str:
    """
    Encrypts a raw token string using Fernet.
    Returns the encrypted token as a UTF-8 string.
    """
    return get_fernet().encrypt(raw.encode()).decode()

def decrypt_token(enc: str) -> str:
    """
    Decrypts an encrypted token string using Fernet.
    Returns the original raw token.
    """
    return get_fernet().decrypt(enc.encode()).decode()
