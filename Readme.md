# Slack Calendar Bot

This Slack Calendar Bot integrates Slack and Google Calendar, allowing users to schedule, retrieve, and manage events directly through Slack commands.

## Features

- **Google Calendar Integration**: Create and view events in your Google Calendar.
- **Slack Chat**: User can interact with bot by mentioning in the chat and use natural laguage.
- **Slack Commands**: Interact with the bot using slash commands in Slack.
- **Authentication**: Securely authenticate via Slack OAuth and Google OAuth.

---

## Prerequisites

1. **Python 3.8+** installed on your system.
2. **Slack Workspace** with appropriate permissions.
3. **Google Cloud Project** with access to Google Calendar API.

---

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/karribalu/slack-calendar-bot.git
cd slack-calendar-bot
```

### 2. Install the dependecies

```bash
pip install -r requirements.txt
```

### 3. Start the Application

```bash
uvicorn app.main:app
```

### 4. Deploy the application from local

- This will create a random hosted url for your app which we can use in further steps

```bash
ngrok http http://127.0.0.1:8000
```

### 5. Configure Google API

1. Create a Google Cloud Project:

   - Go to the Google Cloud Console.
   - Create a new project.
   - Enable the Google Calendar API for your project.

2. Generate OAuth 2.0 Credentials:

   - Navigate to APIs & Services > Credentials.
   - Click "Create Credentials" > "OAuth Client ID".
   - Set the application type to "Web application" and provide the redirect URI. (eg. https://116c-2406-b400-33-5b8e-482-1dc0-459f-8b66.ngrok-free.app/auth/callback)

3. Download Credentials:
   - Save the credentials as credentials.json and place it in the app/ directory.

### 6. Set Up Slack Integration

1. Create a Slack App:

   - Go to the Slack API dashboard.
   - Create a new app with your workspace.

2. Enable OAuth & Permissions:

   - Add bot as a scope under OAuth & Permissions.
   - Configure the Redirect URI (e.g., https://116c-2406-b400-33-5b8e-482-1dc0-459f-8b66.ngrok-free.app/auth/google).

3. Install the App to Workspace:
   - Generate an OAuth Token and copy it.
4. Set Slash Commands:
   - Define commands (e.g., /add-secrets) in the Slack app dashboard.
   - Use <your-host>/slack/add-secrets
5. Create a channel to identify the calender-app and add the slack app to it.
6. We can use the channel created to mention the bot and request the things to do.

### 7. Environment Configuration

```env
SLACK_BOT_TOKEN= <SLACK-OAUTH>
OPENAI_API_KEY=
SERVER_URL= <RANDOM-URL-GENERATED-USING-NGROK>
DATABASE_URL='postgresql://<owner>:<password>@<workspace>.us-east-2.aws.neon.tech/<db_name>?sslmode=require'
SECRET_KEY=<any-secret-for-encryption-and-decryption>
```

### 8. Future Enhancements

1. Currently we still not have a way to get the user's secrets, Added an API which needs work.
2. The Authentication refresh should be done by user, Slack will prompt whenever it expires!
3. We can use postgreSQL for storing the auth token instead of in a file called credentials.pkl.
4. Slack is calling the api twice everytime bot is mentioned, We can use some type of fallback to identify if the request is already served.
5. We can use AI more to filter the calender API results more naturally instead of strict matching.
