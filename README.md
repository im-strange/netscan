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

## Example output
```Usage
usage: netscan [commands] [options]

commands:
  port        scan for open ports on a host
  vuln        scan for known vulnerabilities on a host and
              generate report
  ping        ping a host to check its availability
  reinstall   uninstall and reinstall the package. Useful
              for fixing issues

see '[command] --manual' for more info
```

## Command Documentation
- [Port scanner](netscan/scripts/port_scanner/README.md)

## Found a bug?
Shoot me an email at **im.strange.git@gmail.com**

<br>

> The content of this repository is provided strictly for educational and ethical purposes. Any misuse of the tools or information provided for illegal activities is not supported or endorsed by the author. Use this content responsibly and only in compliance with all applicable laws and regulations.
