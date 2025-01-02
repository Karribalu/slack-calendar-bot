import pickle
import os
import logging
from google.oauth2.credentials import Credentials
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=str(openai_api_key))

logger = logging.getLogger(__name__)
logger.info(f"open ai key {openai_api_key}")


def query_openai(prompt):

    response = client.chat.completions.create(messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
        model="gpt-4o")
    return response.choices[0].message.content.strip()


def store_credentials(credentials):
    with open("credentials.pkl", "wb") as f:
        pickle.dump(credentials, f)


def load_credentials():
    if os.path.exists("credentials.pkl"):
        with open("credentials.pkl", "rb") as f:
            return pickle.load(f)
    return None
