import platform
import subprocess


devices = [
    "8.8.8.8",
    "1.1.1.1",
    "192.168.1.1",
]

def ping_host(host):
    system = platform.system().lower()

    if system == "windows":
        command = ["ping", "-n", "2", "-w", "2000", host]
    else:
        command = ["ping", "-c", "2", "-W", "2", host]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=10,
        )

        return result.returncode == 0

    except FileNotFoundError:
        print("Error: The ping command was not found.")
        return False

    except subprocess.TimeoutExpired:
        print(f"Error: Ping to {host} timed out.")
        return False

    except Exception as error:
        print(f"Error while pinging {host}: {error}")
        return False


def main():
    print("Network reachability check\n")

    for device in devices:
        if ping_host(device):
            print(f"[UP]   {device} is reachable")
        else:
            print(f"[DOWN] {device} is not reachable")


if __name__ == "__main__":
    main()
