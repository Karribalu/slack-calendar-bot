import os
import pickle
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import logging
load_dotenv()
logger = logging.getLogger(__name__)

key = Fernet.generate_key()

logger.info(f"KEY Generated {key}")
cipher_suite = Fernet(key)


def load_credentials():
    if os.path.exists("credentials.pkl"):
        with open("credentials.pkl", "rb") as f:
            return pickle.load(f)
    return None


def store_credentials(credentials):
    with open("credentials.pkl", "wb") as f:
        pickle.dump(credentials, f)

# Encrypt text


def encrypt_text(plain_text):
    encrypted_text = cipher_suite.encrypt(plain_text.encode())
    return encrypted_text

# Decrypt text


def decrypt_text(encrypted_text):
    decrypted_text = cipher_suite.decrypt(encrypted_text).decode()
    return decrypted_text
