"""
Find interfaces that are down from 'show ip interface brief' output.

Offline mode (default) parses sample_data/*show_ip_int_brief*.txt.
Live mode (--live <host>) collects the output from an authorized device with Netmiko.
"""

import sys
from getpass import getpass
from pathlib import Path

SAMPLE_DIRECTORY = Path(__file__).parent / "sample_data"


def parse_ip_int_brief(output: str) -> list[dict]:
    """Parse Cisco 'show ip interface brief' into a list of dictionaries."""

    interfaces = []
    for line in output.splitlines()[1:]:
        parts = line.split()
        if len(parts) < 6:
            continue

        # Status can be two words: "administratively down"
        interfaces.append({
            "interface": parts[0],
            "ip": parts[1],
            "status": " ".join(parts[4:-1]),
            "protocol": parts[-1],
        })
    return interfaces


def report(device: str, interfaces: list[dict]) -> None:
    print(f"\n{device}")
    for entry in interfaces:
        if entry["status"] == "administratively down":
            state = "SHUTDOWN"
        elif entry["status"] == "up" and entry["protocol"] == "up":
            state = "OK"
        else:
            state = "ALERT"   # up/down usually means a cabling, speed/duplex, or keepalive issue
        print(f"  [{state:<8}] {entry['interface']:<22} {entry['ip']:<15} {entry['status']}/{entry['protocol']}")


def collect_live(host: str) -> str:
    from netmiko import ConnectHandler

    device = {
        "device_type": "cisco_ios",
        "host": host,
        "username": input("Username: "),
        "password": getpass("Password: "),
    }
    with ConnectHandler(**device) as connection:
        return connection.send_command("show ip interface brief")


def main() -> None:
    if len(sys.argv) == 3 and sys.argv[1] == "--live":
        report(sys.argv[2], parse_ip_int_brief(collect_live(sys.argv[2])))
        return

    for file in sorted(SAMPLE_DIRECTORY.glob("*show_ip_int_brief*.txt")):
        report(file.name.split("_")[0].upper(), parse_ip_int_brief(file.read_text(encoding="utf-8")))


if __name__ == "__main__":
    main()
