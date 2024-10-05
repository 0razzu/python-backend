from dataclasses import dataclass, field
from typing import Annotated


@dataclass(slots=True)
class Item:
    id: int | None
    name: str
    price: float
    deleted: bool

    def __repr__(self):
        return f'{self.id}, {self.name}'

    def __hash__(self):
        return hash(repr(self))


@dataclass(slots=True)
class PatchItemInfo:
    name: str | None = None
    price: float | None = None

    def __bool__(self) -> bool:
        return self.name is not None or self.price is not None


@dataclass(slots=True)
class Cart:
    id: int | None = None
    items: dict[Item, Annotated[int, 'Quantity']] = field(default_factory=dict)

    def __repr__(self):
        return f'{self.id}'

    def __hash__(self):
        return hash(repr(self))
