"""
Audit Cisco IOS running configurations against a security baseline.

Works offline on saved configs (sample_data/*_running_config.txt), so it can run in
a pipeline after backup_configs.py has collected the configurations.
"""

import re
import sys
from pathlib import Path

SAMPLE_DIRECTORY = Path(__file__).parent / "sample_data"

# (description, pattern, must_exist)
RULES = [
    ("SSH version 2 enabled", r"^ip ssh version 2", True),
    ("Password encryption enabled", r"^service password-encryption", True),
    ("Remote logging configured", r"^logging host \S+", True),
    ("NTP configured", r"^ntp server \S+", True),
    ("No plain-text enable password", r"^enable password ", False),
    ("No Telnet on VTY lines", r"^ transport input .*telnet", False),
    ("HTTP server disabled", r"^ip http server", False),
    ("No default SNMP communities", r"^snmp-server community (public|private)\b", False),
]


def audit(config: str) -> list[tuple[str, bool]]:
    """Return (rule description, passed) for each baseline rule."""

    results = []
    for description, pattern, must_exist in RULES:
        found = re.search(pattern, config, re.MULTILINE) is not None
        results.append((description, found == must_exist))
    return results


def main() -> None:
    directory = Path(sys.argv[1]) if len(sys.argv) > 1 else SAMPLE_DIRECTORY
    configs = sorted(directory.glob("*running_config*.txt"))

    if not configs:
        print(f"No configuration files found in {directory}")
        return

    for config_file in configs:
        results = audit(config_file.read_text(encoding="utf-8"))
        passed = sum(ok for _, ok in results)

        print(f"\n{config_file.name}: {passed}/{len(results)} checks passed")
        for description, ok in results:
            print(f"  [{'PASS' if ok else 'FAIL'}] {description}")


if __name__ == "__main__":
    main()
