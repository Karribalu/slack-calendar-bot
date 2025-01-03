import os
import logging
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from app.credential_utils import store_credentials
from dotenv import load_dotenv

load_dotenv()
CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ["https://www.googleapis.com/auth/calendar"]
URL = str(os.getenv("SERVER_URL"))
logger = logging.getLogger(__name__)

logger.info(f"SERVER_URL {URL}")


def get_google_auth_url():
    flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri = URL+"/auth/callback"
    return flow.authorization_url()[0]


def google_auth_callback(code):
    flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri = URL+"/auth/callback"
    flow.fetch_token(code=code)
    credentials = flow.credentials
    store_credentials(credentials)
    return {"message": "Google Authentication Successful, Please close the tab"}
