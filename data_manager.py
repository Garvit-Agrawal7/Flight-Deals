import os
import requests
from requests.auth import HTTPBasicAuth


SHEETY_PRICES_ENDPOINT = os.environ["SHEETY_ENDPOINT"]
USERNAME = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]
basic = HTTPBasicAuth(USERNAME, PASSWORD)


class DataManager:
    def __init__(self):
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(url=SHEETY_PRICES_ENDPOINT, auth=basic)
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{SHEETY_PRICES_ENDPOINT}/{city['id']}",
                json=new_data,
                auth=basic
            )
            print(response.text)
