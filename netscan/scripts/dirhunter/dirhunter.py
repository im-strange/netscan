
try:
	from datetime import datetime
	from tqdm import tqdm
	import configparser
	import threading
	import argparse
	import requests
	import time
	import sys
	import os

except ModuleNotFoundError as e:
	print(f"[main] {e}")
	exit(2)

# colors
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
GRAY = '\033[90m'
RESET = '\033[0m'

# get the absolute path for a file
def path(file):
	return os.path.join(os.path.dirname(os.path.abspath(__file__)), file)

# get current time
def get_time():
	current_time = datetime.now().strftime('%m-%d-%Y %I:%M:%S%p')
	return current_time

class DirHunter:
	def __init__(self, config_file, url, wordlist=None):
		self.name = "main"
		self.url = url
		self.lock = threading.Lock()
		self.results_lock = threading.Lock()

		# open config file
		self.config = configparser.ConfigParser()
		self.config.read(path(config_file))

		# load configuration settings
		self.wordlist = path(self.config.get("files", "wordlist_path")) if not wordlist else wordlist
		self.connection_timeout = int(self.config.get("settings", "connection_timeout"))
		self.read_timeout = int(self.config.get("settings", "read_timeout"))
		self.thread_count = int(self.config.get("settings", "thread_count"))
		self.verbose = self.config.getboolean("settings", "verbose")
		self.output_file = self.config.get("settings", "output_file")
		self.timeout = (self.connection_timeout, self.read_timeout)
		self.status_codes = [int(code.strip()) for code in self.config.get("settings", "status_codes").split(',')]
		self.sleep_time = float(self.config.get("settings", "sleep_time"))
		self.counter = 0

	# display settings
	def display_settings(self):
		print(f"\n{GRAY}[{YELLOW}{get_time()}{GRAY}]{RESET} scan started")
		print(f"{' '*2}[+] status_codes : {','.join(str(num) for num in self.status_codes)}")
		print(f"{' '*2}[+] target_url   : {self.url}")
		print(f"{' '*2}[+] wordlist     : {self.wordlist}")
		print(f"{' '*2}[+] verbose      : {self.verbose}")
		print(f"{' '*2}[+] thread       : {self.thread_count}")
		print(f"{' '*2}[+] output       : {self.output_file}")
		print(f"{' '*2}[+] sleep_time   : {self.sleep_time}")
		print()

	# thread worker
	def thread_worker(self, payloads, results):
		for payload in payloads:
			self.make_request(payload, results)

			with self.lock:
				self.counter += 1

			#  wait before sending another request
			time.sleep(self.sleep_time)

	# main scan function
	def scan(self):
		# check if wordlist exists
		if not os.path.exists(self.wordlist):
			print(f"[{self.name}] wordlist file not found: {self.wordlist}")
			exit(2)

		# read
		with open(self.wordlist) as file:
			wordlist = file.read().splitlines()

		# results
		results = []
		threads = []

		total_lines = len(wordlist)
		chunk_size = len(wordlist) // self.thread_count

		# call make_request() function for each word
		for i in range(self.thread_count):
			start = i * chunk_size
			end = None if i == (self.thread_count - 1) else (i + 1) * chunk_size
			payload_range = wordlist[start:end]

			thread = threading.Thread(target=self.thread_worker, args=(payload_range, results))
			thread.daemon = True
			threads.append(thread)
			thread.start()

		while any(thread.is_alive() for thread in threads):
			with self.lock:
				progress = round((self.counter / total_lines) * 100, 2)
				print(f"\r\033[K{GRAY}[{YELLOW}{self.counter}/{len(wordlist)}{GRAY}]{RESET} scanning {progress}%", end="\r")

		print(f"\r\033[K{GRAY}[{YELLOW}{get_time()}{GRAY}]{RESET} Finished")

		# join threads
		for thread in threads:
			thread.join()

		# save results
		self.save_results(results)


	# request with the custom url
	def make_request(self, payload, results):
		url = f"{self.url}{payload}" if self.url.endswith("/") else f"{self.url}/{payload}"
		try:
			response = requests.get(url, timeout=self.timeout)

			if response.status_code in self.status_codes:
				with self.results_lock:
					results.append((get_time(), url, response.status_code))
				print(f"\r\r\r\r\r{GRAY}[{GREEN}{response.status_code}{GRAY}] {BLUE}{url}{RESET}")

		except requests.exceptions.Timeout:
			if self.verbose:
				print(f"\r\r\r\r\r[{self.name}] request timed out for: {url}")

		except requests.exceptions.RequestException as e:
			if self.verbose:
				print(f"\r\r\r\r\r[{self.name}] trying {url} - host is down")


	# save results to a file
	def save_results(self, results):
		if len(results) >= 1:
			with open(self.output_file, "a") as file:
				for time, url, status in results:
					file.write(f"[{time}] {url} - {status}\n")
			print()
			print(f"\r\033[K[{self.name}] results saved to {self.output_file}")
		else:
			print()
			print(f"\r\033[K[{self.name}] no directories from 'dir_list/list1.txt' were found on the target site")


# typewrite animation
def type(words, speed=0.005):
	for letter in words:
		print(letter, end="", flush=True)
		time.sleep(speed)
	print()


