"""
Author: Kevin Campos
Date: 2023-12-03
Description: Flight Deal Notifier

This Python script uses the Google Sheets API and a Flight Search API to find and notify users about flight deals.
It fetches data from a Google Sheet, retrieves detailed information about flights, validates for deals,
and sends SMS/Email notifications.

Prerequisites:
- Google Sheets API Key: Set as SHEETY_API_KEY environment variable.
- Google Sheets Endpoint: Set as SHEETY_SPREADSHEET environment variable.
- Flight Search API Key: Set as FLIGHT_SEARCH_API_KEY environment variable.
- Notification Configuration: Set CELL_NUMBER, PROVIDER, GMAIL, and GMAIL_APP_PASS as environment variables.

How to Run:
1. Install dependencies: `pip install -r requirements.txt`
2. Run the script: `python app.py`

Note: Ensure correct setup of environment variables before running the script.
"""

from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationSender

# ------------------------ GET GOOGLE SHEET DATA ------------------------
print("Getting Google Sheet Data...")
sheety_data = DataManager()
sheet_data = sheety_data.get_sheet_data()
print('------------------------------------------------------------------')

# ------------------------ FETCH FLIGHT API DATA ------------------------
print('Getting Flight Information...')
search_flights = FlightSearch(to_flights=sheet_data, homebase='DFW')
results = search_flights.get_flight_info()
print('------------------------------------------------------------------')

# ------------------------ DATA VALIDATION FOR ONLY DEALS ------------------------
print("Transforming Flight Data.")
transformed_flight_data = FlightData(results)
message_deals = transformed_flight_data.transform_data()
print('------------------------------------------------------------------')

# ------------------------ SEND EMAIL TO SMS ------------------------
print("Sending SMS Text for Any Deals.")
sms = NotificationSender()
sms.send_email(body=message_deals)
sms.send_email_to_all(body=message_deals, email_file='FlightApp_Flask/emails/user_emails.json')
