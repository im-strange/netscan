from setuptools import setup

setup(
  name="netscan",
  version="1.0",
  py_modules=["netscan"],
  entry_points={
    "console_scripts": [
      "netscan = netscan:main"
    ]
  }
)
