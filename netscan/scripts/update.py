import subprocess
import sys

# get the latest commit from github
def get_latest_commit():
	try:
		git_repo = "https://github.com/im-strange/netscan.git"
		command = f"git ls-remote {git_repo} HEAD".split(' ')
		result = subprocess.run(
			command,
			check=True,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE
		)
		latest_commit = result.stdout.decode().split()[0]
		return latest_commit

	except subprocess.CalledProcessError as e:
		print(f"[netscan] error fetching latest commit: {e}")


# get the version of installed repo
def get_local_commit():
	try:
		pass
	except FileNotFoundError as e:
		pass

if __name__ == "__main__":
	latest_commit = get_latest_commit()
	print(latest_commit)
