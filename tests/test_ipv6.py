import pytest

from src.formatter import format_network, int_to_ipv6
from src.ip_parser import parse_ip
from src.network import find_min_network

IPV6_VERSION = 6
IPV6_BITS = 128


def test_parse_ipv6_to_int():
    address = "::1"
    expected_version = IPV6_VERSION
    expected_bits = IPV6_BITS
    expected_value = 1

    ip = parse_ip(address)

    assert ip.version == expected_version
    assert ip.bits == expected_bits
    assert ip.value == expected_value


def test_parse_ipv6_groups_with_leading_zeroes():
    address_with_leading_zeroes = "1000:0010:1000::1"
    expected_address = "1000:10:1000::1"

    assert parse_ip(address_with_leading_zeroes) == parse_ip(expected_address)


def test_parse_ipv6_strips_port():
    address_with_port = "[::1]:443"
    expected_address = "::1"

    assert parse_ip(address_with_port) == parse_ip(expected_address)


def test_parse_ipv4_mapped_ipv6_to_int():
    address = "::ffff:192.168.1.1"
    equivalent_hex_address = "::ffff:c0a8:101"
    expected_version = IPV6_VERSION
    expected_bits = IPV6_BITS
    expected_value = parse_ip(equivalent_hex_address).value

    ip = parse_ip(address)

    assert ip.version == expected_version
    assert ip.bits == expected_bits
    assert ip.value == expected_value


def test_parse_ipv4_mapped_ipv6_strips_port():
    address_with_port = "[::ffff:192.168.1.1]:443"
    expected_address = "::ffff:192.168.1.1"

    assert parse_ip(address_with_port) == parse_ip(expected_address)


def test_int_to_ipv6_with_compression():
    zero_value = 0
    uncompressed_address = "2001:0db8:0000:0000:0000:0000:0000:0001"
    expected_address = "2001:db8::1"

    assert int_to_ipv6(zero_value) == "::"
    assert int_to_ipv6(parse_ip(uncompressed_address).value) == expected_address


def test_min_network_for_same_address():
    first_address = "::1"
    second_address = "::1"
    expected_network = (
        "Network: ::1/128\n"
        "Mask:    ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff"
    )

    network = find_min_network(parse_ip(first_address), parse_ip(second_address))
    assert format_network(network) == expected_network


def test_min_network_for_neighbors():
    first_address = "::1"
    second_address = "::2"
    expected_network = (
        "Network: ::/126\n"
        "Mask:    ffff:ffff:ffff:ffff:ffff:ffff:ffff:fffc"
    )

    network = find_min_network(parse_ip(first_address), parse_ip(second_address))
    assert format_network(network) == expected_network


def test_min_network_inside_one_ipv6_range():
    first_address = "2001:db8::1"
    second_address = "2001:db8::ff"
    expected_network = (
        "Network: 2001:db8::/120\n"
        "Mask:    ffff:ffff:ffff:ffff:ffff:ffff:ffff:ff00"
    )

    network = find_min_network(parse_ip(first_address), parse_ip(second_address))
    assert format_network(network) == expected_network


def test_min_network_for_ipv4_mapped_ipv6_range():
    first_address = "::ffff:192.168.1.1"
    second_address = "::ffff:192.168.1.254"
    expected_network = (
        "Network: ::ffff:192.168.1.0/120\n"
        "Mask:    ffff:ffff:ffff:ffff:ffff:ffff:ffff:ff00"
    )

    network = find_min_network(parse_ip(first_address), parse_ip(second_address))
    assert format_network(network) == expected_network


def test_min_network_for_all_ipv6_addresses():
    first_address = "::"
    second_address = "ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff"
    expected_network = (
        "Network: ::/0\n"
        "Mask:    ::"
    )

    network = find_min_network(parse_ip(first_address), parse_ip(second_address))
    assert format_network(network) == expected_network


@pytest.mark.parametrize(
    "address",
    [
        "2001:::1",
        "2001:db8::1::2",
        "2001:db8:0:0:0:0:0",
        "2001:db8::zz",
        "1:2:3:4:5:6:7:8::",
        "::ffff:192.168.1",
        "::ffff:192.168.1.999",
        "::ffff:192.168.1.1:abcd",
        "[::1",
        "[]:443",
        "[::1]:",
        "[::1]:https",
        "[::1]:65536",
    ],
)
def test_invalid_ipv6(address):
    with pytest.raises(ValueError):
        parse_ip(address)
