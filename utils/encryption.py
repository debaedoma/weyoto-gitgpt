from cryptography.fernet import Fernet
import os

FERNET_SECRET = os.getenv("FERNET_SECRET_KEY")
fernet = Fernet(FERNET_SECRET)

def encrypt_token(raw: str) -> str:
    return fernet.encrypt(raw.encode()).decode()

def decrypt_token(enc: str) -> str:
    return fernet.decrypt(enc.encode()).decode()
