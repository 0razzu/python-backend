from dataclasses import dataclass
from typing import Iterable


def _int_id_generator() -> Iterable[int]:
    i = 0
    while True:
        yield i
        i += 1


id_generator = _int_id_generator()


@dataclass(slots=True)
class DBItem:
    name: str
    price: float
    deleted: bool


@dataclass(slots=True)
class DBCart:
    items: list[int]


items = {}
carts = {}
