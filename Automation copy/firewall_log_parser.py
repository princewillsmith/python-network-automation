"""
Firewall Log Parser

Reads firewall_logs.csv and displays:

- Total log entries
- Allowed and denied traffic
- Most common applications
- Top denied source IP addresses
- Traffic by source zone
- Total allowed bytes

This script uses only Python's standard library.
"""

import csv
from collections import Counter
from pathlib import Path


LOG_FILE = Path(__file__).parent / "firewall_logs.csv"


def read_firewall_logs(file_path: Path) -> list[dict[str, str]]:
    """Read firewall log entries from a CSV file."""

    if not file_path.exists():
        print(f"Error: {file_path.name} was not found.")
        return []

    try:
        with file_path.open("r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)

            required_columns = {
                "timestamp",
                "source_ip",
                "destination_ip",
                "application",
                "source_zone",
                "destination_zone",
                "action",
                "bytes",
            }

            available_columns = set(reader.fieldnames or [])

            if not required_columns.issubset(available_columns):
                missing = required_columns - available_columns
                print(f"Error: Missing CSV columns: {', '.join(sorted(missing))}")
                return []

            return list(reader)

    except OSError as error:
        print(f"Error reading the file: {error}")
        return []


def analyze_logs(logs: list[dict[str, str]]) -> None:
    """Analyze firewall logs and print a summary."""

    if not logs:
        print("No firewall logs were found.")
        return

    action_counts = Counter()
    application_counts = Counter()
    denied_sources = Counter()
    source_zone_counts = Counter()

    total_allowed_bytes = 0

    for log in logs:
        action = log["action"].strip().lower()
        application = log["application"].strip().lower()
        source_ip = log["source_ip"].strip()
        source_zone = log["source_zone"].strip().lower()

        action_counts[action] += 1
        application_counts[application] += 1
        source_zone_counts[source_zone] += 1

        if action == "deny":
            denied_sources[source_ip] += 1

        if action == "allow":
            try:
                total_allowed_bytes += int(log["bytes"])
            except ValueError:
                print(
                    f"Warning: Invalid byte value in entry from {source_ip}"
                )

    print("\nFIREWALL LOG ANALYSIS")
    print("=" * 40)

    print(f"Total log entries: {len(logs)}")
    print(f"Allowed traffic:   {action_counts.get('allow', 0)}")
    print(f"Denied traffic:    {action_counts.get('deny', 0)}")
    print(f"Allowed bytes:     {total_allowed_bytes}")

    print("\nMost common applications")
    print("-" * 40)

    for application, count in application_counts.most_common():
        print(f"{application:<20} {count}")

    print("\nTraffic by source zone")
    print("-" * 40)

    for zone, count in source_zone_counts.most_common():
        print(f"{zone:<20} {count}")

    print("\nTop denied source IP addresses")
    print("-" * 40)

    if denied_sources:
        for source_ip, count in denied_sources.most_common(5):
            print(f"{source_ip:<20} {count}")
    else:
        print("No denied traffic found.")


def main() -> None:
    logs = read_firewall_logs(LOG_FILE)
    analyze_logs(logs)


if __name__ == "__main__":
    main()
