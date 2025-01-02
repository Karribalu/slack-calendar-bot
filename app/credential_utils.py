import os
import pickle


def load_credentials():
    if os.path.exists("credentials.pkl"):
        with open("credentials.pkl", "rb") as f:
            return pickle.load(f)
    return None


def store_credentials(credentials):
    with open("credentials.pkl", "wb") as f:
        pickle.dump(credentials, f)
