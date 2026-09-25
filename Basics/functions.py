"""
Functions: reusable blocks of code with inputs and a return value.
"""


def is_private(ip: str) -> bool:
    """Return True if the IPv4 address is in an RFC 1918 private range."""
    first, second = (int(part) for part in ip.split(".")[:2])
    return first == 10 or (first == 172 and 16 <= second <= 31) or (first == 192 and second == 168)


def describe_device(hostname: str, ip: str, role: str = "access-switch") -> str:
    """Build a one-line description of a device. 'role' has a default value."""
    scope = "private" if is_private(ip) else "public"
    return f"{hostname:<10} {ip:<15} {role:<14} ({scope})"


devices = [
    ("core-sw1", "10.0.0.1", "core-switch"),
    ("edge-fw1", "203.0.113.1", "firewall"),
    ("acc-sw1", "192.168.1.10"),
]

for device in devices:
    print(describe_device(*device))
