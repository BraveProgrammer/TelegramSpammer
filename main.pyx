#!/bin/python3

import configparser, os, signal, socks, sys, time
from telethon.tl import functions, types
from telethon.sync import TelegramClient
from progress.spinner import Spinner
from progress.bar import Bar

cdef str FORE_RED = "\u001b[31m"
cdef str FORE_GREEN = "\u001b[32m"
cdef str FORE_BLUE = "\u001b[34m"
cdef str FORE_CYAN = "\u001b[36m"
cdef str FORE_WHITE = "\u001b[37m"
cdef str RESET = "\u001b[0m"
cdef str BACK_RED = "\u001b[41m"
cdef str BACK_CYAN = "\u001b[46m"
cdef str STYLE_BRIGHT = "\u001b[1m"
cdef str STYLE_UNDERLINE = "\u001b[4m"

banner = f"\n{FORE_GREEN}  ______     __                             \n /_  __/__  / /__  ____ __________ _____ ___            \n  / / / _ \/ / _ \/ __ `/ ___/ __ `/ __ `__ \           \n / / /  __/ /  __/ /_/ / /  / /_/ / / / / / /           \n/_/  \___/_/\___/\__, /_/   \__,_/_/ /_/ /_/            \n        / ___/__/____/__ _____ ___  ____ ___  ___  _____\n        \__ \/ __ \/ __ `/ __ `__ \/ __ `__ \/ _ \/ ___/\n       ___/ / /_/ / /_/ / / / / / / / / / / /  __/ /    \n      /____/ .___/\__,_/_/ /_/ /_/_/ /_/ /_/\___/_/     \n          /_/                                           {FORE_WHITE}\n\n{BACK_CYAN}=========== Author: @BraveProgrammer ==========={RESET}\n{BACK_RED}      I'm Not Responsible For your Actions      {RESET}"
cdef str conf_file = os.path.expanduser("~/.tlsprc")

if sys.argv[1] == "conf": os.system(f"vim {conf_file}"); exit()

config = configparser.ConfigParser()
config.read(conf_file)
api_id = int(config["auth"]["api_id"])
api_hash = config["auth"]["api_hash"]
client_count = int(config["auth"]["client_count"])
clients = []

try:
	proxy_addr = config["proxy"]["addr"]
	proxy_port = int(config["proxy"]["port"])
	has_proxy = True
except: has_proxy = False

print(banner)

for i in range(client_count):
	print(f"\n{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Starting Client {i} .....")
	exec(f"""if has_proxy: client{i} = TelegramClient(config['client{i}']['name'], api_id, api_hash, proxy=(socks.SOCKS5, proxy_addr, proxy_port))
else: client{i} = TelegramClient(config['client{i}']['name'], api_id, api_hash)
client{i}.start(config['client{i}']['phone'])
clients.append(client{i})""")
	print(f"\n{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Client {i} Started.")

cdef int sendtext(target, count, file):
	cdef list msg = open(file, 'r').read().splitlines()
	print(f"\n{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Sending {count*len(msg)*client_count} messages .....")
	print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Target: {target}")
	print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] File: {file}")
	cdef object bar = Bar(FORE_WHITE+"\tProcessing ", fill='█', max=count*len(msg)*client_count)
	cdef double t = time.time()
	cdef list entities = []
	try:
		for c in range(client_count): entities.append((clients[c].get_entity(target)))
		for c in range(count):
			for c2 in range(client_count):
				for i in msg:
					clients[c2](functions.messages.SendMessageRequest(peer=entities[c2], message=i))
					bar.next()
	except KeyboardInterrupt:
		print(f"\n{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Time: {time.time() - t}")
		print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] {FORE_RED}Interrupted.{RESET}")
	except: print(f"\n{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] {FORE_RED}Can't send message to this chat.{RESET}")
	else:
		print(f"\n{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Time: {time.time() - t}")
		print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Done.{RESET}")
	bar.finish()

