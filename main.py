from telethon.sync import TelegramClient, events
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
api_id = config["auth"]["api_id"]
api_hash = config["auth"]["api_hash"]
phone = config["auth"]["phone"]

with TelegramClient("spammer", api_id, api_hash) as client:
	client.start(phone)
	client.send_message("me", "Hello, myself!")
	client.run_until_disconnected()
