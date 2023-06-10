import os
import requests
import datetime

TEQUILA_SEARCH_ENDPOINT = "https://tequila-api.kiwi.com/v2/search"
TEQUILA_API_KEY = os.environ["TEQUILA_API_KEY"]


class FlightData:
    def __init__(self):
        self.departure_city = "New York"
        self.departure_airport_code = "city:LGA"
        self.currency = "USD"
        self.datetime = datetime.datetime.now()
        departure_from = self.datetime + datetime.timedelta(days=1)
        departure_to = self.datetime + datetime.timedelta(days=180)
        self.departure_to = departure_to.strftime("%d/%m/%Y")
        self.departure_from = departure_from.strftime("%d/%m/%Y")
        self.header = {'apikey': TEQUILA_API_KEY}

    def get_prices(self, iatacode):
        tequila_params = {
            "fly_from": self.departure_airport_code,
            "selected_cabins": "M",
            "curr": self.currency,
            "one_for_city": 1,
            "fly_to": iatacode,
            "date_from": self.departure_from,
            "date_to": self.departure_to,
            "flight_type": "oneway",
            "max_stopovers": 1
        }
        response = requests.get(url=TEQUILA_SEARCH_ENDPOINT, params=tequila_params, headers=self.header)
        data = response.json()
        return data
