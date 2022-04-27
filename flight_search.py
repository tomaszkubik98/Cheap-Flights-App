import requests
import datetime as dt
from pprint import pprint
from notification_manager import NotificationManager

SHEETY_ENDPOINT = "https://api.sheety.co/prices"
IATA_CODE_ENDPOINT = "https://tequila-api.kiwi.com/v2/search"
TEQUILA_API_KEY = "key"
TEQUILA_HEADER = {
    "apikey": TEQUILA_API_KEY,
}
SHEETY_USERS_ENDPOINT = "https://api.sheety.co/users"


class FlightSearch:
    def __init__(self, notification_manager: NotificationManager):
        self.response = requests.get(url=SHEETY_ENDPOINT)
        self.data = self.response.json()
        #testline
        #self.data = {'prices': [{'city': 'Paris', 'iataCode': 'PAR', 'lowestPrice': 5, 'id': 2}, {'city': 'Berlin', 'iataCode': 'BER', 'lowestPrice': 42, 'id': 3},
        # {'city': 'Mexico', 'iataCode': 'MEX', 'lowestPrice': 500, 'id': 4}]}
        self.codes_with_price = [(self.data["prices"][num]["iataCode"], self.data["prices"][num]["lowestPrice"]) for num in range(len(self.data["prices"]))]
        self.codes = [tuple[0] for tuple in self.codes_with_price]
        self.fly_to_param = (",").join(self.codes)
        self.price = 0
        self.notification_manager = notification_manager
        pprint(self.codes)

    def check_prices_for_6_months(self):
        self.tommorow = (dt.datetime.now()+dt.timedelta(days=1)).strftime("%d/%m/%Y")
        self.date_after_6_months = (dt.datetime.now()+dt.timedelta(days=180)).strftime("%d/%m/%Y")
        self.parameters = {
            "adults": 2,
            "date_from": self.tommorow,
            "date_to": self.date_after_6_months,
            "fly_from": "KRK",
            "fly_to": self.fly_to_param,
            "one_for_city": 1,
            "nights_in_dst_from": 3,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "ret_from_diff_airport": 0,
            "max_stopovers": 0,
        }
        self.response2 = requests.get(url=IATA_CODE_ENDPOINT,params=self.parameters,headers=TEQUILA_HEADER)
        self.flights = self.response2.json()
        pprint(self.flights)
        for flight in self.flights["data"]:
            for tuple in self.codes_with_price:
                if flight['cityCodeTo'] in tuple:
                    self.price = tuple[1]

            if flight["price"] <= self.price:
                self.response3 = requests.get(url=SHEETY_USERS_ENDPOINT)
                self.users_data = self.response3.json()["users"]
                for row in self.users_data:
                    self.user = row["email"]
                    self.text = f"Hello, {row['firstName']}\nOnly {flight['price']} Euro to fly from Krakow-{flight['cityCodeFrom']} to {flight['cityTo']}-{flight['cityCodeTo']}" \
                                f" from {flight['route'][0]['local_departure'][:10]} to {flight['route'][1]['local_departure'][:10]}"
                    self.notification_manager.send_notification(user=self.user, text=self.text)
                    pprint(self.text)



