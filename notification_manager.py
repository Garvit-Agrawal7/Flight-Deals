import os
import smtplib
import data_manager
from twilio.rest import Client
from flight_data import FlightData


flight_data = FlightData()
sheet_data = data_manager.DataManager().get_destination_data()

ACC_SID = os.environ["ACCOUNT_SID"]
TOKEN = os.environ["AUTH_TOKEN"]
TWILIO_NO = os.environ["TWILIO_NUMBER"]
PHONE_NUMBER = os.environ["PHONE_NUMBER"]
client = Client(ACC_SID, TOKEN)
EMAIL = os.environ["EMAIL"]
APP_PASSWORD = os.environ["APP_PASSWORD"]


class NotificationManager:
    def __init__(self):
        self.via_city = ""
        for row in sheet_data:
            data = flight_data.get_prices(row["iataCode"])
            self.lowest_price = flight_data.get_prices(row["lowestPrice"])
            try:
                self.price = data["data"][0]["price"]
                self.departure_city_name = data['data'][0]["cityFrom"]
                self.arrival_city_name = data["data"][0]["cityTo"]
                self.departure_iata_code = data["data"][0]["flyFrom"]
                self.arrival_iata_code = data["data"][0]["flyTo"]
                self.departure_time = data["data"][0]["route"][0]["local_departure"][:-14]
                self.arrival_time = data["data"][0]["route"][0]["local_arrival"][:-14]
                self.via_city = data["data"][0]["route"][0]["cityTo"]

            except IndexError:
                print("No flight found to the give location")

    def send_email(self, email, name):
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(EMAIL, APP_PASSWORD)
            connection.sendmail(
                from_addr=EMAIL,
                to_addrs=email,
                msg=f"Subject:Flight Club\n\n"
                    f"Low Price Alert {name}!\n"
                    f"Only ${self.price} to fly from {self.departure_city_name}-{self.departure_iata_code} to {self.arrival_city_name}-{self.arrival_iata_code} from {self.departure_time} to {self.arrival_time}"
            )

    def send_stopover_mail(self, email, name, stopover):
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(EMAIL, APP_PASSWORD)
            connection.sendmail(
                from_addr=EMAIL,
                to_addrs=email,
                msg=f"Subject:Flight Club\n\n"
                    f"Low Price Alert {name}!\n"
                    f"Only ${self.price} to fly from {self.departure_city_name}-{self.departure_iata_code} to {self.arrival_city_name}-{self.arrival_iata_code} from {self.departure_time} to {self.arrival_time}\n"
                    f"Flight has 1 stopover, via {stopover}"
            )

