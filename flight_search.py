import os
import requests

TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
TEQUILA_API_KEY = os.environ["TEQUILA_API_KEY"]


class FlightSearch:
    def __init__(self):
        self.header = {'apikey': TEQUILA_API_KEY}
        self.LOCATION_ENDPOINT = f"{TEQUILA_ENDPOINT}/locations/query"

    def get_destination_code(self, city_name):
        tequila_params = {
            'term': city_name,
            'location_types': 'city'
        }
        response = requests.get(url=self.LOCATION_ENDPOINT, params=tequila_params, headers=self.header)
        result = response.json()
        return result['locations'][0]["code"]
