"""
Google Calendar API tools for event management.

To use these tools, you need to have a `credentials.json` file in the root of the project.
This file is obtained from the Google Cloud Console.
For more information, see: https://developers.google.com/workspace/guides/create-credentials
"""

import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_calendar_service():
    """
    Returns a Google Calendar API service object.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("calendar", "v3", credentials=creds)
    return service


def get_calendars():
    """
    Returns a list of all calendars.
    """
    service = get_calendar_service()
    calendar_list = service.calendarList().list().execute()
    return calendar_list["items"]


def create_calendar(summary):
    """
    Creates a new calendar.
    """
    service = get_calendar_service()
    calendar = {"summary": summary}
    created_calendar = service.calendars().insert(body=calendar).execute()
    return created_calendar


def get_events(calendar_id):
    """
    Returns a list of all events in a calendar.
    """
    service = get_calendar_service()
    events_result = service.events().list(calendarId=calendar_id).execute()
    return events_result["items"]


def create_event(calendar_id, summary, start, end):
    """
    Creates a new event in a calendar.
    """
    service = get_calendar_service()
    event = {"summary": summary, "start": start, "end": end}
    created_event = service.events().insert(calendarId=calendar_id, body=event).execute()
    return created_event


def update_event(calendar_id, event_id, summary, start, end):
    """
    Updates an event in a calendar.
    """
    service = get_calendar_service()
    event = {"summary": summary, "start": start, "end": end}
    updated_event = (
        service.events()
        .update(calendarId=calendar_id, eventId=event_id, body=event)
        .execute()
    )
    return updated_event


def delete_event(calendar_id, event_id):
    """
    Deletes an event from a calendar.
    """
    service = get_calendar_service()
    service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
    return True
