#!/usr/bin/env python3

# built-in modules, does not need pre-checking
from datetime import datetime
import configparser
import threading
import argparse
import socket
import json
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


# check if third-party modules are installed
try:
	from tqdm import tqdm
	import socks

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

# main class
class PortScanner:
	def __init__(self, config_file, target, port):
		self.name = "netscan"
		self.target = target
		self.port = port
		self.config_file = path(config_file)
		self.save_result = False
		self.result = ""

		try:
			self.port_list = self.parse_port(self.port)
		except ValueError:
			print(f"{bracket('info')} invalid --port value: {self.port}")
			exit(2)

		if not os.path.exists(self.config_file):
			print(f"[{self.name}] config file '{self.config_file}' not found")
			exit(2)

		self.config = configparser.ConfigParser()
		self.config.read(path(config_file))

		self.port_services_file = path(self.config.get("files", "port_services"))
		self.output_file = self.config.get("files", "output_file")
		self.timeout = int(self.config.get("settings", "timeout_per_connect"))

		with open(self.port_services_file) as file:
			self.port_services = json.load(file)

	# get the service names of given list of ports
	def get_service_name(self, ports):
		names = []
		for port in ports:
			name = self.port_services.get(str(port))
			if name:
				names.append([port, name])
			else:
				names.append([port, "unknown service"])
		return names

	# turn given port argument into a list of ports
	def parse_port(self, port_str):
		# if range
		if "-" in port_str:
			pattern = port_str.split("-")
			start_port, end_port = int(pattern[0]), int(pattern[1])

			if end_port > 65535:
				print(f"{bracket('info')} port must be 0-65535")
				exit(2)

			port_list = list(range(start_port, end_port+1))
			return port_list

		# if list (comma-separated)
		elif "," in port_str:
			port_list = [int(port) for port in port_str.split(",")]
			if any(port > 65535 for port in port_list):
				print(f"{bracket('info')} port must be 0-65535")
				exit(2)
			return port_list

		# else, must be given a single port
		else:
			if int(port_str) > 65535:
				print(f"{bracket('info')} port must be 0-65535")
				exit(2)
			return [int(port_str)]

	# scan a port
	def scan_port(self, ip, port, open_ports):
		try:
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
				sock.settimeout(self.timeout)
				result = sock.connect((ip, port))
				open_ports.append(port)

		except (socket.timeout, socket.error, ConnectionRefusedError) as e:
			if self.verbose:
				print(f"{bracket('info')} {e} in port {port}")
			else:
				pass

	# multi-thread scanning
	def scan_ports(self, ip, ports):
		open_ports = []
		threads = []
		for port in tqdm(ports, leave=False):
			thread = threading.Thread(target=self.scan_port, args=(ip, port, open_ports))
			thread.daemon = True
			threads.append(thread)
			thread.start()
		for thread in threads:
			thread.join()
		return open_ports

	# display scan results
	def display_results(self, ip, target_ports, open_ports):
		tabsize = 4
		print(f"\n{bracket('info')} {MAGENTA}@{ip}{RESET} {len(open_ports)}/{len(target_ports)} were found open:")
		if len(open_ports) > 0:
			print(f"{' '*tabsize}{BLUE}{'PORT':<10}SERVICE{RESET}")
			port_service_names = self.get_service_name(open_ports)
			for port in port_service_names:
				print(f"{' '*tabsize}{port[0]:<10}{port[1]}")
				time.sleep(0.01)

	# save scan results
	def add_to_results(self, ip, target_ports, open_ports):
		service_names = self.get_service_name(open_ports)
		self.result += f"{' '*2}@{ip} {len(open_ports)}/{len(target_ports)} were found open\n"
		self.result += f"{' '*4}{'PORT':<10}SERVICE\n"
		for open_port in service_names:
			self.result += f"{' '*4}{str(open_port[0]):<10}{str(open_port[1])}\n"


	# save
	def save_results(self):
		with open(self.output_file, "a") as file:
			file.write(self.result)

	# start scan
	def start_scan(self):
		tabsize = 4
		print()
		print(f"{bracket('info')} netscan started")
		print(f"{' '*tabsize}{BLUE}{'TARGET':<10}{RESET}{','.join(self.target)}")
		print(f"{' '*tabsize}{BLUE}{'PORT':<10}{RESET}{self.port}")
		print(f"{' '*tabsize}{BLUE}{'VERBOSE':<10}{RESET}{self.verbose}")

		if self.save_result:
			self.result += f"{'―'*50}\n"
			self.result += f"[{current_time()}] netscan result\n"
			self.result += f"{'―'*50}\n"

		start_time = time.time()
		for target in self.target:
			results = self.scan_ports(target, self.port_list)
			self.display_results(target, self.port_list, results)

			if self.save_result:
				self.result += "\n"
				self.add_to_results(target, self.port_list, results)

		elapsed_time = round(time.time() - start_time, 1)
		print(f"\n{bracket('info')} netscan finished in {elapsed_time}s")

		if self.save_result:
			self.result += f"{'―'*50}\n"
			self.save_results()
			print(f"{bracket('info')} results saved to {BLUE}{self.output_file}{RESET}")

