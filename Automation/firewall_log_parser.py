"""
Analyze a CSV firewall log and summarize allowed and denied traffic.

Expected CSV columns:

source_ip,destination_ip,application,action
"""


import csv
from collections import Counter
from pathlib import Path


LOG_FILE = Path("firewall_logs.csv")


def analyze_logs(filename: Path) -> None:
    """Read firewall logs and print a traffic summary."""

    if not filename.exists():
        print(f"{filename} was not found.")
        return

    action_counter: Counter[str] = Counter()
    application_counter: Counter[str] = Counter()
    denied_sources: Counter[str] = Counter()

    total_logs = 0

    try:
        with filename.open("r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)

            required_columns = {
                "source_ip",
                "destination_ip",
                "application",
                "action",
            }

            if not required_columns.issubset(reader.fieldnames or []):
                print("The CSV file is missing one or more required columns.")
                return

            for row in reader:
                total_logs += 1

                action = row["action"].strip().lower()
                application = row["application"].strip().lower()
                source_ip = row["source_ip"].strip()

                action_counter[action] += 1
                application_counter[application] += 1

                if action == "deny":
                    denied_sources[source_ip] += 1

    except OSError as error:
        print(f"Unable to read the log file: {error}")
        return

    print("\nFirewall log summary")
    print(f"Total records: {total_logs}")

    print("\nActions:")
    for action, count in action_counter.most_common():
        print(f"{action}: {count}")

    print("\nTop applications:")
    for application, count in application_counter.most_common(5):
        print(f"{application}: {count}")

    print("\nTop denied source addresses:")
    if denied_sources:
        for source_ip, count in denied_sources.most_common(5):
            print(f"{source_ip}: {count}")
    else:
        print("No denied traffic found.")


if __name__ == "__main__":
    analyze_logs(LOG_FILE)
