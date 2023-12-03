from wrapper import time_function


class DataManager:
    # This class is responsible for talking to the Google Sheet

    def __init__(self):
        import os
        self.sheety_api_key = os.environ.get('SHEETY_API_KEY', 'Sheety API Key Not SET as ENV Variable.')
        self.sheety_spreadsheet = os.environ.get('SHEETY_SPREADSHEET', 'Check Sheety Endpoint URL.')

    @time_function
    def get_sheet_data(self):
        import requests
        url = f'https://api.sheety.co/{self.sheety_spreadsheet}/flightPrices/flights'

        headers = {
            'Authorization': f'Bearer {self.sheety_api_key}'
        }
        response = requests.get(url=url, headers=headers)

        return response
