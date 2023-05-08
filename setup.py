from setuptools import setup

setup(
  name="netscan",
  version="1.0.0",
  author="Sam Genoguin",
  description="A Python tool for network scanning.",
  url="https://github.com/im-strange/netscan.git",
  py_modules=["netscan"],
  install_requires=[
    "tqdm",
    "requests"
  ],
  entry_points={
    "console_scripts": [
      "netscan = netscan:main"
    ]
  }
)
