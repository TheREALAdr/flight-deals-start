# ------------------------ IMPORTS  ------------------------ #
from notification_manager import NotificationManager


class FlightData:
    """This class is responsible for structuring the flight data."""

    def __init__(self, flight_data):
        self.flight_price = flight_data["price"]
        self.origin_city = flight_data["cityFrom"]
        self.origin_airport = flight_data["flyFrom"]
        self.destination_city = flight_data["cityTo"]
        self.destination_airport = flight_data["flyTo"]
        self.departure_date = flight_data["local_departure"].split("T")[0]
        self.arrival_date = flight_data["local_arrival"].split("T")[0]
        self.compile_message()

    def compile_message(self):
        message_data = f"\n Low price alert! Only £{self.flight_price} to fly from" \
                       f" {self.origin_city}-{self.origin_airport} to" \
                       f" {self.destination_city}-{self.destination_airport}," \
                       f" from {self.departure_date} to {self.arrival_date}."
        NotificationManager(message_data)

