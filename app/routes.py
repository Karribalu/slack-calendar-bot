import os
from datetime import datetime
from fastapi import APIRouter, Request, Form, Header
from app.slack_bot import process_slack_event
from app.google_auth import get_google_auth_url, google_auth_callback
from app.google_calendar import create_calendar_event
from pydantic import BaseModel
from app.credential_utils import encrypt_text, decrypt_text
import logging
import json

router = APIRouter()
logger = logging.getLogger(__name__)
SECRET_KEY = os.getenv("SECRET_KEY")


@router.post("/slack/events")
async def slack_events(request: Request):
    body = await request.json()
    return await process_slack_event(body)


@router.get("/auth/google")
def auth_google():
    return {"auth_url": get_google_auth_url()}


@router.get("/auth/callback")
def auth_callback(code: str):
    return google_auth_callback(code)


@router.post("/calendar/event")
async def calendar_event(event_details: dict):
    return await create_calendar_event(event_details)


@router.post("/slack/add-secrets")
async def add_secrets(request: Request,
                      # Content entered after the command
                      text: str = Form(...),
                      user_id: str = Form(...)):
    # Store the client secrets encrypted
    current_timestamp = datetime.now()  # Get the current timestamp
    if (verify_secrets(text)):
        encrypted_secrets = str(encrypt_text(text))
        async with request.app.state.db.acquire() as conn:
            result = await conn.fetchval("SELECT EXISTS (SELECT 1 FROM client_secrets WHERE user_id = $1)", user_id)

        logger.info(f"Result from db {result}")
        if result:
            await conn.execute("UPDATE client_secrets SET secret='{encrypted_secrets}', update_time={current_timestamp} where user_id='{user_id}'")
        else:
            await conn.execute("INSERT INTO client_secrets (user_id, secret, update_time) VALUES($1, $2, $3)", user_id, encrypted_secrets, current_timestamp)
    else:
        logger.info(f"Secrets not valid {text}")
        return {
            "response_type": "ephemeral",  # Only the user sees this
            "text": "Sorry, Something doesn't seem to be right with the credentials passed, Please try again"
        }
    return {
        "response_type": "ephemeral",  # Only the user sees this
        "text": "Stored your client secrets securely"
    }


def verify_secrets(text):
    try:
        reference_str = ""
        with open("reference_secrets.json", "r") as f:
            reference_str = f.read()

        reference_data = json.loads(reference_str)
        json_text = json.loads(text)
        reference_keys = set(extract_keys(reference_data))
        target_keys = set(extract_keys(json_text))

        missing_keys = reference_keys - target_keys
        return len(missing_keys) == 0
    except:
        return False


def extract_keys(data, prefix=""):
    keys = []
    if isinstance(data, dict):
        for k, v in data.items():
            full_key = f"{prefix}.{k}" if prefix else k
            keys.append(full_key)
            keys.extend(extract_keys(v, full_key))
    elif isinstance(data, list):
        for i, item in enumerate(data):
            full_key = f"{prefix}[{i}]"
            keys.extend(extract_keys(item, full_key))
    return keys
