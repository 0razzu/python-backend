from dataclasses import dataclass, field
from typing import Iterable, Annotated


def _int_id_generator() -> Iterable[int]:
    i = 0
    while True:
        yield i
        i += 1


_id_generator = _int_id_generator()


def generate_id() -> int:
    return next(_id_generator)


@dataclass(slots=True)
class DBItem:
    name: str
    price: float
    deleted: bool


@dataclass(slots=True)
class DBCart:
    items: dict[Annotated[int, 'Item ID'], Annotated[int, 'Quantity']] = field(default_factory=dict)


items: dict[Annotated[int, 'ID'], DBItem] = {}
carts: dict[Annotated[int, 'ID'], DBCart] = {}
