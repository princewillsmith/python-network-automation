"""
Check whether TCP ports are open on a host, for example to verify firewall rules after a change.

Use only on systems you own or are authorized to test.
"""

import socket
from concurrent.futures import ThreadPoolExecutor

COMMON_PORTS = {
    22: "ssh",
    53: "dns",
    80: "http",
    443: "https",
    3389: "rdp",
    8080: "http-alt",
}


def check_port(host: str, port: int, timeout: float = 2.0) -> tuple[int, str]:
    """Return (port, status) where status is open, closed, or filtered."""

    try:
        with socket.create_connection((host, port), timeout=timeout):
            return port, "open"
    except ConnectionRefusedError:
        return port, "closed"      # host answered with RST
    except (socket.timeout, TimeoutError):
        return port, "filtered"    # no answer, usually a firewall drop
    except OSError as error:
        return port, f"error ({error.strerror})"


def parse_ports(raw: str) -> list[int]:
    """Parse '22,80,443' or '8000-8010' into a list of ports."""

    if not raw.strip():
        return list(COMMON_PORTS)

    ports: list[int] = []
    for part in raw.split(","):
        if "-" in part:
            start, end = (int(value) for value in part.split("-"))
            ports.extend(range(start, end + 1))
        else:
            ports.append(int(part))

    return ports


def main() -> None:
    host = input("Host: ").strip()
    ports = parse_ports(input("Ports (e.g. 22,443 or 8000-8010, blank = common): "))

    with ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(lambda port: check_port(host, port), ports)

    for port, status in sorted(results):
        print(f"{port:>5}/tcp  {COMMON_PORTS.get(port, ''):<9} {status}")


if __name__ == "__main__":
    main()
