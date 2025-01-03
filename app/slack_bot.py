import os
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from app.utils import query_openai
from dotenv import load_dotenv

load_dotenv()
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
client = WebClient(token=SLACK_BOT_TOKEN)

logger = logging.getLogger(__name__)


async def process_slack_event(event_body):
    if "challenge" in event_body:
        return {"challenge": event_body["challenge"]}
    logger.info(f"Received the request {event_body}")
    event = event_body.get("event", {})
    if event.get("type") == "app_mention" and "subtype" not in event:
        user_input = event.get("text", "")
        channel = event.get("channel")
        response = await query_openai(user_input)
        try:
            client.chat_postMessage(channel=channel, text=response["result"])
            return {"status": "ok"}
        except SlackApiError as e:
            logger.error(
                f"Something wrong has occured while posting the slack message {event_body}")
            print(f"Error posting to Slack: {e}")
    return {"status": "ok"}
