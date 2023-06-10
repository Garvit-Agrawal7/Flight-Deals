import os
import requests
from requests.auth import HTTPBasicAuth
from notification_manager import NotificationManager

SHEETY_USER_ENDPOINT = os.environ["SHEETY_USER_DATA"]
USERNAME = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]
basic = HTTPBasicAuth(USERNAME, PASSWORD)

print("Welcome to the Flight Club!")
print("We try to find the best flight deals for you and email you.")
fname = input("What is your first name?\n")
lname = input("What is your last name?\n")
email = input("What is your email?\n")
conformation = input("Type your email again.\n")
if email == conformation:
    print("You are registered in the Flight Club, you will hear from us soon.")
    new_user = {
        "user": {
            "firstName": fname,
            "lastName": lname,
            "email": email
        }
    }
    response = requests.put(SHEETY_USER_ENDPOINT, json=new_user, auth=basic)
    notification_manager = NotificationManager()
    try:
        if notification_manager.price < notification_manager.lowest_price:
            if notification_manager.via_city != notification_manager.arrival_city_name:
                notification_manager.send_stopover_mail(email, f"{fname} {lname}", notification_manager.via_city)
            else:
                notification_manager.send_email(email, f"{fname} {lname}")
    except TypeError:
        pass
else:
    print("The validation email doesn't match the email entered above, please check you answer again.")
