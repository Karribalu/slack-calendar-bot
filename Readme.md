# Slack Calendar Bot

This Slack Calendar Bot integrates Slack and Google Calendar, allowing users to schedule, retrieve, and manage events directly through Slack commands.

## Features

- **Google Calendar Integration**: Create and view events in your Google Calendar.
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

### 7. Environment Configuration

```env
SLACK_BOT_TOKEN= <SLACK-OAUTH>
OPENAI_API_KEY=
SERVER_URL= <RANDOM-URL-GENERATED-USING-NGROK>
DATABASE_URL='postgresql://<owner>:<password>@<workspace>.us-east-2.aws.neon.tech/<db_name>?sslmode=require'
SECRET_KEY=<any-secret-for-encryption-and-decryption>
```
