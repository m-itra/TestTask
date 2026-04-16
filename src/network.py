from src.models import Network, ParsedIP


def find_min_network(first_ip: ParsedIP, second_ip: ParsedIP) -> Network:
    if first_ip.version != second_ip.version:
        raise ValueError("IP-адреса должны быть одной версии")

    diff = first_ip.value ^ second_ip.value

    bits = first_ip.bits
    if diff == 0:
        prefix = bits
    else:
        prefix = bits - diff.bit_length()

    host_bits = bits - prefix
    mask = ((1 << prefix) - 1) << host_bits
    network_value = first_ip.value & mask

    return Network(
        version=first_ip.version,
        bits=bits,
        value=network_value,
        prefix=prefix,
    )
