"""
Build a CSV inventory (hostname, OS version, model, serial, uptime) from 'show version'.

Offline mode (default) parses sample_data/*show_version*.txt.
Live mode (--live) connects to every device in Automation/devices.txt with Netmiko.
"""

import csv
import re
import sys
from getpass import getpass
from pathlib import Path

PROJECT_DIRECTORY = Path(__file__).parent
SAMPLE_DIRECTORY = PROJECT_DIRECTORY / "sample_data"
DEVICES_FILE = PROJECT_DIRECTORY.parent / "devices.txt"
OUTPUT_FILE = Path("inventory.csv")

PATTERNS = {
    "hostname": r"^(\S+) uptime is",
    "version": r"Version ([\w.()]+)",
    "model": r"^cisco (\S+)",
    "serial": r"Processor board ID (\S+)",
    "uptime": r"uptime is (.+)$",
}


def parse_show_version(output: str) -> dict:
    """Extract inventory fields from Cisco 'show version' output."""

    record = {}
    for field, pattern in PATTERNS.items():
        match = re.search(pattern, output, re.MULTILINE)
        record[field] = match.group(1).strip() if match else "unknown"
    return record


def collect_live() -> list[dict]:
    from netmiko import ConnectHandler

    username = input("Username: ")
    password = getpass("Password: ")
    records = []

    for host in DEVICES_FILE.read_text(encoding="utf-8").split():
        try:
            with ConnectHandler(device_type="cisco_ios", host=host,
                                username=username, password=password) as connection:
                record = parse_show_version(connection.send_command("show version"))
        except Exception as error:
            print(f"{host}: failed ({error})")
            continue
        record["ip"] = host
        records.append(record)

    return records


def main() -> None:
    if "--live" in sys.argv:
        records = collect_live()
    else:
        records = []
        for file in sorted(SAMPLE_DIRECTORY.glob("*show_version*.txt")):
            record = parse_show_version(file.read_text(encoding="utf-8"))
            record["ip"] = "sample"
            records.append(record)

    if not records:
        print("No devices collected.")
        return

    fields = ["hostname", "ip", "model", "version", "serial", "uptime"]
    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(records)

    for record in records:
        print(" | ".join(record[field] for field in fields))
    print(f"\nInventory written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
