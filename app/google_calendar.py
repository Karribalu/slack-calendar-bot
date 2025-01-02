from googleapiclient.discovery import build
from app.utils import load_credentials


def create_calendar_event(event_details):
    credentials = load_credentials()
    if not credentials:
        return {"error": "User not authenticated"}

    service = build("calendar", "v3", credentials=credentials)
    event = {
        "summary": event_details["summary"],
        "start": {"dateTime": event_details["start"], "timeZone": "UTC"},
        "end": {"dateTime": event_details["end"], "timeZone": "UTC"},
    }
    created_event = service.events().insert(
        calendarId="primary", body=event).execute()
    return {"event_link": created_event.get("htmlLink")}
