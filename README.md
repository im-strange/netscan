<h1 align="center"> NetScan </h1>

 <p align="center">
 <img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge">
 <img src="https://img.shields.io/badge/Netscan-1.1.0-red?style=for-the-badge">
 <img src="https://img.shields.io/badge/Python-3.11.1-blue?style=for-the-badge">
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

## Usage
```
usage: netscan <target_host> [OPTIONS]

options:
    -h, --help      show this help message and exit
    -v, --version   show this cli version
    -p, --port      single, range, or comma-separated
```

## Example output
```python
$ netscan www.google.com -p 1-10000

[INFO] netscan started
        HOST      ['www.google.com']
        PORT      1-10000

[INFO] @www.google.com 2/10000 were found open
        PORT      SERVICE
        80        Hypertext Transfer Protocol (HT..
        443       Hypertext Transfer Protocol ove..

```
<br>

> Use this repository's content only for legal and ethical purposes. I do not support any illegal actions.
