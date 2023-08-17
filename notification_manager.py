# ------------------------ IMPORTS  ------------------------ #
from twilio.rest import Client
import os


class NotificationManager():
    """This class is responsible for sending notifications with the deal flight details."""

    def __init__(self, message_data):
        self.twilio_phone_number = os.environ["TWILIO_PHONE_NUMBER"]
        self.twilio_account_sid = os.environ["TWILIO_ACCOUNT_SID"]
        self.twilio_auth_token = os.environ["TWILIO_AUTH_TOKEN"]
        self.user_phone_number = os.environ["USER_PHONE_NUMBER"]
        self.send_message(message_data=message_data)

    def send_message(self, message_data):
        client = Client(self.twilio_account_sid, self.twilio_auth_token)
        message = client.messages.create(
            body=message_data, from_=self.twilio_phone_number, to=self.user_phone_number)
        print(message.status)
