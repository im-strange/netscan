#!/usr/bin/env python3

# built-in modules, does not need pre-checking
from datetime import datetime
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

print(sys.path)

# check if third-party modules are installed
try:
	from scripts import PortScanner

# else, tell the user
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

# main function to call
def main():
	class CustomArgumentParser(argparse.ArgumentParser):
		def print_help(self):
			tabsize = 2
			lines = [
				f"usage: netscan <host> [options]",
				f"\npositional arguments:",
				f"{' '*tabsize}{'target':<15} target host/s",
				f"{' '*tabsize}{'-p, --port':<15} target port/s [default=1-1000]",
				f"\noptional arguments:",
				f"{' '*tabsize}{'-v, --verbose':<15} print scanning info",
				f"{' '*tabsize}{'-o, --output':<15} output file to write",
				f"\nexamples:",
				f"{' '*tabsize}netscan 127.0.0.1 -p 22,80,443",
				f"{' '*tabsize}netscan example.com -o myresults.txt"
			]
			for line in lines:
				print(line)
				time.sleep(0.01)

		def error(self, message):
			print(f"[netscan] {message}")
			print(f"[netscan] see '--help' for more info")
			exit(2)

	parser = CustomArgumentParser()
	parser.add_argument("target")
	parser.add_argument("-p", "--port", default="1-1000")
	parser.add_argument("-v", "--verbose", action="store_true")
	parser.add_argument("-o", "--output")

	args = parser.parse_args()
	target = args.target.split(',')
	port = args.port

	config_file = "netscan.conf"
	port_scanner = PortScanner(config_file, target, port)
	port_scanner.verbose = args.verbose

	if args.output:
		port_scanner.save_result = True
		port_scanner.output_file = args.output

	port_scanner.start_scan()

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print(f"\r\r\r\r\n{bracket('info')} stopped by user")
		exit()
