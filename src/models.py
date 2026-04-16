from dataclasses import dataclass


@dataclass(frozen=True)
class ParsedIP:
    version: int
    bits: int
    value: int


@dataclass(frozen=True)
class Network:
    version: int
    bits: int
    value: int
    prefix: int
