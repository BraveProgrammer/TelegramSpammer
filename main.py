from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
from telethon.tl.functions.messages import ReportRequest
from telethon.sync import TelegramClient, events
from telethon.tl.types import *
from colorama import init, Fore, Back, Style
import configparser, click, random, os
from progress.bar import Bar

config = configparser.ConfigParser()
config.read("config.ini")
api_id = config["auth"]["api_id"]
api_hash = config["auth"]["api_hash"]
phone = config["auth"]["phone"]
try: bot_token = config["auth"]["bot_token"]
except: bot_token = None
name = config["auth"]["name"]

client = TelegramClient(name, api_id, api_hash)
init(autoreset=True)

if bot_token: client.start(bot_token=bot_token)
else: client.start(phone)

@click.group()
def cli(): pass

@cli.command()
@click.argument("target")
@click.option("-c", "--count", type=int, default=1, help="Number of messages.")
@click.option("-f", "--file", default=None, help="File.")
def send_text(target, count, file):
	print(f"{Fore.BLUE}[{Fore.WHITE}*{Fore.BLUE}]{Fore.WHITE} {Fore.GREEN}File:{Fore.WHITE} {file}, {Fore.GREEN}Target:{Fore.WHITE} {target}, {Fore.GREEN}Count:{Fore.WHITE} {count}")
	file = open(file, 'r').read().splitlines()
	bar = Bar("Processing", fill='█', max=count)
	i = 0
	for c in range(count):
		try:
			client.send_message(target, file[i])
			i += 1
			bar.next()
		except IndexError:
			i = 0
			client.send_message(target, file[i])
			bar.next()
	bar.finish()
	print(f"{Fore.BLUE}[{Fore.WHITE}*{Fore.BLUE}]{Fore.GREEN} Done.")

@cli.command()
def auth():
	os.remove(f"{name}.session")
	client = TelegramClient(name, api_id, api_hash)
	if bot_token: client.start(bot_token=bot_token)
	else: client.start(phone)
	client.disconnect()
	print(f"{Fore.BLUE}[{Fore.WHITE}*{Fore.BLUE}]{Fore.GREEN} Done.")

@cli.command()
@click.argument("id")
def join(id):
	try:
		client(JoinChannelRequest(id))
		print(f"{Fore.BLUE}[{Fore.WHITE}*{Fore.BLUE}]{Fore.GREEN} Joined.")
	except: print(f"{Fore.BLUE}[{Fore.WHITE}*{Fore.BLUE}]{Fore.RED} Can't Join.")

@cli.command()
@click.argument("id")
def leave(id):
	try:
		client(LeaveChannelRequest(id))
		print(f"{Fore.BLUE}[{Fore.WHITE}*{Fore.BLUE}]{Fore.GREEN} Left.")
	except: print(f"{Fore.BLUE}[{Fore.WHITE}*{Fore.BLUE}]{Fore.RED} Can't Leave.")

@cli.command()
@click.argument("id")
@click.argument("type", type=click.Choice(["porn", "spam", "violence", "other"]))
@click.option("-c", "--count", type=int, default=1, help="Number of reports.")
def report(id, type, count):
	print(f"{Fore.BLUE}[{Fore.WHITE}*{Fore.BLUE}]{Fore.WHITE} {Fore.GREEN}Type:{Fore.WHITE} {type}, {Fore.GREEN}Target:{Fore.WHITE} {id}, {Fore.GREEN}Count:{Fore.WHITE} {count}")
	if type == "porn": reason = InputReportReasonPornography()
	if type == "spam": reason = InputReportReasonPornography()
	if type == "violence": reason = InputReportReasonViolence()
	if type == "other": reason = InputReportReasonOther()
	bar = Bar("Processing", fill='█', max=count)
	for c in range(count):
		client(ReportRequest(id, id=[42], reason=reason))
		bar.next()
	bar.finish()
	print(f"{Fore.BLUE}[{Fore.WHITE}*{Fore.BLUE}]{Fore.GREEN} Done.")

cli()
client.run_until_disconnected()
