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
	import json
	import os

except ModuleNotFoundError as error:
	print(f"[NETSCAN] {error}")


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


# get port service name
json_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ports.json")
with open(json_file, "r") as file:
	services = json.load(file)

def service_name(ports):
	service_list = []
	for port in ports:
		name = services.get(str(port))
		if name:
			service_list.append([port, name[0]["description"]])
		else:
			service_list.append([port, "unknown service"])
	return service_list


# scan a port
def scan_port(host, port, open_ports):
	try:
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
			sock.settimeout(1)
			result = sock.connect_ex((host, port))
			if result == 0:
				open_ports.append(port)
	except socket.error as error:
		pass


# scan ports
def scan_ports(host, ports, thread_list):
	open_ports = []

	for port in tqdm(ports, leave=False):
		thread = threading.Thread(target=scan_port, args=(host, port, open_ports))
		thread_list.append(thread)
		thread.start()

	return open_ports


# display
def display_result(host, target_ports, open_ports):
	print(f"\n[INFO] @{host} {len(open_ports)}/{len(target_ports)} were found open")
	if len(open_ports) > 0:
		open_ports = service_name(open_ports)
		print(f"\t{'PORT':<10}SERVICE")
		for port in open_ports:
			print(f"\t{port[0]:<10}{port[1]}")

# terminate scan
def kill_threads(thread_list):
	print(f"\n[INFO] terminating process")
	for t in thread_list:
		t.join()
	print("[INFO] threads terminated")


# scan multiple host
def scan_multiple(hosts, ports):
	thread_list = []
	for host in hosts:
		open_ports = scan_ports(host, ports, thread_list)
		display_result(host, ports, open_ports)
	return thread_list

# main
def main():
	try:
		parser = argparse.ArgumentParser()
		parser.add_argument("target", type=str, help="target host")
		parser.add_argument("-p", "--port", default="1-1000", help="target port: range or comma-separated")

		args = parser.parse_args()
		target_hosts = args.target.split(",")
		target_ports = args.port
		port_list = port_parser(args.port)

		print(f"\n[INFO] netscan started")
		print(f"\t{'PORT':<15}HOST")

		for host in target_hosts:
			print(f"\t{target_ports:<15}{host}")

		processes = scan_multiple(target_hosts, port_list)
		kill_threads(processes)

	except KeyboardInterrupt:
		print(f"[STOPPED] keyboard interrupt")


if __name__ == "__main__":
	main()
