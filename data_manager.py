# ------------------------ IMPORTS  ------------------------ #

import requests
import os


# ----------------------- CONSTANTS  ----------------------- #


class DataManager:
    """This class is responsible for talking to the Google Sheet."""

    def __init__(self):
        self.sheety_auth = (os.environ["SHEETY_USERNAME"], os.environ["SHEETY_PASSWORD"])
        self.tequila_api_key = os.environ["TEQUILA_API_KEY"]
        self.call_sheety = False
        self.airport_codes_needed = False
        self.destination_data = {}
        self.city_codes = {}
        self.get_city_data()

    def get_sheety_data(self, call_sheety: bool = False) -> list:
        if call_sheety:
            get_response = requests.get(
                url=os.environ["SHEETY_ENDPOINT"],
                auth=self.sheety_auth
            )
            get_response.raise_for_status()
            data = get_response.json()["prices"]
        else:
            data = [{"city": "Paris", "iataCode": "PAR", "lowestPrice": 54, "id": 2},
                    {"city": "Berlin", "iataCode": "BER", "lowestPrice": 42, "id": 3},
                    {"city": "Tokyo", "iataCode": "TYO", "lowestPrice": 485, "id": 4},
                    {"city": "Sydney", "iataCode": "SYD", "lowestPrice": 551, "id": 5},
                    {"city": "Istanbul", "iataCode": "IST", "lowestPrice": 95, "id": 6},
                    {"city": "Kuala Lumpur", "iataCode": "KUL", "lowestPrice": 414, "id": 7},
                    {"city": "New York", "iataCode": "NYC", "lowestPrice": 240, "id": 8},
                    {"city": "San Francisco", "iataCode": "SFO", "lowestPrice": 260, "id": 9},
                    {"city": "Cape Town", "iataCode": "CPT", "lowestPrice": 378, "id": 10}]
        return data

    def pull_airport_codes(self, city_name):
        iata_code_headers = {"accept": "application/json", "apikey": self.tequila_api_key}
        iata_code_params = {
            "term": city_name,
            "locale": "en-US",
            "location_types": "airport",
            "limit": 1,
            "active_only": "true",
        }
        city_data = requests.get(url="https://api.tequila.kiwi.com/locations/query",
                                 params=iata_code_params,
                                 headers=iata_code_headers).json()
        for location in city_data["locations"]:
            if location['city']['name'] == city_name:
                city_code = location['city']['code']
                self.city_codes[city_name] = city_code

    def add_iata_codes(self, city_codes):
        pass
        # data_row_count = 2
        # for city in city_codes:
        #     response_url = f"{os.environ['SHEETY_ENDPOINT']}/{data_row_count}"
        #     edit_response = requests.put(
        #         url=response_url,
        #         json={"price": {"iataCode": city_codes[city]}},
        #         auth=self.sheety_auth
        #     )
        #     edit_response.raise_for_status()
        #     data_row_count += 1

    def get_city_data(self):
        data = self.get_sheety_data(call_sheety=self.call_sheety)
        for data_row in data:
            city_name = data_row['city']
            city_code = data_row['iataCode']
            city_lowest_price = data_row['lowestPrice']
            self.destination_data[city_name] = {"city_code": city_code, "city_lowest_price": city_lowest_price}
            if self.airport_codes_needed:
                self.pull_airport_codes(city_name=city_name)
        self.add_iata_codes(city_codes=self.city_codes)


