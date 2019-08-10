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

#read/write access to events
SCOPES = ['https://www.googleapis.com/auth/calendar.events'] 

def main():
    #Based on quickstart.py from Google Calendar API Docs
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    #If no valid creds, let user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        #Save creds for next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)


    service = build('calendar', 'v3', credentials=creds)


    #Create event
    print(datetime.datetime.now().isoformat())
    current_time = datetime.datetime.now()
    end_time = current_time + datetime.timedelta(minutes=30)
    # TODO try start dateTime as now, figure out how to add 30 minutes 
    # to end dateTime
    event = {
        'summary': 'What do you want to do the most?',
        'location': '17348 SW Lawton St., Beaverton, OR 97003',
        'start': {
            'dateTime': current_time.isoformat(),
            'timeZone': 'America/Los_Angeles'
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'America/Los_Angeles'
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))

if __name__ == '__main__':
    main()