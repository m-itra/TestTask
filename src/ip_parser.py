import re

from src.models import ParsedIP

_IPV6_GROUP_RE = re.compile(r"[0-9A-Fa-f]{1,4}")


def parse_ip(address: str) -> ParsedIP:
    address = address.strip()

    if "." in address and ":" not in address:
        return ParsedIP(
            version=4,
            bits=32,
            value=_parse_ipv4_to_int(address),
        )

    if ":" in address and "." not in address:
        return ParsedIP(
            version=6,
            bits=128,
            value=_parse_ipv6_to_int(address),
        )

    raise ValueError("IP-адрес должен быть корректным IPv4 или IPv6")


def _parse_ipv4_to_int(address: str) -> int:
    octets = _split_ipv4(address)
    value = 0

    for octet in octets:
        value = (value << 8) | octet

    return value


def _split_ipv4(address: str) -> list[int]:
    parts = address.split(".")

    if len(parts) != 4:
        raise ValueError("IPv4-адрес должен состоять из 4 октетов")

    octets = []

    for part in parts:
        if not part:
            raise ValueError("IPv4-октет не должен быть пустым")

        if not part.isdigit():
            raise ValueError("IPv4-октет должен содержать только цифры")

        octet = int(part)

        if octet < 0 or octet > 255:
            raise ValueError("IPv4-октет должен быть в диапазоне от 0 до 255")

        octets.append(octet)

    return octets


def _parse_ipv6_to_int(address: str) -> int:
    groups = _split_ipv6(address)
    value = 0

    for group in groups:
        value = (value << 16) | group

    return value


def _split_ipv6(address: str) -> list[int]:
    if address.count("::") > 1:
        raise ValueError("IPv6-адрес может содержать только одно сокращение ::")

    if "::" in address:
        left, right = address.split("::")
        left_groups = _split_ipv6_side(left)
        right_groups = _split_ipv6_side(right)
        missing_groups = 8 - len(left_groups) - len(right_groups)

        if missing_groups < 1:
            raise ValueError("Сокращение :: должно заменять минимум одну группу")

        groups = left_groups + ([0] * missing_groups) + right_groups
        if len(groups) != 8:
            raise ValueError("После раскрытия IPv6-адрес должен содержать 8 групп")
    else:
        groups = _split_ipv6_side(address)

        if len(groups) != 8:
            raise ValueError("IPv6-адрес должен содержать 8 групп или сокращение ::")

    return groups


def _split_ipv6_side(side: str) -> list[int]:
    if side == "":
        return []

    parts = side.split(":")

    if "" in parts:
        raise ValueError("IPv6-группа не должна быть пустой")

    return [_parse_ipv6_group(part) for part in parts]


def _parse_ipv6_group(group: str) -> int:
    if not _IPV6_GROUP_RE.fullmatch(group):
        raise ValueError("IPv6-группа должна содержать от 1 до 4 hex-символов")
    return int(group, 16)
