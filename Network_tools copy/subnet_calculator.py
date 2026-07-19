"""
Calculate IPv4 subnet information.
"""

import ipaddress

def calculate_subnet(network_input: str) -> None:
    """Display useful information about an IPv4 network."""

    try:
        network = ipaddress.ip_network(network_input, strict=False)
    except ValueError as error:
        print(f"Invalid network: {error}")
        return

    usable_hosts = max(network.num_addresses - 2, 0)

    print("\nSubnet information")
    print(f"Network address:   {network.network_address}")
    print(f"Broadcast address: {network.broadcast_address}")
    print(f"Subnet mask:       {network.netmask}")
    print(f"Prefix length:     /{network.prefixlen}")
    print(f"Total addresses:   {network.num_addresses}")
    print(f"Usable hosts:      {usable_hosts}")

    if usable_hosts > 0:
        hosts = list(network.hosts())
        print(f"First usable host: {hosts[0]}")
        print(f"Last usable host:  {hosts[-1]}")


def main() -> None:
    network_input = input("Enter a network, for example 192.168.10.0/24: ")
    calculate_subnet(network_input)


if __name__ == "__main__":
    main()
