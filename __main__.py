from bot import TelegramBot
import sys
import os

# Fix pathing issues with Windows
sys.path.insert(1, '../SchoolPathFinder')

import a
import threading
from threading import Thread
import signal
import time
import sys
bot = TelegramBot()

def exit_gracefully(signum, frame):
    # restore the original signal handler as otherwise evil things will happen
    # in raw_input when CTRL+C is pressed, and our signal handler is not re-entrant
    signal.signal(signal.SIGINT, original_sigint)

    # restore the exit gracefully handler here    
    sys.exit()

def UpdateQueuePosition(bot, one, chat_id="ID", item=""):
    if one:
        bot.send_message("You are " + str(CurrentQueue.index(item) + 1) + " in the queue", chat_id)
    else:
        for item in CurrentQueue:
            bot.send_message("You are " + str(CurrentQueue.index(item) + 1) + " in the queue", item["message"]["from"]["id"])

def Queue(bot):
    global CurrentQueue
    CurrentQueue = []

    count = 0
    prevLength = 0
    while True:
        updates = bot.get_updates(offset=update_id)
        try:
            updates = updates["result"]
            for item in updates:
                if item not in CurrentQueue:
                    prevLength = len(CurrentQueue)
                    CurrentQueue.append(item)
                    _from = item["message"]["from"]["id"]
                    UpdateQueuePosition(bot, True, _from, item)
                    print(item)
        except:
            pass

def DeletePhoto(Path):
    os.remove(Path)

def run():
    global update_id
    update_id = None

    global t1
    t1 = threading.Thread(target=Queue, args=[bot])
    t1.start()

    while True:
        try:
            item = CurrentQueue[0]
            print("dont think im ever getting here.")
            print(item)
            try:
                update_id = item["update_id"]
                # try:
                message = item["message"]["text"]
                # except:
                    # message = None                    
                message = message.split(" ")

                if message[0] == "/start":
                    print("removing")
                    CurrentQueue.remove(item)
                else:
                    _from = item["message"]["from"]["id"]
                    if len(message) == 2:
                        # a.start()
                        pathList = a.main(message[0], message[1])
                        for path in pathList:
                            bot.send_photo(path, _from)
                        DeletePhoto(path)
                        CurrentQueue.remove(item)
                        print("removing item")
                        print(item)
                        UpdateQueuePosition(bot, False)
                    else:
                        print("message less than2")
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