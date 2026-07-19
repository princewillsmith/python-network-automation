"""
Connect to a network device through SSH and run a show command.

Use only with devices you own or are authorized to manage.
"""


from getpass import getpass

from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoAuthenticationException
from netmiko.exceptions import NetmikoTimeoutException


def main() -> None:
    host = input("Device IP address: ")
    username = input("Username: ")
    password = getpass("Password: ")

    device = {
        "device_type": "cisco_ios",
        "host": host,
        "username": username,
        "password": password,
    }

    try:
        connection = ConnectHandler(**device)

        output = connection.send_command("show ip interface brief")
        print("\nCommand output:\n")
        print(output)

        connection.disconnect()

    except NetmikoAuthenticationException:
        print("Authentication failed. Check the username and password.")

    except NetmikoTimeoutException:
        print("Connection timed out. Check reachability and SSH access.")

    except Exception as error:
        print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()
