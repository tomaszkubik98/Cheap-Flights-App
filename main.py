#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from pprint import pprint
import requests
from data_manager import DataManager
from flight_data import FlightData
from notification_manager import NotificationManager
from flight_search import FlightSearch
SHEETY_ENDPOINT = "https://api.sheety.co/prices"

sheet = DataManager()

flight_data = FlightData(sheet)
flight_data.add_missing_codes()

data = flight_data.airports_file.cities_data

#Update sheet with IATA Codes
for row in data["prices"]:
    id = row["id"]
    parameter = {
        "price": {
            "iataCode": row["iataCode"]
        },
    }
    endpoint = f"{SHEETY_ENDPOINT}/{id}"
    response = requests.put(url=endpoint,json=parameter)

notification_manager = NotificationManager()
flight_search = FlightSearch(notification_manager)
flight_search.check_prices_for_6_months()




