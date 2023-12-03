from wrapper import time_function


class FlightSearch:
    """This class is responsible for talking to the Flight Search API."""

    def __init__(self, to_flights: list, homebase:str):
        import os
        self.tequila_api_key = os.environ.get('TEQUILA_API_KEY', 'Tequila API Key Not SET as ENV Variable.')
        self.flights = to_flights
        self.homebase = homebase

    @time_function
    def get_flight_info(self) -> list:
        """GET API Call to Query All Flight Data based on City and Target Price.

        :returns a list with all flight information.

        """
        import requests

        flight_data = []

        for obj in self.flights:
            city = obj.get('iataCode')
            target_price = obj.get('lowestPrice')
            print(f'City: {city}: Target Price: {target_price}')

            tequila_endpoint = f'https://api.tequila.kiwi.com/v2/search?fly_from={self.homebase}&fly_to={city}&' \
                               f'date_from=01%2F01%2F2024&date_to=09%2F01%2F2024&nights_in_dst_from=3&' \
                               f'nights_in_dst_to=4&ret_from_diff_city=false&ret_to_diff_city=false&adults=1&' \
                               f'fly_days=5&partner_market=us&curr=USD&price_to={target_price}&max_stopovers=0&' \
                               f'select_airlines=NK&select_airlines_exclude=true&vehicle_type=aircraft&limit=1'

            headers = {
                'accept': 'application/json',
                'apikey': self.tequila_api_key
            }

            data = requests.get(url=tequila_endpoint, headers=headers)

            flight_data.append(data.json())

        return flight_data
