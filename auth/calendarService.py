import datetime
from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def getCalService():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    tokenPath = 'auth/token.json'
    credentialsPath = 'auth/credentials.json'
    if os.path.exists(tokenPath):
        creds = Credentials.from_authorized_user_file(tokenPath, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentialsPath, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(tokenPath, 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    return service;

def getCalendar():
    service = getCalService()
    # Call the Calendar API
    calendars_result = service.calendarList().list().execute()
    
    calendars = calendars_result.get('items', [])
    
    cal_dict = {}
    if not calendars:
        print('No calendars found.')
    for calendar in calendars:
        cal_dict[calendar['summary']] = calendar['id']
    print(cal_dict)
    getEntriesForCalendar(cal_dict['Office'])

    return cal_dict;


def getEntriesForCalendar(id):
    print('Getting calendar event')
    print(id)
    service = getCalService()
       # Call the Calendar API
    now = datetime.datetime(2021, 5, 5).isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting List of 10 events')
    events_result = service.events().list(
        calendarId=id, timeMin=now, singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
    