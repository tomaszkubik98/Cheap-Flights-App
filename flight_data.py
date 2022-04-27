import requests
from data_manager import DataManager

IATA_CODE_ENDPOINT = "https://tequila-api.kiwi.com/locations/query"
TEQUILA_API_KEY = "key"
TEQUILA_HEADER = {
    "apikey": TEQUILA_API_KEY,
}


class FlightData:

    def __init__(self, sheet: DataManager):
        self.airports_file = sheet

    def add_missing_codes(self):
        for num in range(len(self.airports_file.cities_data["prices"])):
            if self.airports_file.cities_data["prices"][num]["iataCode"] == '':
                parameters = {
                    "term": self.airports_file.cities_data["prices"][num]["city"],
                    "location_types": "airport",
                }
                self.response = requests.get(url=IATA_CODE_ENDPOINT, params=parameters, headers=TEQUILA_HEADER)
                self.response.raise_for_status()
                self.airports_file.cities_data["prices"][num]["iataCode"] = self.response.json()["locations"][0]["city"]["code"]


