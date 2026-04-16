from src.models import Network


def format_network(network: Network) -> str:
    address = _format_ip(network.value, network.version)
    mask_value = _prefix_to_mask(network.prefix, network.bits)
    mask = _format_ip(mask_value, network.version)

    return (
        f"{'Network:':<8} {address}/{network.prefix}\n"
        f"{'Mask:':<8} {mask}"
    )


def _prefix_to_mask(prefix: int, bits: int) -> int:
    return ((1 << prefix) - 1) << (bits - prefix)


def _format_ip(value: int, version: int) -> str:
    return {4: int_to_ipv4, 6: int_to_ipv6}[version](value)


def int_to_ipv4(value: int) -> str:
    octets = []

    for shift in (24, 16, 8, 0):
        octets.append(str((value >> shift) & 255))

    return ".".join(octets)


def int_to_ipv6(value: int) -> str:
    groups = []

    for shift in range(112, -1, -16):
        groups.append((value >> shift) & 65535)

    best_start = -1
    best_length = 0
    current_start = -1
    current_length = 0

    for index, group in enumerate(groups + [1]):
        if group == 0:
            if current_start == -1:
                current_start = index
                current_length = 1
            else:
                current_length += 1
        else:
            if current_length > best_length:
                best_start = current_start
                best_length = current_length

            current_start = -1
            current_length = 0

    if best_length < 2:
        return ":".join(_format_ipv6_group(group) for group in groups)

    left = [_format_ipv6_group(group) for group in groups[:best_start]]
    right = [_format_ipv6_group(group) for group in groups[best_start + best_length:]]

    if not left and not right:
        return "::"

    if not left:
        return "::" + ":".join(right)

    if not right:
        return ":".join(left) + "::"

    return ":".join(left) + "::" + ":".join(right)


def _format_ipv6_group(group: int) -> str:
    return format(group, "x")
