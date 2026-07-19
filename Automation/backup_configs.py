"""
Back up running configurations from authorized Cisco IOS devices.

Device information is read from devices.txt.
"""

from datetime import datetime
from getpass import getpass
from pathlib import Path

from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoAuthenticationException
from netmiko.exceptions import NetmikoTimeoutException


BACKUP_DIRECTORY = Path("backups")


def load_devices(filename: str) -> list[str]:
    """Read device IP addresses from a text file."""

    path = Path(filename)

    if not path.exists():
        print(f"{filename} was not found.")
        return []

    return [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def back_up_device(host: str, username: str, password: str) -> None:
    """Connect to one device and save its running configuration."""

    device = {
        "device_type": "cisco_ios",
        "host": host,
        "username": username,
        "password": password,
    }

    try:
        print(f"Connecting to {host}...")

        connection = ConnectHandler(**device)
        hostname = connection.find_prompt().replace("#", "").replace(">", "").strip()

        configuration = connection.send_command("show running-config")
        connection.disconnect()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = BACKUP_DIRECTORY / f"{hostname}_{timestamp}.txt"

        filename.write_text(configuration, encoding="utf-8")
        print(f"Backup saved: {filename}")

    except NetmikoAuthenticationException:
        print(f"Authentication failed for {host}")

    except NetmikoTimeoutException:
        print(f"Connection timed out for {host}")

    except Exception as error:
        print(f"Backup failed for {host}: {error}")


def main() -> None:
    devices = load_devices("devices.txt")

    if not devices:
        return

    BACKUP_DIRECTORY.mkdir(exist_ok=True)

    username = input("Username: ")
    password = getpass("Password: ")

    for host in devices:
        back_up_device(host, username, password)


if __name__ == "__main__":
    main()
