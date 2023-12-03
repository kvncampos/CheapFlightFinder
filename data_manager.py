from wrapper import time_function


class DataManager:
    """This class is responsible for talking to the Google Sheet.

    :param ENV VARS
        SHEETY_API_KEY,
        SHEETY_SPREADHSEET

    :returns
        GET Response from Google Sheets.
    """

    def __init__(self):
        """Fetch ENV VARS to communicate with Google Sheets."""
        import os
        self.sheety_api_key = os.environ.get('SHEETY_API_KEY', 'Sheety API Key Not SET as ENV Variable.')
        self.sheety_spreadsheet = os.environ.get('SHEETY_SPREADSHEET', 'Check Sheety Endpoint URL.')

    @time_function
    def get_sheet_data(self) -> list:
        """GET Request for Google Sheets Data.

        - Decorator Function to Time Speed of Execution.

        :returns
            List of Sheet Data
        """
        import requests
        # Change the name of your spreadsheet according to Sheety API. (Leave out the Spreadsheet ID)
        url = f'https://api.sheety.co/{self.sheety_spreadsheet}/flightPrices/flights'

        headers = {
            'Authorization': f'Bearer {self.sheety_api_key}'
        }
        response = requests.get(url=url, headers=headers)
        sheet_data = response.json()['flights']

        return sheet_data
