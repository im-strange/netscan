<h1 align="center"> NetScan </h1>

 <p align="center">
 <img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge">
 <img src="https://img.shields.io/badge/Netscan-1.2.0-red?style=for-the-badge">
 <img src="https://img.shields.io/badge/Python-3.11.1-blue?style=for-the-badge">
</p>

## Features
- **Server Scanning**: Efficiently scan servers for open ports and vulnerabilities.
- **Organized Result Printing**: Display scanning results in a clear and structured format.
- **Custom Port Scanning**: Specify custom ports to scan based on your needs.
- **Multiple Host Support**: Scan multiple hosts simultaneously for faster results.
- **Progress Bar**: Visualize the scanning progress with a built-in progress bar for better tracking.


## Installation
```
pip install git+https://github.com/im-strange/netscan.git
```

## Usage
```
usage: netscan <host> [options]

positional arguments:
  target          target host/s
  -p, --port      target port/s [default=1-1000]

optional arguments:
  -v, --verbose   print scanning info
  -o, --output    output file to write

examples:
  netscan 127.0.0.1 -p 22,80,443
  netscan example.com -o myresults.txt
```

## Example output
```python
$ netscan www.google.com -p 1-10000

[info] netscan started
    TARGET    localhost
    PORT      1-1000
    VERBOSE   False

[info] @localhost 2/1000 were found open:
    PORT      SERVICE
    135       DCE endpoint resolution
    445       Microsoft-DS

[info] netscan finished in 0.4s

```
<br>

> The content of this repository is provided strictly for educational and ethical purposes. Any misuse of the tools or information provided for illegal activities is not supported or endorsed by the author. Use this content responsibly and only in compliance with all applicable laws and regulations.
