from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.parser]).parse_args()
except:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar' #Read/Write scope
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store, flags) \
        if flags else tools.run_flow(flow, store)
CAL = build('calendar', 'v3', http=creds.authorize(Http()))

GMT_OFF = '-8:00' #PST
EVENT = { #Bare min info, summary, start and end times
    'summary': 'Dinner with friends',
    'start': {'dateTime': '2019-01-25T12:30:29-08:00%s' % GMT_OFF},
    'end': {'dateTime': '2019-01-25T12:45:29-08:00%s' % GMT_OFF},
}

e = CAL.events().insert(calendarId='primary', sendNotifications=True, body=EVENT).execute()

print('''*** %r event added:
    Start: %s
    End: %s''' % (e['summary'].encode('utf-8'), e['start']['dateTime'], e['end']['dateTime']))
