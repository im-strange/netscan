# Port Scanner
The `netscan port` subcommand is designed to scan specified ports on a target host or network. This functionality helps users identify open ports and associated services, which is crucial for network security assessments and troubleshooting.

## Usage
To use the `netscan port` command, you need to specify the target and the ports you wish to scan. You can view the detailed informations with `netscan port --manual` command.

```
usage: netscan port [target] [options]

positional arguments:
  -t, --target   specify the target host(s), comma-separated
                 if multiple
  -p, --port     Specify the port(s) to scan. Can be a single
                 port, a range, or comma-separated list of
                 ports [default=1-1000]

optional arguments:
  --manual       print this help manual and exit
  -v, --verbose  enable detailed output during the scan
  -o, --output   save the scan results to a specified file
```
