import pytz
import pickle
import os
import logging
from app.google_calendar import create_calendar_event, update_calender_event, get_calendar_events
from google.oauth2.credentials import Credentials
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=str(openai_api_key))

logger = logging.getLogger(__name__)


async def query_openai(prompt):
    # We have to figure out the type of request first before processing
    # Identify if the prompt is greetings prompty
    greetings_prompt = ""
    with open("./prompts/identify-greetings.txt", "r") as f:
        greetings_prompt = f.read()
    greetings_prompt = f"{greetings_prompt} \n message: {prompt}"
    response = client.chat.completions.create(messages=[
        {
            "role": "user",
            "content": greetings_prompt,
        }
    ],
        model="gpt-4o")
    chat_response = response.choices[0].message.content

    if (chat_response == "true"):
        return {"result": "Hello! I’m your virtual assistant here to help you manage your calendar effortlessly. How can I assist you today?"}
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
    chat_response = response.choices[0].message.content
    json_object = chat_response.replace("null", "None").replace("true", "True")
    parsed_object = eval(json_object)
    logger.info(
        f"Actual Chat response {chat_response} \n parsed response: {parsed_object}")
    """
    Sample Format
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
        return "Apologies, Please provide what can I help with you in adding, updating your google calendar"
    else:
        parsed_object['start_time'] = '00:00'
        parsed_object['end_time'] = '23:59'
        match parsed_object["request_type"]:
            case 'CREATE':
                response = await create_calendar_event(parsed_object)
                logger.info(
                    f'Recieved the response after creating the event {response}')
                return response
            case 'UPDATE':
                response = await update_calender_event(parsed_object)
                logger.info(
                    f"Received the response after updating the event {response}")
                return response
            case 'RETRIEVE':
                response = await get_calendar_events(parsed_object)
                return response
            case 'DELETE':
                pass

    return response.choices[0].message.content.strip()


def create_event(payload):

    pass
