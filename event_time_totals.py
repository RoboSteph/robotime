#Read in the last week's events from the user's primary Google Calendar
#List amount of time per event 
#Stephanie Simpler
#3-14-2019

from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def main():
	readEvents()

def readEvents():
	#based on quickstart.py from Calendar API docs
	creds = None
	if os.path.exists('token.pickle'):
		with open('token.pickle', 'rb') as token:
			creds = pickle.load(token)
	#if no valid creds, let user log in
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				'credentials.json', SCOPES)
			creds = flow.run_local_server()
		#save creds for next run
		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)

	service =  build('calendar', 'v3', credentials=creds)

	#Call Calendar API
	now = datetime.datetime.utcnow().isoformat() + 'Z'
	week_ago = (datetime.datetime.utcnow() - datetime.timedelta(days=7)).isoformat() + 'Z'

	print('Reading your calendar...')


	#List events from the past week
	events_results = service.events().list(calendarId='primary', timeMin = week_ago, timeMax = now,
											maxResults=100, singleEvents=True,
											orderBy='startTime').execute()
	events = events_results.get('items', [])

	if not events:
		print("No events found :( ")
	for event in events: 
		start = event['start'].get('dateTime', event['start'].get('date'))
		end = event['end'].get('dateTime', event['end'].get('date'))
		#duration = end - start #Does not work, just an idea. Working on trying to get the non-iso formatted time 
		print('Start Time: ' + start, '|', 'End Time: ' + end, '|', event['summary'])

if __name__ == '__main__':
	main()