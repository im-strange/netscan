
import subprocess
import time

def uninstall_package(package_name):
	try:
		command = f"pip uninstall -y {package_name}".split()
		result = subprocess.run(
			command,
			check=True,
			capture_output=True,
			text=True
		)
		return True
	except subprocess.CalledProcessError as e:
		print(f"[info] error: {e}")

def install_package(url):
	try:
		command = f"pip install git+{url}".split()
		result = subprocess.run(
			command,
			check=True,
			capture_output=True,
			text=True
		)
		return True
	except subprocess.CalledProcessError as e:
		print(f"[info] error: {e}")

def reinstall_package():
	try:
		package_name = "netscan"
		url = "https://github.com/im-strange/netscan"

		print(f"[info] uninstalling the package", end="\r")
		if uninstall_package(package_name):
			print(f"\r\r\r\r[info] uninstalling the package -> OK")
			time.sleep(0.5)

		print(f"[info] reinstalling the package", end="\r")
		if install_package(url):
			print(f"\r\r\r\r[info] reinstalling the package -> OK")
			time.sleep(0.5)

		print(f"[info] package successfully reinstalled!")

	except Exception as e:
		print(f"[info] error: {e}")

if __name__ == "__main__":
	reinstall_package()
