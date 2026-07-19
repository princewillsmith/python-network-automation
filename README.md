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
│   ├── backup_configs.py
│   ├── devices.txt
│   ├── firewall_log_parser.py
│   ├── firewall_logs.csv
│   ├── requirements.txt
│   └── ssh_connect.py
├── Basics/
├── Network_Tools/
│   ├── ping_multiple_hosts.py
│   └── subnet_calculator.py
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

## Disclaimer

Use these scripts only on systems and network devices that you own or are authorized to manage.
