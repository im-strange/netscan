#!/usr/bin/env python3

# colors
BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
LIGHT_GRAY = '\033[37m'
DARK_GRAY = '\033[90m'
BRIGHT_RED = '\033[91m'
BRIGHT_GREEN = '\033[92m'
BRIGHT_YELLOW = '\033[93m'
BRIGHT_BLUE = '\033[94m'
BRIGHT_MAGENTA = '\033[95m'
BRIGHT_CYAN = '\033[96m'
WHITE = '\033[97m'
RESET = '\033[0m'


# import libraries
try:
	from tqdm import tqdm
	import threading
	import argparse
	import socket
	import time
	import json
	import os

except ModuleNotFoundError as error:
	print(f"{DARK_GRAY}[{YELLOW}NETSCAN{DARK_GRAY}] {YELLOW}{error}")


# parse port
def port_parser(port_str):
	if "-" in port_str:
		pattern = port_str.split("-")
		start_port, end_port = int(pattern[0]), int(pattern[1])
		port_list = list(range(start_port, end_port + 1))
		return port_list
	elif "," in port_str:
		ports = [int(port) for port in port_str.split(",")]
		return ports
	else:
		return [int(port_str)]


# limit service name length
def limit(name):
	max_length = 30
	return name if len(name) <= max_length else name[:max_length+1] + ".."


# get port service name
json_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ports.json")
with open(json_file, "r") as file:
	services = json.load(file)

def service_name(ports):
	service_list = []
	for port in ports:
		name = services.get(str(port))
		if name:
			service_list.append([port, limit(name[0]["description"])])
		else:
			service_list.append([port, "unknown service"])
	return service_list


# scan a port
def scan_port(host, port, open_ports):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
		sock.settimeout(1)
		try:
			sock.connect((host, port))
			open_ports.append(port)
		except (socket.timeout, ConnectionRefusedError):
			pass


# scan ports
def scan_ports(host, ports):
	open_ports = []
	thread_list = []
	for port in tqdm(ports, leave=False):
		thread = threading.Thread(target=scan_port, args=(host, port, open_ports))
		thread_list.append(thread)
		thread.start()
	for t in thread_list:
		t.join()
	return open_ports


# display
def display_result(host, target_ports, open_ports):
	print(f"{DARK_GRAY}[{YELLOW}INFO{DARK_GRAY}] {MAGENTA}@{host} {YELLOW}{len(open_ports)}/{len(target_ports)} were found open{RESET}")
	if len(open_ports) > 0:
		time.sleep(0.01)
		open_ports = service_name(open_ports)
		print(f"\t{CYAN}{'PORT':<10}SERVICE{RESET}")
		for port in open_ports:
			print(f"\t{port[0]:<10}{port[1]}")
			time.sleep(0.01)
	print()


# scan multiple host
def scan_multiple(hosts, ports):
	for host in hosts:
		open_ports = scan_ports(host, ports)
		display_result(host, ports, open_ports)


# main
def main():
	try:
		# cli info
		cli_version = "netscan 1.1.0"

		# custom parser
		class CustomArgumentParser(argparse.ArgumentParser):
			def print_help(self):
				lines = [
					f"usage: netscan <target_host> [OPTIONS]",
					f"\noptions:",
					f"{' '*4}{'-h, --help':<15} show this help message and exit",
					f"{' '*4}{'-v, --version':<15} show this cli version",
					f"{' '*4}{'-p, --port':<15} single, range, or comma-separated"
				]
				for line in lines:
					print(line)

			def error(self, message):
				print(f"{DARK_GRAY}[{YELLOW}NETSCAN{DARK_GRAY}] {RESET}{message}")
				print()
				self.print_help()
				exit(2)

		parser = CustomArgumentParser()
		parser.add_argument("target", type=str, help="target host")
		parser.add_argument("-v", "--version", action="version", version=cli_version)
		parser.add_argument("-p", "--port", default="1-1000", help="target port: range or comma-separated")

		# arguments
		args = parser.parse_args()
		target_hosts = args.target.split(",")
		target_ports = args.port
		port_list = port_parser(args.port)

		# display
		print(f"\n{DARK_GRAY}[{YELLOW}INFO{DARK_GRAY}] {YELLOW}netscan started{RESET}")
		time.sleep(0.01)
		print(f"\t{CYAN}{'HOST':<10}{RESET}{target_hosts}{RESET}")
		time.sleep(0.01)
		print(f"\t{CYAN}{'PORT':<10}{RESET}{target_ports}{RESET}")
		time.sleep(0.01)
		print()

		processes = scan_multiple(target_hosts, port_list)

	except KeyboardInterrupt:
		print(f"\n{DARK_GRAY}[{YELLOW}STOPPED{DARK_GRAY}] {YELLOW}keyboard interrupt{RESET}\n")


if __name__ == "__main__":
	main()
