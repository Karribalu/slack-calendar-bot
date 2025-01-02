import os
import logging
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from app.utils import store_credentials, load_credentials
from dotenv import load_dotenv

load_dotenv()
CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ["https://www.googleapis.com/auth/calendar"]
URL = "https://fcbd-2406-b400-33-5b8e-482-1dc0-459f-8b66.ngrok-free.app"
logger = logging.getLogger(__name__)


def get_google_auth_url():
    flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri = URL+"/auth/callback"
    return flow.authorization_url()[0]


def google_auth_callback(code):
    flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri = URL+"/auth/callback"
    flow.fetch_token(code=code)
    credentials = flow.credentials
    logger.info(credentials.token)
    store_credentials(credentials)
    return {"message": "Google Authentication Successful"}
