import unittest

from src.formatter import format_network, int_to_ipv4
from src.ip_parser import parse_ip
from src.network import find_min_network


class IPv4TestCase(unittest.TestCase):
    def test_parse_ipv4_uses_octets_as_bytes(self):
        ip = parse_ip("192.168.1.10")

        self.assertEqual(ip.version, 4)
        self.assertEqual(ip.bits, 32)
        self.assertEqual(ip.value, 3232235786)

    def test_int_to_ipv4(self):
        self.assertEqual(int_to_ipv4(3232235786), "192.168.1.10")

    def test_min_network_inside_one_subnet(self):
        network = find_min_network(parse_ip("192.168.1.10"), parse_ip("192.168.1.20"))
        self.assertEqual(
            format_network(network),
            "Network: 192.168.1.0/27\nMask:    255.255.255.224",
        )

    def test_min_network_for_same_address(self):
        network = find_min_network(parse_ip("10.0.0.1"), parse_ip("10.0.0.1"))
        self.assertEqual(
            format_network(network),
            "Network: 10.0.0.1/32\nMask:    255.255.255.255",
        )

    def test_min_network_for_all_ipv4_addresses(self):
        network = find_min_network(parse_ip("0.0.0.0"), parse_ip("255.255.255.255"))
        self.assertEqual(
            format_network(network),
            "Network: 0.0.0.0/0\nMask:    0.0.0.0",
        )

    def test_min_network_for_different_first_bit(self):
        network = find_min_network(parse_ip("10.0.0.1"), parse_ip("172.16.0.1"))
        self.assertEqual(
            format_network(network),
            "Network: 0.0.0.0/0\nMask:    0.0.0.0",
        )

    def test_invalid_ipv4(self):
        invalid_addresses = [
            "192.168.1",
            "192.168.1.999",
            "192..1.1",
            "abc.def.1.2",
        ]

        for address in invalid_addresses:
            with self.assertRaises(ValueError):
                parse_ip(address)


if __name__ == "__main__":
    unittest.main()
