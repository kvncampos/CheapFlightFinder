# This file will need to use the
# DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from pprint import pp
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationSender

# ------------------------ GET GOOGLE SHEET DATA ------------------------
print("Getting Google Sheet Data...")
sheet_data = DataManager()
flights = sheet_data.get_sheet_data()
sheet_data = flights.json()['flights']
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

