#!/bin/python3

import argparse, atexit, cmd, configparser, os, random, readline, shlex, sys
from telethon.tl import functions, types
from telethon.sync import TelegramClient, events
from telethon.errors.rpcerrorlist import *
from progress.bar import Bar
from utils import *
import time

banner = formatter(open("banner", 'r').read())

config = configparser.ConfigParser()
config.read("config.ini")
api_id = config["auth"]["api_id"]
api_hash = config["auth"]["api_hash"]
client_count = config["auth"]["client_count"]
clients = []

for i in range(int(client_count)):
	print(f"\n{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] Starting Client {i} .....")
	exec(f"client{i}_phone = config['client{i}']['phone']")
	exec(f"client{i}_name = config['client{i}']['name']")
	exec(f"client{i} = TelegramClient(client{i}_name, api_id, api_hash)")
	exec(f"client{i}.start(client{i}_phone)")
	exec(f"clients.append(client{i})")
	print(f"\n{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] Client {i} Started.")

class ArgumentParser(argparse.ArgumentParser):
	def format_help(self): return self.usage

class Prompt(cmd.Cmd):
	def __init__(self):
		self.intro = banner
		self.prompt = Style.BRIGHT + "\033[4m" + "tlsp" + "\033[0m" + Style.RESET_ALL + " > "
		self.path = ''
		super().__init__()
	def cmdloop(self, intro=None):
		self.preloop()
		if self.use_rawinput and self.completekey:
			try:
				self.old_completer = readline.get_completer()
				readline.set_completer(self.complete)
				readline.parse_and_bind(self.completekey + ": complete")
			except ImportError: pass
		try:
			if intro is not None: self.intro = intro
			if self.intro: self.stdout.write(str(self.intro) + "\n")
			stop = None
			while not stop:
				if self.cmdqueue: line = self.cmdqueue.pop(0)
				else:
					if self.use_rawinput:
						try: line = input(self.prompt)
						except EOFError: line = "EOF"
						except KeyboardInterrupt: line = "^C"
					else:
						self.stdout.write(self.prompt)
						self.stdout.flush()
						line = self.stdin.readline()
						if not len(line): line = "EOF"
						else: line = line.rstrip("\r\n")
				line = self.precmd(line)
				stop = self.onecmd(line)
				stop = self.postcmd(stop, line)
			self.postloop()
		finally:
			if self.use_rawinput and self.completekey:
				try: readline.set_completer(self.old_completer)
				except ImportError: pass
	def do_exit(self, arg):
		__doc__ = formatter(open("help/exit", 'r').read())
		def _exit(): sys.exit(0)
		arg = shlex.split(arg)
		parser = ArgumentParser(prog="exit", add_help=False, usage=__doc__)
		parser.add_argument("-v", "--version", action="version", version="%(prog)s 1.0")
		parser.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS)
		parser.parse_args(arg)
		_exit()
	def do_clear(self, arg):
		__doc__ = formatter(open("help/clear", 'r').read())
		def _clear(): os.system("clear")
		arg = shlex.split(arg)
		parser = ArgumentParser(prog="clear", add_help=False, usage=__doc__)
		parser.add_argument("-v", "--version", action="version", version="%(prog)s 1.0")
		parser.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS)
		try:
			parser.parse_args(arg)
			_clear()
		except SystemExit: pass
	def do_banner(self, arg):
		__doc__ = formatter(open("help/banner", 'r').read())
		def _banner(): print(banner)
		arg = shlex.split(arg)
		parser = ArgumentParser(prog="banner", add_help=False, usage=__doc__)
		parser.add_argument("-v", "--version", action="version", version="%(prog)s 1.0")
		parser.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS)
		try:
			parser.parse_args(arg)
			_banner()
		except SystemExit: pass
	def do_history(self, arg):
		__doc__ = formatter(open("help/history", 'r').read())
		def _history(clear):
			if clear == False: print(open(os.path.expanduser("~/.tlsp_history"), 'r').read())
			elif clear == True: open(os.path.expanduser("~/.tlsp_history"), 'w').close()
		arg = shlex.split(arg)
		parser = ArgumentParser(prog="history", add_help=False, usage=__doc__)
		parser.add_argument("-v", "--version", action="version", version="%(prog)s 1.0")
		parser.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS)
		parser.add_argument("-c", "--clear", action="store_true")
		try:
			args = parser.parse_args(arg)
			_history(args.clear)
		except SystemExit: pass
	def do_sendtext(self, arg):
		__doc__ = formatter(open("help/sendtext", 'r').read())
		def _sendtext(target, count, file):
			count *= int(client_count)
			print(f"{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] Sending {count*len(file)*int(client_count)} messages .....")
			print(f"{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] Target: {target}")
			print(f"{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] File: {file}")
			file = open(file, 'r').read().splitlines()
			bar = Bar("\tProcessing", fill='█', max=count*len(file)*int(client_count))
			ct = 0
			check = False
			try:
				t = time.time()
				for c in range(count):
					for i in file:
						for cl in clients:
							if ct == count*len(file)*int(client_count): break
							if not check:
								entity = cl.get_entity(target)
								check = True
							cl(functions.messages.SendMessageRequest(peer=entity, message=i))
							bar.next()
							ct += 1
			except KeyboardInterrupt: print(f"\n{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] {Fore.RED}Interrupted.")
			except: print(f"\n{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] {Fore.RED}Can't send message to this chat.")
			else:
				print(f"\n{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] Time: {time.time() - t}")
				print(f"{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] Done.")
			bar.finish()
		arg = shlex.split(arg)
		parser = ArgumentParser(prog="exit", add_help=False, usage=__doc__)
		parser.add_argument("-v", "--version", action="version", version="%(prog)s 1.0")
		parser.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS)
		parser.add_argument("-c", "--count", type=int, default=1)
		parser.add_argument("-f", "--file", required=True)
		parser.add_argument("target")
		try:
			args = parser.parse_args(arg)
			_sendtext(args.target, args.count, args.file)
		except SystemExit: pass
		except EOFError: pass
	def do_report(self, arg):
		__doc__ = formatter(open("help/report", 'r').read())
		def _report(target, count, type):
			count *= int(client_count)
			print(f"{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] Reporting {count} Times .....")
			print(f"{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] Target: {target}")
			print(f"{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] Type: {type}")
			bar = Bar("\tProcessing", fill='█', max=count*int(client_count))
			ct = 0
			check = False
			try:
				t = time.time()
				for c in range(count):
					for cl in clients:
						if ct == count*int(client_count): break
						if not check:
							entity = cl.get_entity(target)
							check = True
						cl(functions.account.ReportPeerRequest(peer=entity, reason=rep_types[type]()))
						bar.next()
						ct += 1
			except KeyboardInterrupt: print(f"\n{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] {Fore.RED}Interrupted.")
			except: print(f"\n{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] {Fore.RED}Can't report this peer.")
			else:
				print(f"\n{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] Time: {time.time() - t}")
				print(f"{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] Done.")
			bar.finish()
		arg = shlex.split(arg)
		rep_types = {"porn": types.InputReportReasonPornography, "spam": types.InputReportReasonSpam, "copyright": types.InputReportReasonCopyright, "childabuse": types.InputReportReasonChildAbuse, "violence": types.InputReportReasonViolence, "geoirrelevant": types.InputReportReasonGeoIrrelevant}
		parser = ArgumentParser(prog="exit", add_help=False, usage=__doc__)
		parser.add_argument("-v", "--version", action="version", version="%(prog)s 1.0")
		parser.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS)
		parser.add_argument("-c", "--count", type=int, default=1)
		parser.add_argument("target")
		parser.add_argument("type", choices=rep_types.keys())
		try:
			args = parser.parse_args(arg)
			_report(args.target, args.count, args.type)
		except SystemExit: pass
		except EOFError: pass
	def do_join(self, arg):
		__doc__ = formatter(open("help/join", 'r').read())
		def _join(id, client_num, private):
			print(f"{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] Joining {id} .....")
			try:
				if private: exec(f"client{client_num}(functions.messages.ImportChatInviteRequest('{id}'))")
				else: exec(f"client{client_num}(functions.channels.JoinChannelRequest('{id}'))")
			except KeyboardInterrupt: print(f"\n{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] {Fore.RED}Interrupted.")
			except: print(f"\n{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] {Fore.RED}You can't join this chat.")
			else: print(f"\n{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] Done.")
		arg = shlex.split(arg)
		parser = ArgumentParser(prog="exit", add_help=False, usage=__doc__)
		parser.add_argument("-v", "--version", action="version", version="%(prog)s 1.0")
		parser.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS)
		parser.add_argument("-p", "--private", action="store_true")
		parser.add_argument("id")
		parser.add_argument("client_num")
		try:
			args = parser.parse_args(arg)
			_join(args.id, args.client_num, args.private)
		except SystemExit: pass
		except EOFError: pass
	def do_leave(self, arg):
		__doc__ = formatter(open("help/leave", 'r').read())
		def _leave(id, client_num):
			print(f"{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] Leaving {id} .....")
			try: exec(f"client{client_num}(functions.channels.LeaveChannelRequest('{id}'))")
			except KeyboardInterrupt: print(f"\n{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] {Fore.RED}Interrupted.")
			except: print(f"\n{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] {Fore.RED}You can't leave this chat.")
			else: print(f"\n{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] Done.")
		arg = shlex.split(arg)
		parser = ArgumentParser(prog="exit", add_help=False, usage=__doc__)
		parser.add_argument("-v", "--version", action="version", version="%(prog)s 1.0")
		parser.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS)
		parser.add_argument("id")
		parser.add_argument("client_num")
		try:
			args = parser.parse_args(arg)
			_leave(args.id, args.client_num)
		except SystemExit: pass
		except EOFError: pass
	def do_help(self, arg):
		__doc__ = formatter(open("help/help", 'r').read())
		def _help(name):
			try:
				text = open(f"help/{name}", 'r').read()
				text = formatter(text)
				print(text)
			except FileNotFoundError: print(Fore.RED + f"Unknown command \"{name}\"")
		arg = shlex.split(arg)
		parser = ArgumentParser(prog="help", add_help=False, usage=__doc__)
		parser.add_argument("-v", "--version", action="version", version="%(prog)s 1.0")
		parser.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS)
		parser.add_argument("name")
		try:
			args = parser.parse_args(arg)
			_help(args.name)
		except SystemExit: pass
	def complete_help(self, text, line, start_index, end_index):
		if text:
			return [
				hlp for hlp in os.listdir("help/")
				if hlp.startswith(text)
			]
		else: return os.listdir("help/")

def save_history(prev_h_len, histfile):
	new_h_len = readline.get_current_history_length()
	readline.set_history_length(1000)
	readline.append_history_file(new_h_len - prev_h_len, histfile)

def main():
	init(autoreset=True)
	histfile = os.path.join(os.path.expanduser('~'), ".tlsp_history")
	try:
		readline.read_history_file(histfile)
		h_len = readline.get_current_history_length()
	except FileNotFoundError:
		open(histfile, "wb").close()
		h_len = 0
	atexit.register(save_history, h_len, histfile)
	prompt = Prompt()
	prompt.cmdloop()

if __name__ == "__main__":
    main()
