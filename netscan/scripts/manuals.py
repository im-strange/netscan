import textwrap
import shutil
import time

def parse_manual(lines, tabsize=2, max_width=45, mid_indent=15):
	terminal_width = shutil.get_terminal_size().columns
	max_width = terminal_width - 20 if terminal_width <= 70 else max_width
	parsed = []
	for line in lines:
		if len(line) == 2:
			arg, desc = line
			wrapped_desc = f"\n{' '*(tabsize+mid_indent)}".join(textwrap.wrap(desc, width=max_width))
			#wrapped_desc = textwrap.fill(desc, width=max_width, subsequent_indent=' '*(tabsize+mid_indent))
			parsed.append(f"{' '*tabsize}{arg:<{mid_indent}}{wrapped_desc}")
		else:
			parsed.append(line)
	return parsed

class Manual:
	def __init__(self):
		self.tabsize = 2
		self.max_width = 45

	def port_scanner(self):
		lines = [
			"usage: netscan port -t [target] [options]",
			"\npositional arguments:",
			("-t, --target", "specify the target host(s), comma-separated if multiple"),
			("-p, --port", "Specify the port(s) to scan. Can be a single port, a range, or comma-separated list of ports [default=1-1000]"),
		    "\noptional arguments:",
			("--manual", "print this help manual and exit"),
			("-v, --verbose", "enable detailed output during the scan"),
			("-o, --output", "save the scan results to a specified file")
		]
		for line in parse_manual(lines):
			print(line)
			time.sleep(0.01)

	def dirhunter(self):
		lines = [
			"usage: netscan dirhunter -u [url] [options]",
			"\npositional arguments:",
			("-u, --url", "target URL"),
			("-w, --wordlist", "wordlist file path"),
			"\noptional arguments:",
			("-s, --status", "target status code(s)"),
			("-t, --threads", "number of threads [default=5]"),
			("-o, --output", "output file"),
			("--sleep", "delay between requests (in seconds) [default=0.2]"),
			("--manual", "print this help manual and exit"),
			"\nexamples:",
			f"{' '*self.tabsize}netscan dirhunter -u https://example.com",
			f"{' '*self.tabsize}netscan dirhunter -u https://example.com -t 1 -s 200,201,202,203",
			f"{' '*self.tabsize}netscan dirhunter -u https://example.com -o output.txt"
		]
		for line in parse_manual(lines):
			print(line)
			time.sleep(0.01)

if __name__ == "__main__":
	manual = Manual()
	manual.port_scanner()
	manual.dirhunter()
