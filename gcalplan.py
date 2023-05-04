import datetime
import os
import pytz
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up Google Calendar API
service_file = os.environ.get('SERVICE_ACCOUNT_FILE')
scopes = ['https://www.googleapis.com/auth/calendar']
print(f'SERVICE_ACCOUNT_FILE: {service_file}')

credentials = service_account.Credentials.from_service_account_file(
    service_file, scopes=scopes)
calendar_service = build('calendar', 'v3', credentials=credentials)

# Replace with your calendar ID, usually it's your email address
calendar_id = os.environ.get('CALENDAR_ID')

# Your schedule
schedule = [
    ('Wake up, breathing with prayer', '06:00:00', 15),
    ('Go for jog on beach', '06:15:00', 45),
    # Add more items here
]

# Set the date for the events
event_date = '2023-05-02'  # Change this to the desired date

# Timezone
tz = pytz.timezone('America/Sao_Paulo')

for title, start_time, duration in schedule:
    start = datetime.datetime.strptime(
        f'{event_date} {start_time}', '%Y-%m-%d %H:%M:%S')
    start = tz.localize(start)
    end = start + datetime.timedelta(minutes=duration)

    event = {
        'summary': title,
        'start': {
            'dateTime': start.isoformat(),
            'timeZone': 'America/Sao_Paulo',
        },
        'end': {
            'dateTime': end.isoformat(),
            'timeZone': 'America/Sao_Paulo',
        },
    }

    created_event = calendar_service.events().insert(
        calendarId=calendar_id, body=event).execute()
    print(f'Event created: {created_event.get("htmlLink")}')
