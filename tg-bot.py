
import telebot
import getlink
from simplebot import SimpleBot
import csv
from datetime import datetime

CSV_FILE = "tg-bot-clients.csv"
BOT_TOKEN = "6988486796:AAFxK05_KtkXD1WZRwO0fyjKHc3Uz9vE4V0"
NGROK_LINK = getlink.get_ngrok_link()
WARNING_MSG = """
Attention: This platform is designed for respectful and responsible communication. Engage in conversations with kindness and empathy. 

Any form of harassment, hate speech, or inappropriate behavior is strictly prohibited. Remember that anonymity doesn't justify harmful actions. Please maintain a safe and positive environment for everyone.
"""
SCHEDULE = """
The server will be online only in the following period:

- Friday 10:00pm to 2:00am
"""
HOW_MSG = """
To start chatting with strangers,

1. Kindly use /link command to get a free link.
2. Open the given link

Note that this link will renew due to server maintenance. See the /sched command.
"""
WELCOME_MSG = """
Hi, Pollify here! How can I help?

/link - get the link for chat
/sched - get the schedule of the chat
/how - how to start chatting
"""

def write_csv(data):
    current_time = datetime.now().strftime("%B %d, %Y %I:%M:%S %p")
    data.append(current_time)
    current = list(csv.reader(open(CSV_FILE)))
    current.append(data)
    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(current)

bot = telebot.TeleBot(BOT_TOKEN)
mybot = SimpleBot()
mybot.train("intents.json")

available_commands = ["/start", "/link", "/sched", "/how"]

@bot.message_handler(commands=["start"])
def start(message):
    id = message.chat.id
    user = message.chat.username
    bot.send_message(id, WELCOME_MSG)
    write_csv([user, message.text])
    print(f"new message from {user}: {message.text}")

@bot.message_handler(commands=["link"])
def link(message):
    id = message.chat.id
    user = message.chat.username
    bot.send_message(id, f"Here's the free link for today's Pollify chat: {NGROK_LINK}")
    bot.send_message(id, WARNING_MSG)
    write_csv([user, message.text])
    print(f"new message from {user}: {message.text}")

@bot.message_handler(commands=["how"])
def how(message):
    id = message.chat.id
    user = message.chat.username
    bot.send_message(id, HOW_MSG)
    write_csv([user, message.text])
    print(f"new message from {user}: {message.text}")

@bot.message_handler(commands=["sched"])
def sched(message):
    id = message.chat.id
    user = message.chat.username
    bot.send_message(id, SCHEDULE)
    write_csv([user, message.text])
    print(f"new message from {user}: {message.text}")

@bot.message_handler(func=lambda m: True)
def process_messages(message):
    id = message.chat.id
    user = message.chat.username
    text = message.text
    text_list = (message.text).split()

    if any(item in available_commands for item in text_list) and len(text_list) == 1:
        pass
    else:
        response = mybot.respond(text)

    bot.send_message(id, response)
    print(f"new message from {user}: {message.text}")
    write_csv([user, message.text])

bot.infinity_polling()
