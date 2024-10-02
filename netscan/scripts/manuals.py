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
			wrapped_desc = textwrap.fill(desc, width=max_width, subsequent_indent=' '*(tabsize+mid_indent))
			parsed.append(f"{' '*tabsize}{arg:<{mid_indent}}{wrapped_desc}")
		else:
			parsed.append(line)
	return parsed

class Manual:
	def port_scanner(self):
		tabsize = 2
		max_width = 45

		lines = [
			"usage: netscan port [target] [options]",
			"\npositional arguments:",
			("-t, --target", "specify the target host(s), comma-separated if multiple"),
			("-p, --port", "Specify the port(s) to scan. Can be a single port, a range, or comma-separated list of ports [default=1-1000]"),
		    "\noptional arguments:",
			("--manual", "print this help manual and exit"),
			("-v, --verbose", "enable detailed output during the scan"),
			("-o, --output", "save the scan results to a specified file")
		]

		parsed = parse_manual(lines)

		for line in parsed:
			print(line)
			time.sleep(0.01)

if __name__ == "__main__":
	manual = Manual()
	manual.port_scanner()
