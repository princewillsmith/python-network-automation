"""
Validate IP addresses and classify them (private, public, loopback, multicast, etc.).
"""

import ipaddress


def classify(address: str) -> str:
    """Return a human-readable classification of an IPv4 or IPv6 address."""

    try:
        ip = ipaddress.ip_address(address.strip())
    except ValueError:
        return "INVALID"

    if ip.is_loopback:
        kind = "loopback"
    elif ip.is_link_local:
        kind = "link-local"
    elif ip.is_multicast:
        kind = "multicast"
    elif ip.is_private:
        kind = "private"
    elif ip.is_reserved or ip.is_unspecified:
        kind = "reserved"
    else:
        kind = "public"

    return f"valid IPv{ip.version}, {kind}"


def main() -> None:
    raw = input("Enter IP addresses separated by commas: ")

    for address in raw.split(","):
        if address.strip():
            print(f"{address.strip():<40} {classify(address)}")


if __name__ == "__main__":
    main()
