"""
Resolve hostnames to IP addresses (forward) and IP addresses to names (reverse).

Uses only the Python standard library, so it relies on the system resolver.
"""

import ipaddress
import socket


def forward_lookup(hostname: str) -> list[str]:
    """Return the unique IPv4/IPv6 addresses for a hostname."""

    results = socket.getaddrinfo(hostname, None)
    return sorted({result[4][0] for result in results})


def reverse_lookup(address: str) -> str:
    """Return the PTR name for an IP address."""

    return socket.gethostbyaddr(address)[0]


def lookup(query: str) -> None:
    query = query.strip()

    try:
        ipaddress.ip_address(query)
        is_ip = True
    except ValueError:
        is_ip = False

    try:
        if is_ip:
            print(f"{query} -> {reverse_lookup(query)}")
        else:
            for address in forward_lookup(query):
                print(f"{query} -> {address}")
    except (socket.gaierror, socket.herror) as error:
        print(f"{query}: lookup failed ({error})")


def main() -> None:
    raw = input("Enter hostnames or IPs separated by commas: ")

    for query in raw.split(","):
        if query.strip():
            lookup(query)


if __name__ == "__main__":
    main()
