#Create a timed event in the user's primary Google Calendar 
#Stephanie Simpler
#1-25-2019
#Based on quickstart.py from Google Calendar API Docs

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
    postEvent(buildEvent())
#     creds = None
#     if os.path.exists('token.pickle'):
#         with open('token.pickle', 'rb') as token:
#             creds = pickle.load(token)
#     #If no valid creds, let user log in
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'credentials.json', SCOPES)
#             creds = flow.run_local_server()
#         #Save creds for next run
#         with open('token.pickle', 'wb') as token:
#             pickle.dump(creds, token)


#     service = build('calendar', 'v3', credentials=creds)

#     #Call Calendar API
#     now = datetime.datetime.utcnow().isoformat() + 'Z' #UTC time <<<<working?
#     # print('Getting the upcoming 10 events')
#     # events_result=service.events().list(calendarId='primary', timeMin=now,
#     #                                 maxResults= 10, singleEvents=True, 
#     #                                 orderBy='startTime').execute()
#     # events = events_result.get('items', [])

#     # if not events:
#     #     print('No upcoming events found.')
#     # for event in events:
#     #     start = event['start'].get('dateTime', event['start'].get('date'))
#     #     print(start, event['summary'])


# #     #Create event
# #     # print(datetime.date.today())
# #     print(datetime.datetime.now().isoformat())
# #     current_time = datetime.datetime.now()
# #     end_time = current_time + datetime.timedelta(minutes=30)
# #     # TODO try start dateTime as now, figure out how to add 30 minutes 
# #     # to end dateTime
# #     event = {
# #         # 'summary': 'Boris Time',
# #         # 'location': '17348 SW Lawton St., Beaverton, OR 97003',
# #         # 'description': 'Boris invites you to pet him and talk about how \
# #         # handsome he is',
# #         # 'start': {
# #         #     'dateTime': current_time.isoformat(),
# #         #     'timeZone': 'America/Los_Angeles'
# #         # },
# #         # 'end': {
# #         #     'dateTime': end_time.isoformat(),
# #         #     'timeZone': 'America/Los_Angeles'
# #         # },
# #         #########################################################
# #         'summary': 'What do you want to do the most?',
# #         'location': '17348 SW Lawton St., Beaverton, OR 97003',
# #         'start': {
# #             'dateTime': current_time.isoformat()
# # ,            'timeZone': 'America/Los_Angeles'
# #         },
# #         'end': {
# #             'dateTime': end_time.isoformat(),
# #             'timeZone': 'America/Los_Angeles'
# #         },
# #     }

# #     event = service.events().insert(calendarId='primary', body=event).execute()
# #     print('Event created: %s' % (event.get('htmlLink')))

def buildEvent():
    current_time = datetime.datetime.now()
    end_time = current_time + datetime.timedelta(minutes=30)
    event_summary = input("Please enter the name of your time block: ")
    event_description = input("Would you like to enter a description for your time block? Press Enter to skip: ") #TODO - double check still works when empty
    full_event_info = {
        'summary': event_summary,
        'location': '17348 SW Lawton St., Beaverton, OR 97003', #TODO - replace with current location
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

def postEvent(event_info):
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

    #Call Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' #UTC time <<<<working?

    event = event_info
    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))    


if __name__ == '__main__':
    main()