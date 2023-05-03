
try:
  import threading
  import socket
  import time
  import re
  import sys
  from tqdm import tqdm
  import requests
except ModuleNotFoundError as error:
  print(f"Netscan: {error}")
  exit()

# functions for options
class Options:
  def __init__(self):
    pass

  # attempts to retrieve SSH server
  def detect_ssh(self, host):
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.settimeout(2)
    result = None
    try:
      socket_server.connect((host, 22))
      response = socket_server.recv(250).decode()
      server_running = response.strip()
      return server_running
    except TimeoutError: return "Connection timed out"
    except socket.error as error: return error

  # attempts to retrieve web server
  def detect_webserver(self, host):
    try:
      url = f"http://{host}/"
      response = requests.get(url)
      server = ["OK", response.headers["Server"]]
      return server
    except Exception as error:
      return ["ERR", error]

# print help message
def display_help():
  help_msgs = [
    "usage: netscan [-t TARGET] [--port PORT]\n",
    "Options:",
    f" {'-h, --help':<15} display help",
    f" {'-p, --port':<15} define specific port or range",
    f" {'-t, --target':<15} specify single target host (comma separated if multiple)",
    f" {'--server':<15} attempts to detect web server running",
    f" {'--ssh':<15} attempts to detect ssh server running"
]
  for msg in help_msgs:
    print(msg)

# parsing arguments
def args_parser(list):
  available_args = {
    "port": "1-1000",
    "target": [],
    "detect_ssh": False,
    "detect_webserver": False
  }
  given_args = list
  if "-p" in given_args:
    try: available_args["port"] = given_args[(given_args.index("-p")+1)]
    except IndexError: print("Netscan: Missing value after '-p'"), exit()

  elif "--port" in given_args:
    try: available_args["port"] = given_args[(given_args.index("--port")+1)]
    except IndexError: print("Netscan: Missing value after '--port'"), exit()

  if "-t" in given_args:
    try:
      hosts = given_args[(given_args.index("-t")+1)].split(",")
      available_args["target"] = hosts
    except IndexError: print("Netscan: Missing value after '-t'"), exit()

  elif "--target" in given_args:
    try:
      hosts = given_args[(given_args.index("--target")+1)].split(",")
      available_args["target"] = hosts
    except IndexError: print("Netscan: Missing or invalid value for '--target'"), exit()

  if "--ssh" in given_args: available_args["detect_ssh"] = True
  if "--server" in given_args: available_args["detect_webserver"] = True

  return available_args

# check args
def check_args():
  options_list = [
    "-h", "--help",
    "-p", "--port",
    "-t", "--target",
    "--server", "--ssh"
  ]
  args = sys.argv
  for arg in args:
    if "-" in arg and arg not in options_list and not "-" in args[(args.index(arg)-1)]:
      print(f"Netscan: Invalid option '{arg}'")
      exit()

  if "-h" in args or "--help" in args:
    display_help()
    exit()

  if len(args) < 2:
    print(f"Netscan: Not enough argument")
    display_help()
    exit()

  if "-t" not in args:
    if "--target" in args: pass
    else:
      print("Netscan: Missing target host")
      display_help()
      exit()

# label ports
def label(port):
  try:
    service_name = socket.getservbyport(port)
    return service_name
  except OSError:
    return "unknown"

# timer for reporting elapsed time
class Timer:
  def __init__(self):
    self.start_time = None
    self.stop_time = None
    self.elapsed_time = None

  def start(self):
    self.start_time = time.time()
  def stop(self):
    self.stop_time = time.time()
    self.elapsed_time = self.stop_time - self.start_time
  def get_time(self):
    return round(self.elapsed_time, 2)

# initialize timer
timer = Timer()

# split argument for port range
def port_handler(port_range):
  ports = re.split(",|-", port_range)
  type = ""
  if "-" in port_range: type = "range"
  elif len(port_range) == 1: type = "single"
  else: type = "listed"
  return [type, ports]

# attempts to make connection to test if a port is open
open_ports = []
def check_port(host, port):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.settimeout(1)
  status = sock.connect_ex((host, port))
  if status == 0: open_ports.append([port, "open", label(port)])
  elif status == socket.timeout: open_ports.append([port, "filtered", label(port)])
  elif status == socket.error: open_ports.append([port, "close", label(port)])
  sock.close()

# scan target host
def port_scan(host, port_range):
  host = socket.gethostbyname(host)
  port_info = port_handler(port_range)
  scan_type = port_info[0]

  try: ports = [int(port) for port in port_info[1]]
  except ValueError: print("Netscan: Invalid port given"), exit()

  result = []

  # with given range
  if scan_type == "range":
    threads = []
    for port in range(ports[0], ports[1]+1):
      t = threading.Thread(target=check_port, args=(host, port))
      threads.append(t)
    for t in tqdm(threads):
      t.start()
    for t in threads:
      t.join
    return open_ports

  # scan with given list
  else:
    for port in tqdm(ports):
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      sock.settimeout(1)
      status = sock.connect_ex((host, port))
      if status == 0: result.append([port, "open", label(port)])
      elif status == socket.timeout: result.append([port, "filtered", label(port)])
      else: result.append([port, "close", label(port)])
    sock.close()
    return result

# run the function and display the results
def main(host, ports, detect_ssh, detect_webserver):
  global open_ports
  options = Options()
  try:
    host_ip = socket.gethostbyname(host)
  except socket.gaierror as e:
    print(f"Netscan: {e}")
    exit()

  print(f"\r\r\rScanning ports for {host} {host_ip}")
  timer.start()
  open_ports = []
  result_list = port_scan(host, ports)

  print(f"\nScan report for {host}")
  print(f" {'Port':<15}{'Status':<15}Service")

  for r in result_list:
    print(f" {r[0]:<15}{r[1]:<15}{r[2]:<15}")

  if detect_webserver:
    print(f"\nScan report for server detection")
    webserver = options.detect_webserver(host)
    if webserver[0] == "OK":
      print(f" {'Server':<15}{webserver[1]}")
    else:
      print(f" {'Server':<15}{webserver[1]}")

  if detect_ssh:
    print(f"\nScan report for SSH server detection")
    ssh_server = options.detect_ssh(host)
    print(f" {'SSH':<15}{ssh_server}")

  timer.stop()
  elapsed = timer.get_time()
  print(f"\nDone in {elapsed}s")

if __name__ == "__main__":
  check_args()
  arguments = args_parser(sys.argv)
  host = arguments["target"]
  port = arguments["port"]
  detect_ssh = arguments["detect_ssh"]
  detect_webserver = arguments["detect_webserver"]

  for target in host:
    main(target, port, detect_ssh, detect_webserver)
    if target != host[-1]:
      print("")
