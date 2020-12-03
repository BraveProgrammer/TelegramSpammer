#!/bin/python3

from utils import *
from utils import _sendtext_thread, _report_thread
from multiprocessing import Process

class ArgumentParser(argparse.ArgumentParser):
	def format_help(self): return self.usage

class Prompt(cmd.Cmd):
	def __init__(self):
		self.intro = banner
		self.prompt = STYLE_BRIGHT + STYLE_UNDERLINE + FORE_WHITE + "tlsp" + RESET + " > "
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
			print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Sending {count*len(file)*int(client_count)} messages .....")
			print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Target: {target}")
			print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] File: {file}")
			file = open(file, 'r').read().splitlines()
			entity = client0.get_entity(target)
			t = time.time()
			process = Process(target=_sendtext_thread, args=(count, file, clients, target, t, entity,))
			process.start()
			process.join()
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
			print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Reporting {count*int(client_count)} Times .....")
			print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Target: {target}")
			print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Type: {type}")
			entity = client0.get_entity(target)
			t = time.time()
			process = Process(target=_report_thread, args=(count, clients, target, t, type, entity,))
			process.start()
			process.join()
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
			print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Joining {id} .....")
			try:
				if private: exec(f"client{client_num}(functions.messages.ImportChatInviteRequest('{id}'))")
				else: exec(f"client{client_num}(functions.channels.JoinChannelRequest('{id}'))")
			except KeyboardInterrupt: print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] {FORE_RED}Interrupted.{FORE_WHITE}")
			except: print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] {FORE_RED}You can't join this chat.")
			else: print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Done.")
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
			print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Leaving {id} .....")
			try: exec(f"client{client_num}.delete_dialog('{id}')")
			except KeyboardInterrupt: print(f"\n{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] {FORE_RED}Interrupted.{FORE_WHITE}")
			except UserNotParticipantError: print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] {FORE_RED}You are not a member of this chat.{FORE_WHITE}")
			except: print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] {FORE_RED}You can't leave this chat.")
			else: print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Done.")
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
	def do_block(self, arg):
		__doc__ = formatter(open("help/block", 'r').read())
		def _block(id, client_num):
			print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Blocking {id} .....")
			try: exec(f"client{client_num}(functions.contacts.BlockRequest('{id}'))")
			except KeyboardInterrupt: print(f"\n{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] {FORE_RED}Interrupted.{FORE_WHITE}")
			except: print(f"\n{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] {FORE_RED}You can't block this user.")
			else: print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Done.")
		arg = shlex.split(arg)
		parser = ArgumentParser(prog="exit", add_help=False, usage=__doc__)
		parser.add_argument("-v", "--version", action="version", version="%(prog)s 1.0")
		parser.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS)
		parser.add_argument("id")
		parser.add_argument("client_num")
		try:
			args = parser.parse_args(arg)
			_block(args.id, args.client_num)
		except SystemExit: pass
		except EOFError: pass
	def do_unblock(self, arg):
		__doc__ = formatter(open("help/unblock", 'r').read())
		def _block(id, client_num):
			print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Unblocking {id} .....")
			try: exec(f"client{client_num}(functions.contacts.UnblockRequest('{id}'))")
			except KeyboardInterrupt: print(f"\n{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] {FORE_RED}Interrupted.{FORE_WHITE}")
			except: print(f"\n{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] {FORE_RED}You can't unblock this user.")
			else: print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Done.")
		arg = shlex.split(arg)
		parser = ArgumentParser(prog="exit", add_help=False, usage=__doc__)
		parser.add_argument("-v", "--version", action="version", version="%(prog)s 1.0")
		parser.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS)
		parser.add_argument("id")
		parser.add_argument("client_num")
		try:
			args = parser.parse_args(arg)
			_block(args.id, args.client_num)
		except SystemExit: pass
		except EOFError: pass
	def do_deleteaccount(self, arg):
		__doc__ = formatter(open("help/deleteaccount", 'r').read())
		def _block(client_num):
			print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Are you sure (y/n)? {Fore.WHITE}", end='')
			if input() == "y":
				print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] if you are sure say yes. {Fore.WHITE}", end='')
				if input() == "yes":
					print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] if you are sure say 'I am Sure!'. {Fore.WHITE}", end='')
					if input() == "I am Sure!":
						print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Deleting Account {client_num} .....")
						try:
							exec(f"client{client_num}(functions.account.DeleteAccountRequest('{reason}'))")
							exec(f"del client{client_num}")
							exec(f"del clients[{client_num}]")
						except KeyboardInterrupt: print(f"\n{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] {FORE_RED}Interrupted.{FORE_WHITE}")
						except: print(f"\n{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] {FORE_RED}You can't delete this account.")
						else: print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] Done.")
					else: print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] {FORE_RED}Cancel.{FORE_WHITE}")
				else: print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] {FORE_RED}Cancel.{FORE_WHITE}")
			else: print(f"{FORE_GREEN}[{FORE_WHITE}+{FORE_GREEN}] {FORE_RED}Cancel.{FORE_WHITE}")
		arg = shlex.split(arg)
		parser = ArgumentParser(prog="exit", add_help=False, usage=__doc__)
		parser.add_argument("-v", "--version", action="version", version="%(prog)s 1.0")
		parser.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS)
		parser.add_argument("client_num")
		parser.add_argument("reason")
		try:
			args = parser.parse_args(arg)
			_block(args.client_num)
		except SystemExit: pass
		except EOFError: pass
	def do_help(self, arg):
		__doc__ = formatter(open("help/help", 'r').read())
		def _help(name):
			try:
				text = open(f"help/{name}", 'r').read()
				text = formatter(text)
				print(text)
			except FileNotFoundError: print(FORE_RED + f"Unknown command \"{name}\"")
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

if __name__ == "__main__": main()
