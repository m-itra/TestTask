import re
from src.models import ParsedIP

_IPV6_GROUP_RE = re.compile(r"[0-9A-Fa-f]{1,4}")


def parse_ip(address: str) -> ParsedIP:
    address = _strip_port(address.strip())

    if "." in address and ":" not in address:
        return ParsedIP(
            version=4,
            value=_parse_ipv4_to_int(address),
        )

    if ":" in address:
        return ParsedIP(
            version=6,
            value=_parse_ipv6_to_int(address),
        )

    raise ValueError("IP-адрес должен быть корректным IPv4 или IPv6")


def _strip_port(address: str) -> str:
    if address.startswith("["):
        return _strip_bracketed_port(address)

    if address.count(":") == 1 and "." in address:
        host, port = address.split(":")
        _validate_port(port)
        return host

    return address


def _strip_bracketed_port(address: str) -> str:
    close_bracket_index = address.find("]")

    if close_bracket_index == -1:
        raise ValueError("IP-адрес с портом должен быть в формате [адрес]:порт")

    host = address[1:close_bracket_index]
    port = address[close_bracket_index + 1:]

    if not host:
        raise ValueError("IP-адрес внутри скобок не должен быть пустым")

    if not port:
        return host

    if not port.startswith(":"):
        raise ValueError("IP-адрес с портом должен быть в формате [адрес]:порт")

    _validate_port(port[1:])
    return host


def _validate_port(port: str) -> None:
    if not port:
        raise ValueError("Порт не должен быть пустым")

    if not port.isdigit():
        raise ValueError("Порт должен содержать только цифры")

    if int(port) > 65535:
        raise ValueError("Порт должен быть в диапазоне от 0 до 65535")


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
        left_groups = _split_ipv6_side(left, allow_ipv4_tail=False)
        right_groups = _split_ipv6_side(right, allow_ipv4_tail=True)
        missing_groups = 8 - len(left_groups) - len(right_groups)

        if missing_groups < 1:
            raise ValueError("Сокращение :: должно заменять минимум одну группу")

        groups = left_groups + ([0] * missing_groups) + right_groups
        if len(groups) != 8:
            raise ValueError("После раскрытия IPv6-адрес должен содержать 8 групп")
    else:
        groups = _split_ipv6_side(address, allow_ipv4_tail=True)

        if len(groups) != 8:
            raise ValueError("IPv6-адрес должен содержать 8 групп или сокращение ::")

    return groups


def _split_ipv6_side(side: str, allow_ipv4_tail: bool) -> list[int]:
    if side == "":
        return []

    parts = side.split(":")

    if "" in parts:
        raise ValueError("IPv6-группа не должна быть пустой")

    if any("." in part for part in parts[:-1]):
        raise ValueError("IPv4-хвост IPv6-адреса должен быть последней частью")

    if "." in parts[-1]:
        if not allow_ipv4_tail:
            raise ValueError("IPv4-хвост IPv6-адреса должен быть последней частью")

        return [
            *(_parse_ipv6_group(part) for part in parts[:-1]),
            *_parse_ipv4_tail(parts[-1]),
        ]

    return [_parse_ipv6_group(part) for part in parts]


def _parse_ipv4_tail(address: str) -> list[int]:
    ipv4_value = _parse_ipv4_to_int(address)
    return [(ipv4_value >> 16) & 65535, ipv4_value & 65535]


def _parse_ipv6_group(group: str) -> int:
    if not _IPV6_GROUP_RE.fullmatch(group):
        raise ValueError("IPv6-группа должна содержать от 1 до 4 hex-символов")
    return int(group, 16)
