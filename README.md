<h1 align="center"> NetScan </h1>
<p align="center">
 <img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge">
 <img src="https://img.shields.io/badge/Netscan-v1.0.0-red?style=for-the-badge"
</p>

## Features
- Server scanning
- Custom port scanning
- Multiple host
- Web and SSH server detection
- Progress bar

## Installation
```
pip install git+https://github.com/im-strange/netscan.git
```
<br>

## Usage
```
~ $ netscan --help
usage: netscan [OPTIONS] [-t TARGET] [--port PORT]

Options:
 -h, --help      display help
 -p, --port      define specific port or range
 -t, --target    specify single target host (comma separated if multiple)
 --version       print netscan version
 --info          display available details about netscan
 --server        attempts to detect web server running
 --ssh           attempts to detect ssh server running

Note: Always check for updates.
```
<br>

> Use this repository's content only for legal and ethical purposes.
I do not support any illegal actions.
