import time

class Manual:
	def port_scanner(self):
		tabsize = 2
		lines = [
			f"usage: netscan port [target] [options]",
			f"\npositional arguments:",
			f"{' '*tabsize}{'-t, --target':<15} target host/s",
			f"{' '*tabsize}{'-p, --port':<15} target port/s [default=1-1000]",
			f"\noptional arguments:",
			f"{' '*tabsize}{'--manual':<15} print this manual and exit",
			f"{' '*tabsize}{'-v, --verbose':<15} print info",
			f"{' '*tabsize}{'-o, --output':<15} save results into a file"
		]

		for line in lines:
			print(line)
			time.sleep(0.01)

if __name__ == "__main__":
	manual = Manual()
	manual.port_scanner()
