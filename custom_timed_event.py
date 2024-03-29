#Create a timed event in the user's primary Google Calendar 
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

def main():
    post_event(build_event())

##Defaults
#Summary: Name 
#Location: Blank/Current
#Color: Blank/Green 
#Description: Blank
#Length: 30 

def build_event():
    current_time = datetime.datetime.now()
    event_summary = input("Please enter the name of your time block: ") #TODO - Can I make the following inputs optional? Let the user skip all and set to defaults 
    event_location = input("Would you like to enter an address? Press Enter to skip: ") or "Beaverton 97006"
    event_color = input("What color is your event? Choose a number 1-11 or press Enter to skip: ") or random.randrange(11)
    event_description = input("Would you like to enter a description for your time block? Press Enter to skip: ") 
    event_length = input("How long is your event (in minutes)? Press Enter for default 30 minutes. ") or 30
    end_time = current_time + datetime.timedelta(minutes=int(event_length))
    full_event_info = {
        'summary': event_summary,
        'location': event_location, 
        'colorId': event_color,
        'description': event_description,
        'start': {
            'dateTime': current_time.isoformat(),
            'timeZone': 'America/Los_Angeles'
        },
        'end': {
            'dateTime': end_time.isoformat(),  
            'timeZone': 'America/Los_Angeles'
        },
    }
    return full_event_info
    
#Based on quickstart.py from Google Calendar API Docs
def post_event(event_info):
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

        #Call Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z' #UTC time <<<<working?

        event = event_info
        event = service.events().insert(calendarId='primary', body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))

    except HttpError as error:
        print('Error occured: %s' % error)

if __name__ == '__main__':
    main()

#TODO - option/flag for more input, defaults if not
#can I have an option to read in previous event and offer that as default? 
#read in user's time zone, location (or does Calendar store it)