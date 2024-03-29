#Create an all day, repeatable event in the user's primary Google Calendar 
#Stephanie Simpler
#1-25-2019

from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError

#read/write access to events
SCOPES = ['https://www.googleapis.com/auth/calendar.events'] 

def main():
    #Based on quickstart.py from Google Calendar API Docs
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    #If no valid creds, let user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        #Save creds for next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)


        #Create event
        today_date = datetime.date.today().isoformat()
        # print(today_date)
        event = {
            'summary': 'What do you want to do the most?',
            'location': 'Portland, OR',
            'start': {
                # 'dateTime': current_time.isoformat(),
                'date': today_date,
                'timeZone': 'America/Los_Angeles'
            },
            'end': {
                # 'dateTime': end_time.isoformat(),
                'date': today_date,
                'timeZone': 'America/Los_Angeles'
            },
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))
    except HttpError as error:
        print('Error occured: %s' % error)

if __name__ == '__main__':
    main()