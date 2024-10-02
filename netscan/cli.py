#!/usr/bin/env python3

# built-in modules, does not need pre-checking
from datetime import datetime
import textwrap
import argparse
import shutil
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
	from scripts import *

# for deploy
except ModuleNotFoundError as e:
	try:
		from netscan.scripts import *

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
	target = args.target.split(',')
	port = args.port

	config_file = "netscan.conf"
	port_scanner = PortScanner(config_file, target, port)
	port_scanner.verbose = args.verbose

	if args.output:
		port_scanner.save_result = True
		port_scanner.output_file = args.output

	port_scanner.start_scan()

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
				("vuln","scan for known vulnerabilities on a host and generate report"),
				("ping", "ping a host to check its availability"),
				"\nsee '[command] --manual' for more info"
			]

			terminal_width = shutil.get_terminal_size().columns
			max_width = terminal_width - 20
			parsed = parse_manual(lines, max_width=max_width, mid_indent=10)

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

	args = parser.parse_args()

	if args.command == "port":
		if args.manual:
			manual.port_scanner()
			exit()

		else:
			if args.target is None:
				print(f"[netscan] the following arguments are required: -t/--target")
				exit()

			start_port_scanning(args)

	else:
		parser.print_help()

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print(f"\r\r\r\r\n{bracket('info')} stopped by user")
		exit()
