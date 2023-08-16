#Create an all day, repeatable event in the user's primary Google Calendar 
#Stephanie Simpler
#1-25-2019

from __future__ import print_function
import datetime
import pickle
import os.path
import random 
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError

#read/write access to events
SCOPES = ['https://www.googleapis.com/auth/calendar.events'] 

def build_event():
    today_date = datetime.date.today().isoformat()
    # print(today_date)
    event_summary = input("Please enter the name of your event: ")
    event_location = input("Would you like to enter an address? Press Enter to skip: ") or "Portland, OR"
    event_color = input("What color is your event? Choose a number 1-11 or press Enter to skip: ") or random.randrange(11)
    event_description = input("Would you like to enter a description for your event? Press Enter to skip: ")
    event_start_date = input("When is the start date? Format YYYY-MM-DD Press Enter for today:") or today_date
    event_end_date = input("When is the end date? Format YYYY-MM-DD Press Enter for today:") or today_date
    full_event_info = {
        'summary': event_summary,
        'location': event_location,
        'colorId': event_color,
        'description': event_description,
        'start': {
            # 'dateTime': current_time.isoformat(),
            'date': event_start_date,
            'timeZone': 'America/Los_Angeles'
        },
        'end': {
            # 'dateTime': end_time.isoformat(),
            'date': event_end_date,
            'timeZone': 'America/Los_Angeles'
        },
    }
    return full_event_info

def post_event(event_info):
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
        event = event_info
        event = service.events().insert(calendarId='primary', body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))
    except HttpError as error:
        print('Error occured: %s' % error)

def main():
    post_event(build_event())

if __name__ == '__main__':
    main()