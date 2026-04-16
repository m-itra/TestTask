import sys

from src.ip_parser import parse_ip
from src.network import find_min_network
from src.formatter import format_network


def _get_addresses(argv):
    if len(argv) == 3:
        return argv[1], argv[2]

    if len(argv) == 1:
        first_address = input("Введите первый IP-адрес: ")
        second_address = input("Введите второй IP-адрес: ")
        return first_address, second_address

    raise ValueError("передайте два IP-адреса аргументами или запустите без аргументов")


def main():
    try:
        first_address, second_address = _get_addresses(sys.argv)
        first_ip = parse_ip(first_address)
        second_ip = parse_ip(second_address)
        network = find_min_network(first_ip, second_ip)
    except ValueError as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 1

    print(format_network(network))
    return 0


if __name__ == "__main__":
    sys.exit(main())
