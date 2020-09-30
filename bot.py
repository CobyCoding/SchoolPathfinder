""" This file will store the TelegramBot class. This class will deal with the API.
"""

# Imports
import requests
import json
import telepot


class TelegramBot():
    """This class will deal with the telegram API.

    Note:
    Some things in this class are done via the python module telepot.
    Others are done via the requests module.
    """

    def __init__(self):
        # The "SchoolBot" API token
        self.token = "1318361251:AAHYjfIBsz1Tan8N65P13bSWRKFjhUqnnjw"
        # The base API url
        self.base = "https://api.telegram.org/bot{}/".format(self.token)
        # Generate a telepot bot with the API token. This is used in the send_photo function
        self.bot = telepot.Bot(self.token)

    def get_updates(self, offset=None):
        """This function will get all the messages that have been sent to the bot.

        Returns:
            dict: A list of all the messages that have been sent in json format.
        """

        url = self.base + "getUpdates?timeout=100"
        if offset:
            url = url + "&offset={}".format(offset + 1)
        r = requests.get(url)
        return json.loads(r.content)  # Return the dict in json data

    def send_message(self, msg, chat_id):
        """This function will send a message to a specific chat.

        Args:
            msg (str): The message you want to send.
            chat_id (int): The chat_id of the user you want to message.
        """
        url = self.base + "sendMessage?chat_id={}&text={}".format(chat_id, msg)
        if msg is not None:
            requests.get(url)

    def send_photo(self, path, chat_id):
        """This function will send a photo to a specific chat.

        Args:
            path (str): The path of the photo to send.
            chat_id (int):  The chat_id of the user you want to send the photo to.
        """

        self.bot.sendPhoto(chat_id, photo=open(path, "rb"))
