from langchain.tools import BaseTool
import json
from typing import Optional
from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials, credentials

class JsonTool(BaseTool):
    name: str = "Save_Json"
    description: str = """
                Here is how I read json data:
                - Full Name: [Customer's Full Name]
                - Phone Number: [Phone Number]
                - Email Address: [Email Address]
                - Property Type: [Type of Property]
                - Property Address: [Property Address]
                - Service Required: [Service Required]
                - Issue Description: [Issue Description]
                - Preferred Appointment Date: [Date]
                - Preferred Appointment Time: [Time]
                - Additional Notes: [Additional Notes or Special Requests]
                """

    def _run(self, booking_data_str: str) -> str:
        try:
            booking_data = json.loads(booking_data_str)
            json_file_path = os.getenv("BOOKING_PATH", "hvac_booking.json") #replace with your path
            with open(json_file_path, 'w') as json_file:
                json.dump(booking_data, json_file, indent=4)
            return f"Booking is done."
        except Exception as e:
            return f"Error saving JSON file: {e}"



class CalendarTool(BaseTool):
    name: str = "Add_to_Calendar"
    description: str = """
        "Time data must match format '%Y-%m-%d %H:%M'"
        Here is how I read json data:

        full_name = booking_data["Customer's Full Name"]
        phone_number = booking_data["Contact Information"]["Phone Number"]
        email_address = booking_data["Contact Information"]["Email Address"]
        property_address = booking_data["Property Details"]["Property Address"]
        service_required = booking_data["Service Required"]
        issue_description = booking_data["Issue Description"]
        appointment_date_str = booking_data["Preferred Appointment"]["Date"]
        appointment_time_str = booking_data["Preferred Appointment"]["Time"]
        additional_notes = booking_data["Additional Notes or Special Requests"]
    """

    def _run(self, booking_data_str: str) -> str:
        try:
            booking_data = json.loads(booking_data_str)

            # OAuth 2.0 Authentication
            SCOPES = ['https://www.googleapis.com/auth/calendar']
            creds = None
            token_path = os.getenv("GOOGLE_TOKEN", "token.json")  # Path to store the token, default to token.json

            if os.path.exists(token_path):
                creds = Credentials.from_authorized_user_file(token_path, SCOPES)
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    credentials_path = os.getenv("GOOGLE_CREDENTIALS", "credentials.json") #get path from environment variable, default to credentials.json
                    flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
                    creds = flow.run_local_server(port=0)
                with open(token_path, 'w') as token:
                    token.write(creds.to_json())

            service = build('calendar', 'v3', credentials=creds)

            # ... (rest of the calendar event creation code)
            full_name = booking_data["Customer's Full Name"]
            phone_number = booking_data["Contact Information"]["Phone Number"]
            email_address = booking_data["Contact Information"]["Email Address"]
            property_address = booking_data["Property Details"]["Property Address"]
            service_required = booking_data["Service Required"]
            issue_description = booking_data["Issue Description"]
            appointment_date_str = booking_data["Preferred Appointment"]["Date"]
            appointment_time_str = booking_data["Preferred Appointment"]["Time"]
            additional_notes = booking_data["Additional Notes or Special Requests"]

            appointment_datetime_str = f"{appointment_date_str} {appointment_time_str}"
            appointment_datetime = datetime.datetime.strptime(appointment_datetime_str, "%Y-%m-%d %H:%M")
            end_datetime = appointment_datetime + datetime.timedelta(hours=1)

            event = {
                'summary': f'HVAC Service for {full_name}',
                'location': property_address,
                'description': f'Service: {service_required}\nIssue: {issue_description}\nContact: {phone_number}, {email_address}\nNotes: {additional_notes}',
                'start': {
                    'dateTime': appointment_datetime.isoformat(),
                    'timeZone': 'America/New_York',
                },
                'end': {
                    'dateTime': end_datetime.isoformat(),
                    'timeZone': 'America/New_York',
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},
                        {'method': 'popup', 'minutes': 10},
                    ],
                },
            }

            event = service.events().insert(calendarId='primary', body=event).execute()
            return f'Event created: {event.get("htmlLink")}'

        except Exception as e:
            return f"Error adding to calendar: {e}"

    def _arun(self, query: str):
        raise NotImplementedError("This tool does not support async")


class AvailableSlotsTool(BaseTool):
    name: str = "Check_Available_Slots"
    description: str = """
                Useful for checking available time slots from today until the next 7 days.
                When the user requests a specific time slot, use this tool to determine if it is available.
                If the time slot is available, inform the user that the slot is open.
                If the time slot is unavailable, inform the user that the requested slot is not available, and offer to check other available slots.
                DO NOT share any specific details about the events that conflict with the requested time slot.
                This tool does not require any input.
                """

    def _run(self, query: Optional[str] = None) -> str: #added optional query
        SCOPES = ["https://www.googleapis.com/auth/calendar"]
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        creds = None
        token_path = os.getenv("GOOGLE_TOKEN", "token.json")
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(token_path, "w") as token:
                token.write(creds.to_json())

        try:
            service = build("calendar", "v3", credentials=creds)

            # Calculate date range (today to next 7 days)
            today = datetime.date.today()
            seven_days_later = today + datetime.timedelta(days=7)

            start_datetime = datetime.datetime.combine(today, datetime.datetime.min.time())
            end_datetime = datetime.datetime.combine(seven_days_later, datetime.datetime.min.time())

            # Call the Calendar API
            events_result = service.events().list(
                calendarId="primary",
                timeMin=start_datetime.isoformat() + "Z",
                timeMax=end_datetime.isoformat() + "Z",
                singleEvents=True,
                orderBy="startTime",
            ).execute()
            events = events_result.get("items", [])

            if not events:
                return "No upcoming events found in the next 7 days."

            available_slots = []
            for event in events:
                start = event["start"].get("dateTime", event["start"].get("date"))
                summary = event.get("summary", "No summary")
                available_slots.append(f"Start: {start}, Summary: {summary}")

            return "\n".join(available_slots)

        except Exception as error:
            return f"An error occurred: {error}"

    def _arun(self, query: str):
        raise NotImplementedError("This tool does not support async")
