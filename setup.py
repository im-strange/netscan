from setuptools import setup

setup(
  name="netscan",
  version="1.0",
  author="Sam Genoguin",
  description="A Python tool for network scanning.",
  url="https://github.com/im-strange/netscan.git",
  install_requires= [
    "threading",
    "socket",
    "time",
    "re",
    "sys",
    "tqdm",
    "requests"
  ]
  py_modules=["netscan"],
  entry_points={
    "console_scripts": [
      "netscan = netscan:main"
    ]
  }
)
