# Python Network Automation

This repository contains Python scripts for networking, troubleshooting, and basic network automation.

The projects demonstrate practical tasks such as:

- Checking device reachability
- Calculating IPv4 subnets
- Connecting to network devices with SSH
- Backing up device configurations
- Analyzing firewall logs

## Repository Structure

```text
python-network-automation/
├── Automation/
│   ├── backup_configs.py          # back up running configs from devices.txt (Netmiko)
│   ├── firewall_log_parser.py     # analyse firewall traffic logs (CSV)
│   ├── ssh_connect.py             # run a show command over SSH
│   ├── devices.txt
│   ├── firewall_logs.csv
│   ├── requirements.txt
│   └── Projects/
│       ├── config_compliance.py   # audit IOS configs against a security baseline
│       ├── interface_monitor.py   # flag down/err interfaces from show ip int brief
│       ├── network_inventory.py   # build a CSV inventory from show version
│       └── sample_data/           # sample outputs so every project runs offline
├── Basics/                        # variables, lists, dictionaries, loops, functions
├── Network_Tools/
│   ├── dns_lookup.py              # forward and reverse DNS lookups
│   ├── ip_validator.py            # validate and classify IPv4/IPv6 addresses
│   ├── ping_multiple_hosts.py     # reachability check for many hosts
│   ├── port_checker.py            # TCP port check: open / closed / filtered
│   └── subnet_calculator.py       # IPv4 subnet details
├── LICENSE
└── README.md
```

## Requirements

- Python 3
- Netmiko

Install the required package:

```bash
python3 -m pip install -r Automation/requirements.txt
```

## How to Run the Scripts

Run all commands from the main repository folder.

### Ping Multiple Hosts

Checks whether multiple IP addresses are reachable.

```bash
python3 Network_Tools/ping_multiple_hosts.py
```

### Subnet Calculator

Calculates subnet details such as:

- Network address
- Broadcast address
- Subnet mask
- Prefix length
- Total addresses
- Usable hosts

Run:

```bash
python3 Network_Tools/subnet_calculator.py
```

Example input:

```text
192.168.10.0/24
```

### IP Validator

Validates IPv4/IPv6 addresses and classifies them as private, public, loopback, multicast, or link-local.

```bash
python3 Network_Tools/ip_validator.py
```

### DNS Lookup

Forward (name → IPs) and reverse (IP → PTR) lookups.

```bash
python3 Network_Tools/dns_lookup.py
```

### Port Checker

Checks TCP ports concurrently and reports **open** (handshake completed), **closed** (RST received) or **filtered** (no reply, usually a firewall drop). Useful for verifying firewall rule changes.

```bash
python3 Network_Tools/port_checker.py
```

### Configuration Compliance Audit

Audits saved Cisco IOS configurations against a security baseline: SSH v2, password encryption, remote logging, NTP, no Telnet, no HTTP server, no default SNMP communities, no plain-text enable password.

```bash
python3 Automation/Projects/config_compliance.py                 # sample configs
python3 Automation/Projects/config_compliance.py backups/        # your backups
```

Example output:

```text
sw2_running_config.txt: 0/8 checks passed
  [FAIL] SSH version 2 enabled
  [FAIL] No Telnet on VTY lines
  ...
```

### Interface Monitor

Parses `show ip interface brief` and flags interfaces as OK, ALERT (up/down) or SHUTDOWN.

```bash
python3 Automation/Projects/interface_monitor.py                 # sample data
python3 Automation/Projects/interface_monitor.py --live 10.0.0.1 # live device
```

### Network Inventory

Collects hostname, model, OS version, serial number and uptime from `show version` into `inventory.csv`.

```bash
python3 Automation/Projects/network_inventory.py          # sample data
python3 Automation/Projects/network_inventory.py --live   # devices in Automation/devices.txt
```

### Firewall Log Parser

Reads sample firewall logs from a CSV file and displays:

- Total log entries
- Allowed traffic
- Denied traffic
- Most common applications
- Traffic by source zone
- Top denied source IP addresses

Run:

```bash
python3 Automation/firewall_log_parser.py
```

### SSH Connection

Connects to an authorized network device through SSH and runs a show command.

Run:

```bash
python3 Automation/ssh_connect.py
```

This script requires:

- A reachable network device
- SSH enabled on the device
- Valid credentials
- The correct Netmiko device type

### Configuration Backup

Connects to multiple authorized devices and saves their running configurations.

The device addresses are read from:

```text
Automation/devices.txt
```

Run:

```bash
python3 Automation/backup_configs.py
```

## Sample Data

The repository uses sample IP addresses and sample firewall logs.

Do not upload:

- Real customer IP addresses
- Production configurations
- Passwords
- Private keys
- Confidential firewall exports

## Skills Demonstrated

- Python functions and loops
- File handling
- CSV parsing
- Error handling
- IP addressing
- Network troubleshooting
- SSH automation
- Configuration backups
- Firewall log analysis
- Security compliance auditing
- Parsing CLI output with regular expressions
- Concurrent network checks (ThreadPoolExecutor)

## Disclaimer

Use these scripts only on systems and network devices that you own or are authorized to manage.
