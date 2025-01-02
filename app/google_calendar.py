from googleapiclient.discovery import build
import pickle
import os
from app.credential_utils import load_credentials
from datetime import datetime
import pytz
import logging
logger = logging.getLogger(__name__)


def create_calendar_event(event_details):
    credentials = load_credentials()
    if not credentials:
        return {"error": "User not authenticated"}

    service = build("calendar", "v3", credentials=credentials)
    logger.info(f'Before {event_details}')
    start_time = get_utc_date_time(
        event_details["date"], event_details["start_time"])
    end_time = get_utc_date_time(
        event_details["date"], event_details["end_time"])

    logger.info(f'{start_time} - {end_time}')
    event = {
        "summary": event_details["title"],
        "start": {"dateTime": start_time, "timeZone": "UTC"},
        "end": {"dateTime": end_time, "timeZone": "UTC"},
    }
    created_event = service.events().insert(
        calendarId="primary", body=event).execute()
    return {"event_link": created_event.get("htmlLink")}


def get_utc_date_time(date, time):

    # Local date and time
    local_date_time_str = f'{date} {time}'
    local_format = "%Y-%m-%d %H:%M"

    # Parse the string into a datetime object
    local_date_time = datetime.strptime(local_date_time_str, local_format)

    # Set the timezone for the local datetime (e.g., assume it's in your local timezone)
    # Replace with your timezone
    local_timezone = pytz.timezone("Asia/Kolkata")
    localized_date_time = local_timezone.localize(local_date_time)

    # Convert to UTC
    utc_date_time = localized_date_time.astimezone(pytz.utc)

    # Format to desired output
    formatted_date_time = utc_date_time.strftime("%Y-%m-%dT%H:%M:%S%z")

    return formatted_date_time
