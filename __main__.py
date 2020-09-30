import time
import signal
from threading import Thread
import threading
import pathFinder
from bot import TelegramBot
import sys
import os

# Fix pathing issues with Windows
sys.path.insert(1, '../SchoolPathFinder')

bot = TelegramBot()


def exit_gracefully(signum, frame):
    # restore the original signal handler as otherwise evil things will happen
    # in raw_input when CTRL+C is pressed, and our signal handler is not re-entrant
    signal.signal(signal.SIGINT, original_sigint)

    # restore the exit gracefully handler here
    sys.exit()


def UpdateQueuePosition(bot, one, chat_id=None, item=None):
    """This function will send a message to the user telling him what his position in the queue is

    Args:
        bot (TelegramBot): Please refer to bot.py
        one (bool): If send to only one user
        chat_id (int, optional): Chat id of user to send to. Defaults to None.
        item (dict, optional): [description]. Defaults to None.
    """
    if one:
        bot.send_message(
            "You are " + str(CurrentQueue.index(item) + 1) + " in the queue", chat_id)
    else:
        for item in CurrentQueue:
            bot.send_message("You are " + str(CurrentQueue.index(item) + 1) +
                             " in the queue", item["message"]["from"]["id"])


def Queue(bot):
    """This function will be ran as a separate thread and will handle queueing users requests

    Args:
        bot (TelegramBot): The bot used to send messages
    """

    global CurrentQueue
    CurrentQueue = []

    while True:
        updates = bot.get_updates(offset=update_id)
        try:
            updates = updates["result"]
            for item in updates:
                if item not in CurrentQueue:
                    CurrentQueue.append(item)
                    # Get the chat_id of the user that sent this request.
                    _from = item["message"]["from"]["id"]
                    UpdateQueuePosition(bot, True, _from, item)
                    print(item)
        except:
            pass


def DeletePhoto(Path):
    """This function deletes a photo

    Args:
        Path (str): The path of the photo to be deleted.
    """
    os.remove(Path)


def run():
    global update_id
    update_id = None

    global t1
    t1 = threading.Thread(target=Queue, args=[bot])
    t1.start()

    while True:
        try:
            # Attempt to get a request from the queue. If nothing in queue pass and go to next loop. Queue is updated in the seperate thread.
            item = CurrentQueue[0]
            try:
                update_id = item["update_id"]
                message = item["message"]["text"]
                message = message.split(" ")

                # If the user first starts the conversation it auto sends "/start" this just filters that out
                if message[0] == "/start":
                    CurrentQueue.remove(item)
                else:
                    _from = item["message"]["from"]["id"]
                    if len(message) == 2:
                        returnedData = pathFinder.main(message[0], message[1])
                        # If there is a issue in the algorithm
                        if not isinstance(returnedData, list):
                            bot.send_message(returnedData, _from)

                        else:  # If not issue in the algorithm
                            for path in returnedData:
                                bot.send_photo(path, _from)
                                DeletePhoto(path)

                        CurrentQueue.remove(item)
                        UpdateQueuePosition(bot, False)
                    else:
                        bot.send_message(
                            "[USER ERROR] Your message does not include 2 room numbers.", _from)
                        CurrentQueue.remove(item)

            except Exception as e:
                print(e)
                pass
        except:
            pass
    t1.join()


if __name__ == '__main__':
    # store the original SIGINT handler
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)
    run()
