from wrapper import time_function


class FlightData:
    """This class is responsible for structuring the flight data.

    :param
        - List of flight_data


    """

    def __init__(self, flight_data: list):
        self.flight_data = flight_data

    def __find_deals(self) -> list:
        """Quickly Filters out any Locations that Do not Return Data based on Parameters Set in Tequila API.
        :param
            - List of Flight Data

        :returns
            - List of Non-Empty Flight info
        """
        deals = []
        for flight in self.flight_data:
            if not flight.get('data'):
                print('No Deals.')
            else:
                print("Deal Found.")
                deals.append(flight)
        return deals

    @time_function
    def transform_data(self) -> str:
        """
        Transform the Data to only the specified sections.
            - FlyFrom, FlyTo
            - CityFrom, CityTo
            - LocalDeparture(Outbound, Inbound)
            - nightsInDest
            - price
            - airlines
            - deep_link : Each Travel URL

        :return:
            Str of HTML for Email Body.
        """

        from datetime import datetime
        deals = self.__find_deals()

        sms_data = 'Deals Found for the Following Flights:\n'
        sms_data_html = '<h3>Deals Found for the Following Flights:</h3>\n'

        for each_flight in deals:

            cityFrom = each_flight['data'][0].get('cityFrom')
            flyFrom = each_flight['data'][0].get('flyFrom')
            cityTo = each_flight['data'][0].get('cityTo')
            flyTo = each_flight['data'][0].get('flyTo')

            departures = []
            for departure in each_flight['data'][0]['route']:
                departures.append(departure.get('local_departure'))

            # This is to format the Departure and Arrival Times
            formatted_local_departure = datetime.strptime(departures[0], '%Y-%m-%dT%H:%M:%S.%fZ')
            # Extract the year, month, and day
            departure_year = formatted_local_departure.year
            departure_month = formatted_local_departure.month
            departure_day = formatted_local_departure.day

            formatted_local_arrival = datetime.strptime(departures[1], '%Y-%m-%dT%H:%M:%S.%fZ')
            arrival_year = formatted_local_arrival.year
            arrival_month = formatted_local_arrival.month
            arrival_day = formatted_local_arrival.day

            nightsInDest = each_flight['data'][0].get('nightsInDest')
            price = each_flight['data'][0].get('price')
            airlines = each_flight['data'][0].get('airlines')
            deep_link = each_flight['data'][0].get('deep_link')

            flight_info = f"""
            {cityFrom}:{flyFrom} -> {cityTo}:{flyTo}
            Depart on: {departure_year}/{departure_month}/{departure_day} -> Return on: {arrival_year}/{arrival_month}/{arrival_day}
            Total Nights: {nightsInDest} -- Price Round Trip: ${price} USD --- Airlines: {airlines[0]}
            Link: {deep_link}
            """

            # write the HTML part
            flight_info_html = f"""\
            <html>
              <body>
                <p>{cityFrom}:{flyFrom} ---> {cityTo}:{flyTo}<br>
                  Depart on: {departure_year}/{departure_month}/{departure_day} -> Return on: {arrival_year}/{arrival_month}/{arrival_day}:</p>
                <p><a href={deep_link}>Travel Information</a></p>
                <p> Powered By <strong>PythonAnywhere</strong> FlightApp.</p>
              </body>
            </html>
            """

            sms_data += flight_info
            sms_data_html += flight_info_html

        return sms_data_html
