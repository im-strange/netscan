#!/usr/bin/env python3

# built-in modules, does not need pre-checking
from datetime import datetime
import textwrap
import argparse
import time
import sys
import os

# colors
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
GRAY = '\033[90m'
RESET = '\033[0m'

# for development
try:
	from scripts.manuals import *
	from scripts.reinstall import reinstall_package
	from scripts.port_scanner import *
	from scripts.dirhunter import *

# for deploy
except ModuleNotFoundError as e:
	try:
		from netscan.scripts.manuals import *
		from netscan.scripts.reinstall import reinstall_package
		from netscan.scripts.port_scanner import *
		from netscan.scripts.dirhunter import *

	except ModuleNotFoundError as e:
		print(f"[netscan] {e}")
		exit(2)

# get current datetime
def current_time():
	current =  datetime.now().strftime('%m-%d-%Y %I:%M:%S%p')
	return current

# get the absolute path for a file
def path(file):
	return os.path.join(os.path.dirname(os.path.abspath(__file__)), file)

# print bracket
def bracket(text):
	return f"{GRAY}[{YELLOW}{text}{GRAY}]{RESET}"

# start port scanning
def start_port_scanning(args):
	if args.target is None:
		print(f"[netscan] required argument: -t/--target")
		exit()

	target = args.target.split(',')
	port = args.port

	config_file = "portscanner.conf"
	port_scanner = PortScanner(config_file, target, port)
	port_scanner.verbose = args.verbose

	if args.output:
		port_scanner.save_result = True
		port_scanner.output_file = args.output

	port_scanner.start_scan()

# start dir hunt
def start_dirhunter(args):
	if args.url is None:
		print(f"[netscan] required argument: -u/--url")
		exit()

	url = args.url
	wordlist = args.wordlist
	config_file = "dirhunter.conf"
	dirhunter = DirHunter(config_file, url, wordlist)

	if args.status_codes:
		try:
			dirhunter.status_codes = list(map(int, args.status_codes.split(",")))
		except ValueError:
			print(f"[info] invalid --status-code: {args.status_codes}")
			print(f"[info] must be single or comma-separated integer")
			exit()

	if args.thread_count: dirhunter.thread_count = args.thread_count
	if args.output_file: dirhunter.output_file = args.output_file
	if args.sleep_time: dirhunter.sleep_time = args.sleep_time
	if args.verbose: dirhunter.verbose = True

	dirhunter.display_settings()
	dirhunter.scan()

# main function to call
def main():
	manual = Manual()

	class CustomArgumentParser(argparse.ArgumentParser):
		def print_help(self):
			tabsize = 2
			max_width = 40

			lines = [
				"usage: netscan [commands] [options]",
				"\ncommands:",
				("port", "scan for open ports on a host"),
				("dirhunter", "web directory scanner using wordlists to find hidden files and directories"),
				("reinstall", "uninstall and reinstall the package. Useful for fixing issues"),
				"\nsee '[command] --manual' for more info"
			]

			parsed = parse_manual(lines, mid_indent=12)

			for line in parsed:
				print(line)
				time.sleep(0.01)

		def error(self, message):
			print(f"[netscan] {message}")
			print(f"[netscan] see '--help' for more info")
			exit(2)

	parser = CustomArgumentParser()
	subparsers = parser.add_subparsers(dest="command")

	# port scanning
	port_scanner = subparsers.add_parser("port")
	port_scanner.add_argument("-t", "--target", help="target host")
	port_scanner.add_argument("-p", "--port", default="1-1000")
	port_scanner.add_argument("-v", "--verbose", action="store_true")
	port_scanner.add_argument("-o", "--output")
	port_scanner.add_argument("--manual", action="store_true")

	# reinstall
	reinstall = subparsers.add_parser("reinstall")

	# dir hunter
	dirhunter = subparsers.add_parser("dirhunter")
	dirhunter.add_argument("-u", "--url")
	dirhunter.add_argument("-w", "--wordlist", default=path("scripts/dirhunter/list1.txt"))
	dirhunter.add_argument("-s", "--status-codes", dest="status_codes")
	dirhunter.add_argument("-t", "--threads", type=int, dest="thread_count")
	dirhunter.add_argument("-o", "--output", dest="output_file")
	dirhunter.add_argument("--sleep", type=float, dest="sleep_time")
	dirhunter.add_argument("--verbose", action="store_true")
	dirhunter.add_argument("--manual", action="store_true")

	args = parser.parse_args()

	# for port scan
	if args.command == "port":
		if args.manual:
			manual.port_scanner()
			exit()
		else:
			start_port_scanning(args)

	# for reinstalling
	elif args.command == "reinstall":
		reinstall_package()

	# for dirhunter
	elif args.command == "dirhunter":
		if args.manual:
			manual.dirhunter()
			exit()
		else:
			start_dirhunter(args)

	else:
		parser.print_help()

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print(f"\r\r\r\r\n{bracket('info')} stopped by user")
		exit()
