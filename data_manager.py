import requests

SHEETY_ENDPOINT = "https://api.sheety.co/prices"

class DataManager:
    def __init__(self):
        self.response = requests.get(url=SHEETY_ENDPOINT)
        self.cities_data = self.response.json()
        # test line
        # self.cities_data = {'prices': [{'city': 'Paris', 'iataCode': 'PAR', 'lowestPrice': 5, 'id': 2},
        # {'city': 'Berlin', 'iataCode': 'BER', 'lowestPrice': 42, 'id': 3}, {'city': 'Bali', 'iataCode': 'DPS', 'lowestPrice': 500, 'id': 4}]}



