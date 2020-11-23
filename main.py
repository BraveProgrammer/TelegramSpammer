from telethon.sync import TelegramClient, events
from colorama import init, Fore, Back, Style
import configparser, click, random
from progress.bar import Bar

config = configparser.ConfigParser()
config.read("config.ini")
api_id = config["auth"]["api_id"]
api_hash = config["auth"]["api_hash"]
phone = config["auth"]["phone"]

with TelegramClient("spammer", api_id, api_hash) as client:
	init(autoreset=True)
	client.start(phone)
	@click.group()
	def cli(): pass
	@cli.command()
	@click.argument("target")
	@click.option("-n", "--count", default=1, help="Number of messages.")
	@click.option("-t", "--text", help="Text.")
	@click.option("-f", "--file", default=None, help="File.")
	def send_text(target, count, text, file):
		print(f"{Fore.BLUE}[{Fore.WHITE}*{Fore.BLUE}]{Fore.WHITE} {'Text' if not file else 'File'}: {text if not file else file}, Target: {target}, Count: {count}")
		if file: file = open(file, 'r').read().splitlines()
		if not file:
			bar = Bar("Processing", max=count)
			for c in range(count):
				client.send_message(target, text)
				bar.next()
			bar.finish()
			print(f"\n{Fore.BLUE}[{Fore.WHITE}*{Fore.BLUE}]{Fore.WHITE} Done.")
		else:
			c = 0
			bar = Bar("Processing", max=count)
			for line in file:
				if c == count:
					print(f"\n{Fore.BLUE}[{Fore.WHITE}*{Fore.BLUE}]{Fore.WHITE} Done.")
					break
				client.send_message(target, line)
				c += 1
				bar.next()
			bar.finish()
	cli()
	client.run_until_disconnected()
