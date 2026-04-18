import pytest

from src.formatter import format_network, int_to_ipv4
from src.ip_parser import parse_ip
from src.network import find_min_network

IPV4_VERSION = 4
IPV4_BITS = 32


def test_parse_ipv4_uses_octets_as_bytes():
    address = "192.168.1.10"
    expected_version = IPV4_VERSION
    expected_bits = IPV4_BITS
    expected_value = 3232235786

    ip = parse_ip(address)

    assert ip.version == expected_version
    assert ip.bits == expected_bits
    assert ip.value == expected_value


def test_parse_ipv4_strips_port():
    address_with_port = "192.168.1.10:8080"
    expected_address = "192.168.1.10"
    assert parse_ip(address_with_port) == parse_ip(expected_address)


def test_int_to_ipv4():
    value = 3232235786
    expected_address = "192.168.1.10"
    assert int_to_ipv4(value) == expected_address


def test_min_network_inside_one_subnet():
    first_address = "192.168.1.10"
    second_address = "192.168.1.20"
    expected_network = (
        "Network: 192.168.1.0/27\n"
        "Mask:    255.255.255.224"
    )

    network = find_min_network(parse_ip(first_address), parse_ip(second_address))
    assert format_network(network) == expected_network


def test_min_network_for_same_address():
    first_address = "10.0.0.1"
    second_address = "10.0.0.1"
    expected_network = (
        "Network: 10.0.0.1/32\n"
        "Mask:    255.255.255.255"
    )

    network = find_min_network(parse_ip(first_address), parse_ip(second_address))
    assert format_network(network) == expected_network


def test_min_network_for_all_ipv4_addresses():
    first_address = "0.0.0.0"
    second_address = "255.255.255.255"
    expected_network = (
        "Network: 0.0.0.0/0\n"
        "Mask:    0.0.0.0"
    )

    network = find_min_network(parse_ip(first_address), parse_ip(second_address))
    assert format_network(network) == expected_network


def test_min_network_for_different_first_bit():
    first_address = "10.0.0.1"
    second_address = "172.16.0.1"
    expected_network = (
        "Network: 0.0.0.0/0\n"
        "Mask:    0.0.0.0"
    )

    network = find_min_network(parse_ip(first_address), parse_ip(second_address))
    assert format_network(network) == expected_network


@pytest.mark.parametrize(
    "address",
    [
        "192.168.1",
        "192.168.1.999",
        "192..1.1",
        "abc.def.1.2",
        "192.168.1.1:",
        "192.168.1.1:http",
        "192.168.1.1:65536",
    ],
)
def test_invalid_ipv4(address):
    with pytest.raises(ValueError):
        parse_ip(address)