cdef int report(target, count, type):
	cdef dict rep_types = {"porn": types.InputReportReasonPornography, "spam": types.InputReportReasonSpam, "copyright": types.InputReportReasonCopyright, "childabuse": types.InputReportReasonChildAbuse, "violence": types.InputReportReasonViolence, "geoirrelevant": types.InputReportReasonGeoIrrelevant}
	print(f"\n{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Reporting {count*client_count} times .....")
	print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Target: {target}")
	print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Type: {type}")
	cdef object bar = Bar(FORE_WHITE+"\tProcessing ", fill='█', max=count*client_count)
	cdef double t = time.time()
	cdef list entities = []
	try:
		for c in range(client_count): entities.append((clients[c].get_entity(target)))
		for c in range(count):
			for c2 in range(client_count):
					clients[c2](functions.account.ReportPeerRequest(peer=entities[c2], reason=rep_types[type]()))
					bar.next()
	except KeyboardInterrupt:
		print(f"\n{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Time: {time.time() - t}")
		print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] {FORE_RED}Interrupted.{RESET}")
	except: print(f"\n{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] {FORE_RED}Can't report this person.{RESET}")
	else:
		print(f"\n{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Time: {time.time() - t}")
		print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Done.{RESET}")
	bar.finish()

cdef int forward(_from, target, count):
	print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Forwarding messages .....")
	print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Target: {target}")
	print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Count: {count}")
	cdef object spinner = Spinner(FORE_WHITE+"\tProcessing ")
	cdef double t = time.time()
	cdef list entities = []
	cdef list msgs = []
	try:
		for c in range(int(client_count)): msgs.append(clients[c].iter_messages(clients[c].get_entity(_from)))
		for c in range(client_count): entities.append((clients[c].get_entity(target)))
		for c in range(count):
			for c2 in range(int(client_count)):
				for i in msgs[c2]:
					clients[c2].send_message(entities[c2], i)
					spinner.next()
	except TypeError:
		print(f"\n{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Time: {time.time() - t}")
		print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Done.{RESET}")
	except KeyboardInterrupt:
		print(f"\n{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Time: {time.time() - t}")
		print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] {FORE_RED}Interrupted.{RESET}")
	#except: print(f"\n{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] {FORE_RED}Can't forward this message.{RESET}")
	else:
		print(f"\n{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Time: {time.time() - t}")
		print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Done.{RESET}")

cdef int join(id, client_num, private):
	print(f"\n{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Joining {id} .....")
	try:
		if private: clients[client_num](functions.messages.ImportChatInviteRequest(id))
		else: clients[client_num](functions.channels.JoinChannelRequest(id))
	except KeyboardInterrupt: print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] {FORE_RED}Interrupted.{RESET}")
	except: print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] {FORE_RED}You can't join this chat.{RESET}")
	else: print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Done.{RESET}")

cdef int leave(id, client_num):
	print(f"\n{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Leaving {id} .....")
	try: clients[client_num].delete_dialog(id)
	except KeyboardInterrupt: print(f"\n{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] {FORE_RED}Interrupted.{RESET}")
	except: print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] {FORE_RED}You can't leave this chat.{RESET}")
	else: print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Done.{RESET}")

cdef int block(id, client_num):
	print(f"\n{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Blocking {id} .....")
	try: clients[client_num](functions.contacts.BlockRequest(id))
	except KeyboardInterrupt: print(f"\n{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] {FORE_RED}Interrupted.{RESET}")
	except: print(f"\n{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] {FORE_RED}You can't block this user.{RESET}")
	else: print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Done.{RESET}")

cdef int unblock(id, client_num):
	print(f"\n{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Unblocking {id} .....")
	try: clients[client_num](functions.contacts.UnblockRequest(id))
	except KeyboardInterrupt: print(f"\n{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] {FORE_RED}Interrupted.{RESET}")
	except: print(f"\n{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] {FORE_RED}You can't unblock this user.{RESET}")
	else: print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Done.{RESET}")

if sys.argv[1] == "sendtext": sendtext(sys.argv[2], int(sys.argv[3]), sys.argv[4])
elif sys.argv[1] == "report": report(sys.argv[2], int(sys.argv[3]), sys.argv[4])
elif sys.argv[1] == "forward": forward(sys.argv[2], sys.argv[3], int(sys.argv[4]))
elif sys.argv[1] == "join":
	if sys.argv[4] == "private": state = True
	elif sys.argv[4] == "public": state = False
	join(sys.argv[2], int(sys.argv[3]), state)
elif sys.argv[1] == "leave": leave(sys.argv[2], int(sys.argv[3]))
elif sys.argv[1] == "block": block(sys.argv[2], int(sys.argv[3]))
elif sys.argv[1] == "unblock": unblock(sys.argv[2], int(sys.argv[3]))
else: print("\nNothing to do!")