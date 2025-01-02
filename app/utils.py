import pytz
import pickle
import os
import logging
from app.google_calendar import create_calendar_event
from google.oauth2.credentials import Credentials
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=str(openai_api_key))

logger = logging.getLogger(__name__)


def query_openai(prompt):
    # We have to figure out the type of request first before processing
    enhanced_prompt = ""
    with open("./prompts/calendar-prompt.txt", "r") as f:
        enhanced_prompt = f.read()

    enhanced_prompt = f"{enhanced_prompt} \n message: {prompt}"
    response = client.chat.completions.create(messages=[
        {
            "role": "user",
            "content": enhanced_prompt,
        }
    ],
        model="gpt-4o")
    chat_response = response.choices[0].message.content.strip()
    json_object = chat_response.replace("null", "None").replace("true", "True")
    parsed_object = eval(json_object)
    """
    {
  "date": "2023-10-18",
  "start_time": "09:00",
  "end_time": "12:00",
  "duration": "None",
  "title": "my birthday",
  "location": "hyderabad",
  "description": "None",
  "valid_message": "True",
  "request_type": "CREATE"
}
    """
    if ("valid_message" not in parsed_object or parsed_object["valid_message"] != True):
        logger.info(f'{parsed_object} {type(parsed_object["valid_message"])}')
        return "Apologies, Please provide what can I help with you in adding, updating your google calendar"
    else:
        match parsed_object["request_type"]:
            case 'CREATE':
                created_link = create_calendar_event(parsed_object)
                logger.info(f'Created the event with {create_event}')
                return f'Created the event with {create_event}'
                pass
            case 'UPDATE':
                pass
            case 'RETRIEVE':
                pass
            case 'DELETE':
                pass

    return response.choices[0].message.content.strip()


def create_event(payload):

    pass

