
import socket
import sys
import os

def capture_banner(ip, port):
	try:
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
			sock.settimeout(5)
			print(f"[info] connecting to {ip}:{port}", end="\r")
			result = sock.connect((ip, port))

			print(f"[info] connecting to {ip}:{port} -> OK")
			print(f"[info] fetching banner", end="\r")
			banner = sock.recv(1024).decode("utf-8", errors="ignore")

			if banner:
				print(f"\r\r\r\r[info] fetching banner -> OK")
				print(f"[info] banner: {banner}")
			else:
				print(f"[info] no banner received")

	except socket.timeout as e:
		print(f"[info] connection timed out")

	except ConnectionRefusedError as e:
		print(f"[info] connection refused")

	#except Exception as e:
	#	print(f"[info] error: {e}")


if __name__ == "__main__":
	ip = "142.251.220.206"
	port = 80
	banner = capture_banner(ip, port)
