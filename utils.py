import argparse, atexit, cmd, configparser, os, readline, shlex, sys, time
from telethon.tl import functions, types
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import *
from progress.bar import Bar
from progress.spinner import Spinner

FORE_RED = "\u001b[31m"
FORE_GREEN = "\u001b[32m"
FORE_BLUE = "\u001b[34m"
FORE_CYAN = "\u001b[36m"
FORE_WHITE = "\u001b[37m"
RESET = "\u001b[0m"
BACK_RED = "\u001b[41m"
BACK_CYAN = "\u001b[46m"
STYLE_BRIGHT = "\u001b[1m"
STYLE_UNDERLINE = "\u001b[4m"

def formatter(text):
	text = text.replace("{Fore.RED}", FORE_RED)
	text = text.replace("{Fore.GREEN}", FORE_GREEN)
	text = text.replace("{Fore.BLUE}", FORE_BLUE)
	text = text.replace("{Fore.CYAN}", FORE_CYAN)
	text = text.replace("{Fore.WHITE}", FORE_WHITE)
	text = text.replace("{RESET}", RESET)
	text = text.replace("{Back.RED}", BACK_RED)
	text = text.replace("{Back.CYAN}", BACK_CYAN)
	text = text.replace("{Style.BRIGHT}", STYLE_BRIGHT)
	text = text.replace("{Style.UNDERLINE}", STYLE_UNDERLINE)
	return text

banner = formatter(open("banner", 'r').read())

config = configparser.ConfigParser()
config.read("config.ini")
api_id = config["auth"]["api_id"]
api_hash = config["auth"]["api_hash"]
client_count = config["auth"]["client_count"]
clients = []

for i in range(int(client_count)):
	print(f"\n{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Starting Client {i} .....")
	exec(f"client{i}_phone = config['client{i}']['phone']")
	exec(f"client{i}_name = config['client{i}']['name']")
	exec(f"client{i} = TelegramClient(client{i}_name, api_id, api_hash)")
	exec(f"client{i}.start(client{i}_phone)")
	exec(f"clients.append(client{i})")
	print(f"\n{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Client {i} Started.")

def _sendtext_thread(count, file, clients, target, t, entity):
	bar = Bar(FORE_WHITE+"\tProcessing ", fill='█', max=count*len(file)*int(client_count))
	try:
		for c in range(count):
			for i in file:
				for cl in clients:
					cl(functions.messages.SendMessageRequest(peer=entity, message=i))
					bar.next()
		bar.finish()
	except KeyboardInterrupt:
		print(f"\n{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Time: {time.time() - t}")
		print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] {FORE_RED}Interrupted.{FORE_WHITE}")
	except: print(f"\n{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] {FORE_RED}Can't send message to this chat.")
	else:
		print(f"\n{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Time: {time.time() - t}")
		print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Done.")

def _report_thread(count, clients, target, t, type, entity):
	bar = Bar(FORE_WHITE+"\tProcessing ", fill='█', max=count*int(client_count))
	rep_types = {"porn": types.InputReportReasonPornography, "spam": types.InputReportReasonSpam, "copyright": types.InputReportReasonCopyright, "childabuse": types.InputReportReasonChildAbuse, "violence": types.InputReportReasonViolence, "geoirrelevant": types.InputReportReasonGeoIrrelevant}
	try:
		for c in range(count):
			for cl in clients:
				cl(functions.account.ReportPeerRequest(peer=entity, reason=rep_types[type]()))
				bar.next()
		bar.finish()
	except KeyboardInterrupt:
		print(f"\n{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Time: {time.time() - t}")
		print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] {FORE_RED}Interrupted.{FORE_WHITE}")
	except: print(f"\n{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] {FORE_RED}Can't report this peer.")
	else:
		print(f"\n{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Time: {time.time() - t}")
		print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Done.")

def _forward_thread(loop, clients, t, _from, to, entity):
	msg = client0.iter_messages(_from)
	spinner = Spinner(FORE_WHITE+"\tProcessing ")
	try:
		for i in msg:
			for l in range(0, 20):
				for cl in clients:
					cl.send_message(entity, i)
					spinner.next()
	except TypeError:
		print(f"\n{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Time: {time.time() - t}")
		print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Done.")
	except KeyboardInterrupt:
		print(f"\n{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Time: {time.time() - t}")
		print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] {FORE_RED}Interrupted.{FORE_WHITE}")
	except: print(f"\n{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] {FORE_RED}Can't forward this message.")
	else:
		print(f"\n{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Time: {time.time() - t}")
		print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Done.")
