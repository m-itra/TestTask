from dataclasses import dataclass


_IP_BITS_BY_VERSION = {
    4: 32,
    6: 128,
}


@dataclass(frozen=True)
class ParsedIP:
    version: int
    value: int

    @property
    def bits(self) -> int:
        return _IP_BITS_BY_VERSION[self.version]


@dataclass(frozen=True)
class Network:
    version: int
    value: int
    prefix: int

    @property
    def bits(self) -> int:
        return _IP_BITS_BY_VERSION[self.version]
