import unittest

from src.formatter import format_network, int_to_ipv6
from src.ip_parser import parse_ip
from src.network import find_min_network


class IPv6TestCase(unittest.TestCase):
    def test_parse_ipv6_to_int(self):
        ip = parse_ip("::1")

        self.assertEqual(ip.version, 6)
        self.assertEqual(ip.bits, 128)
        self.assertEqual(ip.value, 1)

    def test_int_to_ipv6_with_compression(self):
        self.assertEqual(int_to_ipv6(0), "::")
        self.assertEqual(int_to_ipv6(1), "::1")
        self.assertEqual(int_to_ipv6(parse_ip("2001:db8::1").value), "2001:db8::1")

    def test_min_network_for_same_address(self):
        network = find_min_network(parse_ip("::1"), parse_ip("::1"))
        self.assertEqual(format_network(network), "::1/128")

    def test_min_network_for_neighbors(self):
        network = find_min_network(parse_ip("::1"), parse_ip("::2"))
        self.assertEqual(format_network(network), "::/126")

    def test_min_network_inside_one_ipv6_range(self):
        network = find_min_network(parse_ip("2001:db8::1"), parse_ip("2001:db8::ff"))
        self.assertEqual(format_network(network), "2001:db8::/120")

    def test_min_network_for_all_ipv6_addresses(self):
        network = find_min_network(
            parse_ip("::"),
            parse_ip("ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff"),
        )
        self.assertEqual(format_network(network), "::/0")

    def test_invalid_ipv6(self):
        invalid_addresses = [
            "2001:::1",
            "2001:db8::1::2",
            "2001:db8:0:0:0:0:0",
            "2001:db8::zz",
            "1:2:3:4:5:6:7:8::",
        ]

        for address in invalid_addresses:
            with self.assertRaises(ValueError):
                parse_ip(address)


if __name__ == "__main__":
    unittest.main()
