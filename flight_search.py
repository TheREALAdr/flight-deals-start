# ------------------------ IMPORTS  ------------------------ #
import os
from datetime import datetime
import requests
from data_manager import DataManager
from flight_data import FlightData


class FlightSearch(DataManager):
    """This class is responsible for talking to the Flight Search API."""

    def __init__(self):
        super().__init__()
        self.api_key = os.environ["TEQUILA_API_KEY"]
        self.api_endpoint = "https://api.tequila.kiwi.com/v2/search"
        self.origin_city = "London"
        self.origin_city_code = "LON"
        self.get_flight_data(destination_data=self.destination_data)

    def get_flight_dates(self):
        flight_dates = {}
        now = datetime.now().strftime("%d/%m/%Y")
        month_now = int(datetime.now().strftime("%m"))
        year_now = int(datetime.now().strftime("%Y"))
        if int(month_now) > 7:
            deadline_month = f"0{(month_now + 6) - 12}"
            deadline_year = f"{year_now + 1}"
        else:
            deadline_month = month_now + 6
            deadline_year = year_now
            if deadline_month < 10:
                deadline_month = f"0{deadline_month}"
        deadline = datetime.now().strftime(f"%d/{deadline_month}/{deadline_year}")
        flight_dates["start_date"] = now
        flight_dates["end_date"] = deadline
        return flight_dates

    def get_flight_data(self, destination_data):
        def show_city_options():
            destination_choices: str = ""
            for choice in destination_data:
                destination_choices += f"{choice}\n"
            return destination_choices

        destination = input(f"\nChoices:\n{show_city_options()}\nPlease type in the city you would like to travel to "
                            f"from London (see above).\n")
        destination_code = destination_data[destination]["city_code"]
        destination_price = destination_data[destination]["city_lowest_price"]
        flight_dates = self.get_flight_dates()
        flight_search_headers = {"apikey": self.api_key}
        flight_search_params = {
            "fly_from": self.origin_city_code, "fly_to": destination_code, "date_from": flight_dates["start_date"],
            "date_to": flight_dates["end_date"], "ret_from_diff_city": "true", "ret_to_diff_city": "true",
            "adults": 1, "selected_cabins": "M", "adult_hand_bag": 1, "curr": "GBP", "locale": "us",
            "price_to": destination_price, "vehicle_type": "aircraft", "sort": "price", "limit": 1
        }
        flight_search_response = requests.get(url=self.api_endpoint,
                                              params=flight_search_params,
                                              headers=flight_search_headers)
        flight_search_response.raise_for_status()
        flight_search_data = flight_search_response.json()
        if flight_search_data["_results"] == 0:
            print("No results.")
        else:
            flight_data = flight_search_data["data"][0]
            FlightData(flight_data)


