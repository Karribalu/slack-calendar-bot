from googleapiclient.discovery import build
from google.auth.exceptions import RefreshError
import pickle
import os
from app.credential_utils import load_credentials
from app.google_auth import get_google_auth_url
from datetime import datetime
import pytz
import logging
logger = logging.getLogger(__name__)


async def create_calendar_event(event_details):
    credentials = load_credentials()
    if credentials == None:
        google_auth_url = get_google_auth_url()
        return {"result": f"Apologies, Your login creds might have expired, Please login to google using : {google_auth_url}"}
    service = build("calendar", "v3", credentials=credentials)

    start_time = get_utc_date_time(
        event_details["date"], event_details["start_time"])
    end_time = get_utc_date_time(
        event_details["date"], event_details["end_time"])

    event = {
        "summary": event_details["title"],
        "start": {"dateTime": start_time, "timeZone": "UTC"},
        "end": {"dateTime": end_time, "timeZone": "UTC"},
    }
    try:
        created_event = service.events().insert(
            calendarId="primary", body=event).execute()
    except RefreshError as e:
        google_auth_url = get_google_auth_url()
        return {"result": f"Apologies, Your login creds might have expired, Please login to google using : {google_auth_url}"}
    except Exception as e:
        logger.error(
            f"Something wrong has occured while creating the event {e}")
        return {"result": "Something wrong has occured while updating the event, Please try again later or contact the administrator"}
    return {"result": f"Created the event with URL: {created_event.get('htmlLink')}"}


async def update_calender_event(event_details):
    credentials = load_credentials()
    if credentials == None:
        google_auth_url = get_google_auth_url()
        return {"result": f"Apologies, Your login creds might have expired, Please login to google using : {google_auth_url}"}
    service = build("calendar", "v3", credentials=credentials)

    start_of_day = get_utc_date_time(
        event_details["date"], "00:00")
    end_of_day = get_utc_date_time(
        event_details["date"], "23:59")
    try:
        events_result = service.events().list(
            calendarId="primary",
            timeMin=start_of_day,
            timeMax=end_of_day,
            singleEvents=True,
            orderBy="startTime"
        ).execute()
        events = events_result.get("items", [])
        # Look for a matching event by title
        # TODO: We can use AI here to match the event more promptly instead of strict checking

        matching_event = next(
            (event for event in events if event["summary"]
             == event_details["title"]),
            None
        )

        if not matching_event:
            return {"result": "Event not found, Please verify your prompt"}

        event_id = matching_event["id"]

        start_time = get_utc_date_time(
            event_details["date"], event_details["start_time"])
        end_time = get_utc_date_time(
            event_details["date"], event_details["end_time"])

        updated_event = {
            "summary": event_details["title"],
            "start": {"dateTime": start_time, "timeZone": "UTC"},
            "end": {"dateTime": end_time, "timeZone": "UTC"},
        }

        updated_event_result = service.events().update(
            calendarId="primary",
            eventId=event_id,
            body=updated_event
        ).execute()

        return {"result": f"Updated the event with the given info URL: {updated_event_result.get('htmlLink')}"}
    except RefreshError as e:
        google_auth_url = get_google_auth_url()
        return {"result": f"Apologies, Your login creds might have expired, Please login to google using : {google_auth_url}"}
    except Exception as e:
        logger.error(
            f"Something wrong has occured while updating the event {e}")
        return {"result": "Something wrong has occured while updating the event, Please try again later or contact the administrator"}


async def get_calendar_events(event_details):
    credentials = load_credentials()
    if credentials == None:
        google_auth_url = get_google_auth_url()
        return {"result": f"Apologies, Your login creds might have expired, Please login to google using : {google_auth_url}"}
    service = build("calendar", "v3", credentials=credentials)
    try:
        google_auth_url = get_google_auth_url()
    except Exception as e:
        return {"result": f"Apologies, Your login creds might have expired, Please login to google using : {google_auth_url}"}

    # Convert the date to the start and end of the day in UTC
    start_of_day = get_utc_date_time(
        event_details["date"], event_details["start_time"])
    end_of_day = get_utc_date_time(
        event_details["date"], event_details["end_time"])

    try:
        # Fetch events for the specified date range
        events_result = service.events().list(
            calendarId="primary",
            timeMin=start_of_day,
            timeMax=end_of_day,
            singleEvents=True,
            orderBy="startTime"
        ).execute()

        events = events_result.get("items", [])
        logger.info(
            f"Found {len(events)} events on {event_details['date']} for retrieval")
        # TODO: We can use AI here to filter the results more efficiently
        # Extract relevant event details
        markdown_table = f"Events on {event_details['date']}: \n"

        for event in events:
            title = event.get("summary", "No Title")
            start_time = event["start"].get(
                "dateTime", event["start"].get("date"))
            end_time = event["end"].get("dateTime", event["end"].get("date"))
            link = event.get("htmlLink", "N/A")
            markdown_table += f" - {title} ({start_time} to {end_time})\n"
            markdown_table += (f"   Link: {link}\n")

        return {"result": markdown_table}
    except RefreshError as e:
        google_auth_url = get_google_auth_url()
        return {"result": f"Apologies, Your login creds might have expired, Please login to google using : {google_auth_url}"}
    except Exception as e:
        logger.error(f"Error fetching events: {type(e)}")
        return {"result": f"Failed to fetch events: {str(e)}"}


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
