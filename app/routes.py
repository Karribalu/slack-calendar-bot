from fastapi import APIRouter, Request
from app.slack_bot import process_slack_event
from app.google_auth import get_google_auth_url, google_auth_callback
from app.google_calendar import create_calendar_event

router = APIRouter()


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
def calendar_event(event_details: dict):
    return create_calendar_event(event_details)
